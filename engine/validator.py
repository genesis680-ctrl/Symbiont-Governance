import json
import os
import sys
import importlib.util
from datetime import datetime

# --- CONFIGURAÇÕES DE AMBIENTE ---
REPORT_FILE = "audit_report.json"

class GovernanceEngine:
    def __init__(self):
        self.manifest = self._load_manifest()
        self.violations = []
        self.stats = {"files_scanned": 0, "rules_executed": 0}

    def _load_manifest(self):
        try:
            with open('rules/rule_manifest.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("CRITICAL: Manifesto de regras não encontrado.")
            sys.exit(1)

    def scan_project(self, root_dir="."):
        print(f"🛡️  SYMBIONT ENGINE v2.0 - Iniciando Scan em {root_dir}...")
        
        start_time = datetime.now()

        for root, _, files in os.walk(root_dir):
            if ".git" in root or "engine" in root: continue

            for filename in files:
                filepath = os.path.join(root, filename)
                self.stats["files_scanned"] += 1
                
                # Ignora arquivos binários ou sem extensão relevante
                if not filename.endswith(('.py', '.md', '.json', '.yml', '.txt')):
                    continue

                self._apply_rules(filepath, filename)

        duration = (datetime.now() - start_time).total_seconds()
        self._generate_report(duration)
        
        return len(self.violations)

    def _apply_rules(self, filepath, filename):
        try:
            with open(filepath, 'r', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return

        for rule_config in self.manifest['active_rules']:
            # Importação dinâmica e otimizada
            spec = importlib.util.spec_from_file_location("rule_module", rule_config['file'])
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Executa a regra
                findings = module.check(content, filename)
                self.stats["rules_executed"] += 1
                
                if findings:
                    for find in findings:
                        violation_data = {
                            "rule_id": rule_config['id'],
                            "severity": rule_config['severity'],
                            "file": filepath,
                            "line": find['line'],
                            "message": find['message'],
                            "timestamp": datetime.now().isoformat()
                        }
                        self.violations.append(violation_data)
                        print(f"❌ VIOLAÇÃO [{rule_config['id']}]: {filepath}:{find['line']}")

    def _generate_report(self, duration):
        report = {
            "meta": {
                "project": self.manifest['project'],
                "scan_date": datetime.now().isoformat(),
                "duration_seconds": duration,
                "engine_version": "2.0.0"
            },
            "summary": {
                "total_files": self.stats["files_scanned"],
                "total_violations": len(self.violations),
                "status": "FAILED" if self.violations else "PASSED"
            },
            "violations": self.violations
        }
        
        with open(REPORT_FILE, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Relatório de auditoria gerado: {REPORT_FILE}")

def main():
    engine = GovernanceEngine()
    failures = engine.scan_project()
    
    if failures > 0:
        print(f"\n🔴 FALHA CRÍTICA: {failures} violações detectadas. Deploy abortado.")
        sys.exit(1)
    else:
        print("\n🟢 SUCESSO: Nenhum violação encontrada.")
        sys.exit(0)

if __name__ == "__main__":
    main()

