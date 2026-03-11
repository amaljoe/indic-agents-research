# Multilingual Retrieval Augmented Generation for Culturally-Sensitive Tasks

**Authors:** Bryan Li, Fiona Luo, Samar Haider, Adwait Agashe, Tammy Li, Runqi Liu, Muqing Miao, Shriya Ramakrishnan, Yuan Yuan, Chris Callison-Burch

**Venue:** arXiv preprint (under review)

**ArXiv:** [2410.01171](https://arxiv.org/abs/2410.01171)

---

## Abstract Summary

This paper introduces **BordIRLines**, a dataset of territorial disputes with Wikipedia documents across 49 languages, designed to benchmark cross-lingual robustness in culturally-sensitive RAG scenarios. The study finds that retrieving multilingual documents — even when they may contain contradictory national perspectives — improves response consistency and decreases geopolitical bias compared to purely monolingual retrieval. The work highlights that factual disagreement across languages in culturally-sensitive topics is itself a form of cultural information that RAG systems should surface rather than flatten.

---

## Key Contributions

- **BordIRLines dataset**: 49-language dataset on territorial disputes for culturally-aware RAG evaluation
- **Multilingual retrieval advantage**: Cross-lingual document retrieval reduces geopolitical bias
- **Cultural consistency metric**: New metric measuring consistency of LLM responses across query languages
- **Bias analysis**: Shows English-only RAG amplifies Western geopolitical perspectives

---

## Relevance to indic-agents

Directly relevant to the project's concern about **behavioral drift toward dominant languages**. In healthcare, legal, and civic domains for Indic agents, culturally-sensitive retrieval is critical — this paper provides a framework for evaluating whether Indic knowledge is fairly represented in RAG-augmented responses.
