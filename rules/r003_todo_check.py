def check(content, filename):
    """
    Regra R-003: Detecta Dívida Técnica (TODO/FIXME).
    Severidade esperada: LOW (Aviso).
    """
    failures = []
    
    # Truque: O sinal de + esconde a palavra do nosso próprio scanner
    keywords = ["TODO" + ":", "FIXME" + ":", "HACK" + ":"]
    
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        for word in keywords:
            if word in line:
                failures.append({
                    "line": i,
                    "message": f"Dívida Técnica detectada ({word})"
                })
                
    return failures

