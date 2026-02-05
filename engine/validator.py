import json
import os
import sys
import importlib.util

# Configuração de Cores para Logs
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

def load_rules():
    with open('rules/rule_manifest.json', 'r') as f:
        return json.load(f)

def run_audit():
    manifest = load_rules()
    print(f"🛡️  INICIANDO AUDITORIA: {manifest['project']} v{manifest['version']}\n")
    
    total_failures = 0
    
    # Varre todos os arquivos do projeto
    for root, dirs, files in os.walk("."):
        if ".git" in root or "engine" in root: continue # Ignora sistema
        
        for filename in files:
            if not filename.endswith(".py") and not filename.endswith(".md"): continue
            
            filepath = os.path.join(root, filename)
            try:
                with open(filepath, 'r', errors='ignore') as f:
                    content = f.read()
            except:
                continue

            # Para cada arquivo, roda TODAS as regras ativas
            for rule_config in manifest['active_rules']:
                # Carrega o módulo da regra dinamicamente
                spec = importlib.util.spec_from_file_location("rule_module", rule_config['file'])
                rule_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(rule_module)
                
                # Executa a checagem
                failures = rule_module.check(content, filename)
                
                if failures:
                    print(f"{RED}❌ [VIOLAÇÃO] {rule_config['id']} em: {filepath}{RESET}")
                    for fail in failures:
                        print(f"   ∟ Linha {fail['line']}: {fail['message']}")
                    total_failures += len(failures)

    print("\n" + "="*40)
    if total_failures > 0:
        print(f"{RED}🔴 FALHA: {total_failures} violações de governança impediram o deploy.{RESET}")
        sys.exit(1)
    else:
        print(f"{GREEN}🟢 SUCESSO: O código está em conformidade.{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    run_audit()

