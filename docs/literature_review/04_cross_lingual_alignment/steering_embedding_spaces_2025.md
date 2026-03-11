# Steering into New Embedding Spaces: Analyzing Cross-Lingual Alignment Induced by Model Interventions in Multilingual Language Models

**Authors:** Sundar et al. (Apple Machine Learning Research)

**Venue:** ACL 2025 (cited as Sundar et al. 2025 in indic-agents presentation)

**ArXiv:** [2502.15639](https://arxiv.org/abs/2502.15639)

---

## Abstract Summary

This paper analyzes the effect of **model interventions** — activation steering, representation engineering, and LoRA fine-tuning — on the cross-lingual alignment of embedding spaces in multilingual LLMs. It shows that targeted interventions on intermediate layers can induce new cross-lingual alignment patterns without full retraining, providing a data-efficient alternative to traditional cross-lingual fine-tuning. The study evaluates interventions across mBERT, XLM-R, and LLaMA multilingual models, showing that middle-layer steering vectors are particularly effective at restructuring cross-lingual representation geometry.

---

## Key Contributions

- **Intervention-based alignment**: Shows model interventions (vs. fine-tuning) can reshape cross-lingual embeddings
- **Layer analysis**: Middle layers are most malleable for cross-lingual alignment steering
- **Steering vectors**: Data-efficient alternative to parallel-corpus fine-tuning for alignment
- **Representation geometry analysis**: Visualizes how interventions shift embedding space topology across languages

---

## Relevance to indic-agents

This paper is **directly cited** in the indic-agents presentation (Sundar et al. 2025). It underpins the project's use of steering vectors as a parameterized external memory mechanism — enabling Indic-specific representation alignment without costly full fine-tuning of the base model.
