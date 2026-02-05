# O script cria as aspas 'magicas' para garantir que o GitHub entenda
aspas = chr(96) * 3

conteudo = f"""# 🏛️ Symbiont Governance Protocol

![Build Status](https://img.shields.io/badge/governance-active-success)
![Security](https://img.shields.io/badge/security-hardened-blue)

**Symbiont** é uma infraestrutura de governança como código.

## 🚀 Capacidades
- **Auditoria Determinística:** Regras em Python.
- **Bloqueio Hard-Fail:** Impede código inseguro.

## 📦 Instalação
### Integração Local
{aspas}bash
python engine/validator.py
{aspas}

## 📊 Fluxo de Auditoria

{aspas}mermaid
graph TD
    A[Dev Push] --> B(GitHub Actions)
    B --> C{{Symbiont Engine}}
    C --> F{{Verdict?}}
    F -- CRITICAL --> G[❌ BLOCK]
    F -- LOW --> H[⚠️ WARN]
    F -- Clean --> I[✅ PASS]

    style G fill:#ff0000,color:#fff
    style I fill:#00ff00,color:#000
{aspas}
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(conteudo)

print("✅ README recriado com sucesso!")

