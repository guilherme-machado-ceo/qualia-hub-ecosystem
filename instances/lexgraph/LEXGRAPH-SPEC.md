# LexGraph — Arquitetura Regulatória as a Service

**Instância IPII para mapeamento de legislação digital**
**Status:** MVP disponível | **Artefato:** lexgraph.jsx

---

## Definição

Grafo interativo da arquitetura regulatória digital brasileira.
Seis camadas: Internacional → Federal Vigente → Federal Tramitando
→ Apensados → Estadual → Produto/Serviço.

Cada nó é uma norma, PL ou produto. Cada aresta é uma relação
semântica: ancora, altera, incorpora, inspira, oportunidade.

---

## Artefato disponível

Ver [lexgraph.jsx](lexgraph.jsx) — componente React interativo.
Clique nos nós para detalhes. Drag para navegar. Scroll para zoom.

---

## Corpus atual (abr/2026)

**Internacional:** AI Act UE
**Federal vigente:** LGPD, ECA Digital (Lei 15.211/2025), NR-1
**Federal tramitando:** PL 2338, PL 4/2025, PL 4675/2025,
  PLP 152/2025, PLP 74/2026, PL 278/2026
**Apensados PL 2338:** identidade digital, vieses, escrita humana,
  autoral IA, Selo Conteúdo Sintético, saúde mental, marca d'água
**Estadual:** Paraná (Lei 22.324/2024), Pará (vazio)
**Produto:** Et Alii Advisory, Tech, Academy

---

## Modelo de serviço

- **LexGraph Diagnóstico**: relatório estático por perfil de empresa
- **LexWatch Monitor**: atualização mensal automática (assinatura)
- **LexGraph API**: endpoint para integração B2B (Hubstry CaaS)

---

*Instância proprietária. Core IPII: Hubstry Deep Tech.*
*Produto: Gonçalves et Alii — https://goncalvesetalii.github.io*
