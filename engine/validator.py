import json
import os
import sys
import importlib.util
from datetime import datetime

# --- CONFIGURAÇÕES ---
REPORT_FILE = "audit_report.json"
MANIFEST_FILE = "rules/rule_manifest.json"
WHITELIST_FILE = "rules/whitelist.json"

class GovernanceEngine:
    def __init__(self):
        self.manifest = self._load_json(MANIFEST_FILE)
        self.whitelist = self._load_json(WHITELIST_FILE)
        self.violations = []
        self.stats = {"files_scanned": 0, "rules_executed": 0, "whitelisted_events": 0}

    def _load_json(self, filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Se não tiver whitelist, cria um dicionário vazio para não quebrar
            return {"approved_exceptions": []} if "whitelist" in filepath else {}

    def is_whitelisted(self, filepath, rule_id):
        """Verifica se a violação foi autorizada pelo CISO."""
        for exception in self.whitelist.get("approved_exceptions", []):
            # Normaliza os caminhos para evitar erro de ./
            exc_file = os.path.normpath(exception['file'])
            curr_file = os.path.normpath(filepath)
            
            if exc_file == curr_file and exception['rule_id'] == rule_id:
                return True
        return False

    def scan_project(self, root_dir="."):
        print(f"🛡️  SYMBIONT ENGINE v2.1 (Enterprise) - Iniciando Scan...")
        start_time = datetime.now()

        for root, _, files in os.walk(root_dir):
            if ".git" in root or "engine" in root: continue

            for filename in files:
                if not filename.endswith(('.py', '.md', '.json', '.yml')): continue
                
                filepath = os.path.join(root, filename)
                self.stats["files_scanned"] += 1
                self._apply_rules(filepath, filename)

        duration = (datetime.now() - start_time).total_seconds()
        self._generate_report(duration)
        return len(self.violations)

    def _apply_rules(self, filepath, filename):
        try:
            with open(filepath, 'r', errors='ignore') as f:
                content = f.read()
        except: return

        for rule_config in self.manifest.get('active_rules', []):
            spec = importlib.util.spec_from_file_location("rule", rule_config['file'])
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                findings = module.check(content, filename)
                self.stats["rules_executed"] += 1
                
                if findings:
                    # AQUI ACONTECE A MÁGICA DA WHITELIST
                    if self.is_whitelisted(filepath, rule_config['id']):
                        print(f"⚠️  ALERTA IGNORADO (Whitelist): {filepath} [{rule_config['id']}]")
                        self.stats["whitelisted_events"] += 1
                    else:
                        for find in findings:
                            self.violations.append({
                                "rule_id": rule_config['id'],
                                "severity": rule_config['severity'],
                                "file": filepath,
                                "line": find['line'],
                                "message": find['message'],
                                "timestamp": datetime.now().isoformat()
                            })
                            print(f"❌ VIOLAÇÃO [{rule_config['id']}]: {filepath}:{find['line']}")

    def _generate_report(self, duration):
        report = {
            "meta": {
                "project": self.manifest.get('project', 'Unknown'),
                "scan_date": datetime.now().isoformat(),
                "duration_seconds": duration,
                "version": "2.1.0"
            },
            "summary": {
                "total_files": self.stats["files_scanned"],
                "violations_blocked": len(self.violations),
                "violations_allowed": self.stats["whitelisted_events"],
                "status": "FAILED" if self.violations else "PASSED"
            },
            "violations": self.violations
        }
        with open(REPORT_FILE, 'w') as f:
            json.dump(report, f, indent=2)

def main():
    engine = GovernanceEngine()
    failures = engine.scan_project()
    
    if failures > 0:
        print(f"\n🔴 FALHA: {failures} violações críticas. Deploy abortado.")
        sys.exit(1)
    else:
        print("\n🟢 SUCESSO: Código em conformidade (ou whitelisted).")
        sys.exit(0)

if __name__ == "__main__":
    main()

