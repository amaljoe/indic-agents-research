# Retrieval-Augmented Generation in Multilingual Settings

**Authors:** Nadezhda Chirkova, David Rau, Hervé Déjean, Thibault Formal, Stéphane Clinchant, Vassilina Nikoulina

**Venue:** ACL 2024 (KnowLLM Workshop)

**ArXiv:** [2407.01463](https://arxiv.org/abs/2407.01463)

---

## Abstract Summary

This study investigates RAG pipelines where both queries and knowledge datastores span 13 languages. Despite the availability of high-quality multilingual retrievers (mDPR, mContriever) and multilingual generators (mT5, BLOOM), the system fails to reliably generate responses in the user's query language — the model defaults to English or the document language. The paper finds that task-specific prompt engineering (explicit language instructions) is necessary and partially sufficient to enforce response language consistency. It also shows that in-language retrieval generally outperforms cross-lingual retrieval when the datastore contains in-language documents.

---

## Key Contributions

- **13-language RAG evaluation**: Covers European, Asian, and African languages
- **Language consistency failure**: Documents the tendency of LLMs to ignore query language in RAG generation
- **Prompt engineering solutions**: Language-explicit prompts improve response language consistency by ~25%
- **Retrieval strategy comparison**: In-language vs. cross-lingual vs. English-pivot retrieval tradeoffs

---

## Relevance to indic-agents

The findings on language consistency failures directly apply to Indic agents — a Hindi-speaking user querying an agent backed by an English knowledge base may get English responses. The prompt engineering strategies and retrieval patterns explored here inform the project's context engineering layer.
