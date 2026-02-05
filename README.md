# 🏛️ Symbiont Governance Protocol

![Build Status](https://img.shields.io/badge/governance-active-success)
![Security](https://img.shields.io/badge/security-hardened-blue)
![Platform](https://img.shields.io/badge/platform-github%20actions-gray)

**Symbiont** é uma infraestrutura de governança como código projetada para ambientes de alta conformidade.

## 🚀 Capacidades do Core Engine
- **Auditoria Determinística:** Regras em Python puro.
- **Bloqueio Hard-Fail:** Impede merge de código inseguro.
- **Arquitetura Modular:** Regras via Manifesto JSON.

## 🛠️ Arquitetura do Sistema
1.  **The Manifest (`rule_manifest.json`):** A constituição do projeto.
2.  **The Rules (`/rules`):** Scripts de verificação.
3.  **The Engine (`validator.py`):** O orquestrador.

## 📦 Instalação e Uso

### Integração Local (Desenvolvedores)

```bash
# Executar auditoria manual antes do commit
python engine/validator.py

graph TD
    A[Dev Commits Code] -->|Push| B(GitHub Actions)
    B --> C{Symbiont Engine}
    C -->|Load Rules| D[Rule Manifest]
    C -->|Check Exceptions| E[Whitelist DB]
    C --> F{Verdict?}
    F -- CRITICAL Violation --> G[❌ BLOCK DEPLOY]
    F -- LOW Severity --> H[⚠️ WARNING ONLY]
    F -- Clean --> I[✅ DEPLOY APPROVED]
    
    style G fill:#ff0000,stroke:#333,stroke-width:2px,color:#fff
    style I fill:#00ff00,stroke:#333,stroke-width:2px,color:#000
