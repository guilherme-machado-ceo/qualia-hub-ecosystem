# QuantumReady — Migração Criptográfica Pós-Quântica

**Instância IPII para domínio de criptografia pós-quântica**
**Status:** Especificação | **Produto:** Et Alii Advisory + Qualia Hub

---

## O Problema

*Harvest now, decrypt later*: atores estatais coletam dados
criptografados hoje para decriptar quando tiverem capacidade quântica.
O NIST publicou os primeiros algoritmos PQC em 2024.
O Brasil não tem marco regulatório quântico.
A LGPD já exige proteção de dados pessoais —
o risco quântico é compliance presente, não futuro.

---

## O que a IPII resolve aqui

A transição PQC não é trocar um algoritmo por outro.
É preservar a semântica de segurança através da migração:
confidencialidade, integridade, autenticidade e não-repúdio
precisam ser mantidos com propriedades matemáticas radicalmente
diferentes.

| Sistema Fonte | Sistema Alvo |
|---------------|--------------|
| RSA-2048 | CRYSTALS-Kyber (KEM) |
| ECDSA | CRYSTALS-Dilithium (assinatura) |
| SHA-256 | SPHINCS+ (hash-based) |
| AES-256 | FALCON (assinatura leve) |

A IPII mapeia equivalências funcionais e detecta gaps onde
a semântica de segurança é perdida ou degradada na transição.

---

## Contexto Regulatório

- NIST PQC Standards (2024): CRYSTALS-Kyber, Dilithium, SPHINCS+, FALCON
- EU Quantum Act: previsto mid-2026
- EU PQC Roadmap: todos os Estados-Membros devem ter planos até fim de 2026
- Brasil: vazio regulatório total — oportunidade de posicionamento

---

## Produto: QuantumReady Assessment

**Entregável:** diagnóstico de exposição criptográfica + roadmap PQC
**Âncora legal:** LGPD (dados pessoais em risco) + ECA Digital
**Público:** empresas com dados sensíveis, infraestrutura crítica,
  operadores financeiros, jurídico digital

---

*Instância IPII. Core: Qualia Hub Ecosystem / Hubstry Deep Tech.*
*Produto comercial: Gonçalves et Alii — https://goncalvesetalii.github.io*
