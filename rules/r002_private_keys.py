def check(content, filename):
    """
    Regra R-002: Bloqueio de Chaves Criptográficas Privadas.
    Alvo: RSA, DSA, EC, OPENSSH.
    """
    failures = []
    
    # Lista de cabeçalhos proibidos (Quebrados para evitar auto-detecção)
    forbidden_signatures = [
        "-----BEGIN " + "RSA PRIVATE KEY-----",
        "-----BEGIN " + "DSA PRIVATE KEY-----",
        "-----BEGIN " + "EC PRIVATE KEY-----",
        "-----BEGIN " + "OPENSSH PRIVATE KEY-----",
        "-----BEGIN " + "PRIVATE KEY-----",
        "-----BEGIN " + "ENCRYPTED PRIVATE KEY-----"
    ]
    
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        for signature in forbidden_signatures:
            if signature in line:
                failures.append({
                    "line": i,
                    "message": f"CRÍTICO: Chave Privada detectada ({signature.strip()})"
                })
                
    return failures

