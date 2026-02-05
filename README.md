# 🏛️ Symbiont Governance Protocol

![Build Status](https://img.shields.io/badge/governance-active-success)
![Security](https://img.shields.io/badge/security-hardened-blue)
![Platform](https://img.shields.io/badge/platform-github%20actions-gray)

**Symbiont** é uma infraestrutura de governança como código (Governance-as-Code) projetada para ambientes de alta conformidade. Diferente de linters tradicionais, o Symbiont atua como uma camada de auditoria determinística, bloqueando violações de segurança, lógica e compliance antes que atinjam a produção.

## 🚀 Capacidades do Core Engine

- **Auditoria Determinística:** Regras escritas em Python puro para validação complexa.
- **Zero-Config CI/CD:** Integração nativa com GitHub Actions.
- **Bloqueio Hard-Fail:** Impede merge de código inseguro (Credenciais, Chaves RSA, Padrões Vulneráveis).
- **Arquitetura Modular:** Regras carregadas dinamicamente via Manifesto JSON.

## 🛠️ Arquitetura do Sistema

O sistema opera em três camadas:

1.  **The Manifest (`rule_manifest.json`):** A constituição do projeto. Define quais regras estão ativas e sua severidade.
2.  **The Rules (`/rules`):** Scripts modulares e isolados que executam a lógica de verificação.
3.  **The Engine (`validator.py`):** O orquestrador que carrega o contexto, executa a auditoria e gera relatórios de telemetria.

## 📦 Instalação e Uso

### Integração Local (Desenvolvedores)
```bash
# Executar auditoria manual antes do commit
python engine/validator.py

## 📊 Fluxo de Auditoria (Workflow)

```mermaid
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

