# Symbiont Governance Protocol

**Symbiont** e uma infraestrutura de governanca como codigo.

## Capacidades
- Auditoria: Regras em Python.
- Bloqueio: Impede codigo inseguro.

## Uso
```bash
python engine/validator.py
graph TD
    A[Dev Push] --> B(GitHub Actions)
    B --> C{Symbiont Engine}
    C --> F{Veredito?}
    F -- CRITICO --> G[BLOCK]
    F -- LEVE --> H[WARN]
    F -- OK --> I[PASS]

    style G fill:#ff0000,color:#fff
    style I fill:#00ff00,color:#000

