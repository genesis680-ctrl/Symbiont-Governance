import json
import os
import sys
import importlib.util
from datetime import datetime

# --- CONFIGURAÇÕES ---
REPORT_FILE = "audit_report.json"
MANIFEST_FILE = "rules/rule_manifest.json"
WHITELIST_FILE = "rules/whitelist.json"

# Definição de Política: O que derruba o sistema?
BLOCKING_SEVERITIES = ["CRITICAL", "HIGH"]

class GovernanceEngine:
    def __init__(self):
        self.manifest = self._load_json(MANIFEST_FILE)
        self.whitelist = self._load_json(WHITELIST_FILE)
        self.violations = []
        self.stats = {
            "files_scanned": 0,
            "rules_executed": 0,
            "whitelisted_events": 0,
            "blocking_failures": 0
        }

    def _load_json(self, filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"approved_exceptions": []} if "whitelist" in filepath else {}

    def is_whitelisted(self, filepath, rule_id):
        for exception in self.whitelist.get("approved_exceptions", []):
            exc_file = os.path.normpath(exception['file'])
            curr_file = os.path.normpath(filepath)
            if exc_file == curr_file and exception['rule_id'] == rule_id:
                return True
        return False

    def scan_project(self, root_dir="."):
        print(f"🛡️  SYMBIONT ENGINE v2.3 (Severity Aware) - Iniciando Scan...")
        start_time = datetime.now()

        for root, _, files in os.walk(root_dir):
            if ".git" in root or "engine" in root: continue

            for filename in files:
                # --- CORREÇÃO: Ignora o próprio relatório para não dar erro falso ---
                if filename == REPORT_FILE: continue

                if not filename.endswith(('.py', '.md', '.json', '.yml', '.txt', '.pem', '.key', '.env')):
                    continue

                filepath = os.path.join(root, filename)
                self.stats["files_scanned"] += 1
                self._apply_rules(filepath, filename)

        duration = (datetime.now() - start_time).total_seconds()
        self._generate_report(duration)
        return self.stats["blocking_failures"]

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
                    if self.is_whitelisted(filepath, rule_config['id']):
                        print(f"⚠️  ALERTA IGNORADO (Whitelist): {filepath} [{rule_config['id']}]")
                        self.stats["whitelisted_events"] += 1
                    else:
                        for find in findings:
                            severity = rule_config.get('severity', 'MEDIUM')

                            # Log visual diferenciado
                            icon = "❌" if severity in BLOCKING_SEVERITIES else "⚠️ "
                            print(f"{icon} [{severity}] {rule_config['id']}: {filepath}:{find['line']}")

                            if severity in BLOCKING_SEVERITIES:
                                self.stats["blocking_failures"] += 1

                            self.violations.append({
                                "rule_id": rule_config['id'],
                                "severity": severity,
                                "file": filepath,
                                "line": find['line'],
                                "message": find['message'],
                                "timestamp": datetime.now().isoformat()
                            })

    def _generate_report(self, duration):
        report = {
            "meta": {
                "project": self.manifest.get('project', 'Unknown'),
                "scan_date": datetime.now().isoformat(),
                "duration_seconds": duration,
                "version": "2.3.0"
            },
            "summary": {
                "total_files": self.stats["files_scanned"],
                "violations_found": len(self.violations),
                "blocking_failures": self.stats["blocking_failures"],
                "status": "FAILED" if self.stats["blocking_failures"] > 0 else "PASSED"
            },
            "violations": self.violations
        }
        with open(REPORT_FILE, 'w') as f:
            json.dump(report, f, indent=2)

def main():
    engine = GovernanceEngine()
    blocking_errors = engine.scan_project()

    if blocking_errors > 0:
        print(f"\n🔴 FALHA CRÍTICA: {blocking_errors} violações bloqueantes detectadas.")
        sys.exit(1) # Quebra o deploy
    else:
        print("\n🟢 SUCESSO: Deploy aprovado (Avisos não-bloqueantes podem existir).")
        sys.exit(0) # Permite o deploy

if __name__ == "__main__":
    main()

