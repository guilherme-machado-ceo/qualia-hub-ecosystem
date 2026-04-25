# LexScan — Engine de Compliance Normativo

**Instância IPII para domínio jurídico-regulatório**
**Status:** Especificação | **Produto:** Et Alii Tech

---

## Definição

LexScan é a instância da IPII para o domínio jurídico-regulatório.
Tokeniza textos legais em AST jurídica, indexa via LexMatrix 5D,
itera sobre corpus normativo comparando com o perfil da empresa,
detecta gaps de compliance e conflitos inter-normativos.

**Diferencial crítico:** matching semântico vs checklist estático
dos concorrentes. Detecta conflitos inter-normativos que nenhum
checklist consegue mapear (ex: NR-1 psicossocial + PL 2338 + LGPD
sobre o mesmo fenômeno — uso de IA em RH).

---

## Mapeamento nos 5 Eixos (LexMatrix 5D)

| Eixo GuruMatrix | Equivalente Jurídico |
|-----------------|---------------------|
| i — Categoria Ontológica | Tipo normativo: obrigação / proibição / sanção / prazo / direito |
| j — Campo do Conhecimento | Setor: trabalho / dados / IA / criança / infraestrutura |
| k — Nível Hermenêutico | Interpretação: literal / sistemático / teleológico / constitucional |
| t — Tempo de Execução | Vigência: imediata / prazo fixo / condicional / futura |
| l — Paradigma-Alvo | Âmbito: federal / estadual / municipal / setorial / internacional |

---

## Fluxo LexScan

```
INPUT: perfil da empresa + corpus normativo

1. INGESTÃO NORMATIVA
   Parser de PDFs, HTML de DOU, plaintext jurídico
   → AST jurídica (sujeito, conduta, objeto, sanção, prazo)

2. INDEXAÇÃO LEXMATRIX
   Cada obrigação → indexada nos 5 eixos
   → grafo normativo dimensional

3. ITERAÇÃO
   Para cada obrigação no corpus:
   → compara com perfil da empresa
   → calcula distância de conformidade
   → detecta sobreposições entre normas
   → detecta lacunas não cobertas

4. MATCHING CONTEXTUAL
   Aplica: lex posterior, lex specialis, lex superior

OUTPUT: relatório de compliance com gaps priorizados
```

---

## Corpus Normativo Inicial (2026)

- NR-1 Risco Psicossocial (Portaria MTE 1.419/2024)
- LGPD (Lei 13.709/2018)
- ECA Digital (Lei 15.211/2025)
- PL 2338/2023 — Marco Legal da IA (tramitando)
- PL 4/2025 — Livro VI Código Civil Digital (tramitando)
- REDATA PL 278/2026 (aguarda Senado)
- PL 4675/2025 — Mercados Digitais (tramitando)

---

## Produtos derivados (Et Alii Advisory)

- **LexScan Diagnóstico**: execução pontual, relatório de gaps
- **LexWatch Monitor**: assinatura, atualização automática
- **LexGraph API**: grafo interativo, B2B

---

*Instância proprietária. Core IPII: Hubstry Deep Tech.*
*Produto comercial: Gonçalves et Alii — https://goncalvesetalii.github.io*
