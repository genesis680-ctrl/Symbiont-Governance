import re

def check(content, filename):
    """
    Regra R-001: Procura por chaves de acesso AWS.
    Retorna: Lista de falhas encontradas.
    """
    failures = []
    # Padrão oficial da AWS para chaves de acesso
    pattern = r"AKIA[0-9A-Z]{16}"
    
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if re.search(pattern, line):
            failures.append({
                "line": i,
                "message": "AWS Access Key ID detectada (R-001)"
            })
    return failures

