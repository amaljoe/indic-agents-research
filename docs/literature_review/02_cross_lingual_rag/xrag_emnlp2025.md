# XRAG: Cross-lingual Retrieval-Augmented Generation

**Authors:** Wei Liu, Sony Trenous, Leonardo F. R. Ribeiro, Bill Byrne, Felix Hieber

**Venue:** EMNLP 2025 (Findings)

**ArXiv:** [2505.10089](https://arxiv.org/abs/2505.10089)

---

## Abstract Summary

XRAG introduces a benchmark for evaluating LLMs in cross-lingual RAG settings where the language of the user query differs from the language of retrieved documents. The benchmark uncovers two distinct challenges: (1) **response language correctness** in monolingual retrieval (the model must respond in the user's language despite retrieving in another), and (2) **cross-lingual reasoning** in multilingual retrieval (reasoning must span documents in multiple languages simultaneously). Experiments on multiple LLMs reveal significant performance drops in cross-lingual RAG compared to monolingual RAG, motivating targeted solutions.

---

## Key Contributions

- **Cross-lingual RAG benchmark**: First systematic evaluation of RAG across language mismatches
- **Two-failure-mode taxonomy**: Response language correctness vs. cross-lingual reasoning
- **LLM evaluation**: Benchmarks GPT-4, LLaMA, Mistral and others on cross-lingual RAG
- **Prompt engineering insights**: Identifies language instruction strategies that improve cross-lingual RAG

---

## Relevance to indic-agents

Central to the project's **cross-lingual retrieval challenge** — Indic agents will frequently face the scenario where knowledge bases are in English/Hindi while queries arrive in low-resource Indic languages. XRAG's failure taxonomy and evaluation methodology directly apply to the project's RAG pipeline design.
