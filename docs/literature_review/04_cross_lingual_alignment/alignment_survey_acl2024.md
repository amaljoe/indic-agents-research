# Understanding Cross-Lingual Alignment — A Survey

**Authors:** Yihong Liu, Haotian Ye, Chunlan Ma, Mingyang Wang, Hinrich Schütze

**Venue:** ACL 2024 (Findings)

**ArXiv:** [2404.06228](https://arxiv.org/abs/2404.06228)

---

## Abstract Summary

This survey covers 4 years (2019–2023) of research on improving cross-lingual alignment in multilingual language models. It provides a comprehensive taxonomy of techniques: training objectives (MLM, TLM, contrastive alignment), architecture innovations (shared encoders, language-neutral representations), contrastive fine-tuning on parallel data, and post-hoc embedding space adjustments (linear mapping, Procrustes alignment). A key finding is that maximizing cross-lingual alignment can paradoxically cause **wrong-language generation** in generative models — the model loses the ability to generate in the target language when pushed to align representations too strongly. This creates a fundamental alignment–generation trade-off.

---

## Key Contributions

- **4-year taxonomy**: Comprehensive classification of 100+ cross-lingual alignment papers (2019-2023)
- **Alignment–generation trade-off**: Documents the paradox where high alignment degrades language-specific generation
- **Method comparison**: Systematic comparison of training-time vs. post-hoc alignment techniques
- **Generative model coverage**: Unlike earlier surveys, includes decoder-only and seq2seq models
- **Research gap identification**: Points to multilingual reasoning alignment as an under-studied area

---

## Relevance to indic-agents

Directly informs the project's **semantic memory drift** challenge. When aligning multilingual embeddings in the agent's memory store, aggressive alignment can cause the agent to generate in the wrong language. This survey provides the theoretical grounding and mitigation strategies for this core project risk.
