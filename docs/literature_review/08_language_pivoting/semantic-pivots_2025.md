# Semantic Pivots Enable Cross-Lingual Transfer in Large Language Models

**Authors:** He, Zhou, Chen, Qiu, Liu, Liu, Zhao

**Venue:** arXiv, May 2025

**ArXiv:** [2505.16385](https://arxiv.org/abs/2505.16385)

---

## Abstract Summary

This paper investigates the mechanism by which LLMs acquire cross-lingual transfer capabilities. The authors propose a Word-Level Cross-Lingual Translation Task to probe intermediate layer outputs and identify two distinct internal behaviors: *co-occurrence behavior* (leveraging word co-occurrence statistics from pretraining) and *semantic pivot behavior* (where English serves as a semantic bridge for cross-lingual transfer). They locate documents in pretraining datasets that trigger semantic pivot behavior and construct a training dataset that emphasizes high-proportion semantic pivot documents. Experiments show this targeted pre-training data reconstruction improves cross-lingual ability, offering both interpretability insights and a practical training improvement.

---

## Key Contributions

- **Two-behavior taxonomy**: Distinguishes co-occurrence behavior from semantic pivot behavior in LLM internals, with different implications for cross-lingual transfer
- **Word-level probing task**: A diagnostic method to identify which layers and tokens exhibit semantic pivot behavior
- **Training data attribution**: Locates specific pretraining documents responsible for semantic pivot capabilities
- **Data reconstruction improvement**: Reweighting pre-training data to emphasize semantic pivot documents measurably improves cross-lingual transfer

---

## Relevance to indic-agents

The semantic pivot mechanism identified here provides a mechanistic explanation for why English-pivot reasoning works: LLMs have internalized English as the semantic bridge during pretraining, and this is recoverable and improvable. For **R1** (knowledge assimilation), this suggests that the quality of cross-lingual transfer to Indic languages depends heavily on whether the pretraining data included documents with semantic pivot patterns for those languages — which it almost certainly did not for low-resource Indic languages. This motivates targeted data curation for Indic CPT that specifically includes bilingual documents with semantic pivot structure. The probing methodology could also be adapted to measure cross-lingual memory alignment quality in **R3**.
