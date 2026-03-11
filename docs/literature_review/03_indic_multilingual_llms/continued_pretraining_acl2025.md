# Emergent Abilities of Large Language Models under Continued Pretraining for Language Adaptation

**Authors:** Zhihao Wang, Zhengyan Zhang, Yanqiao Zhu, and others

**Venue:** ACL 2025 (Long Papers)

**ArXiv:** [2506.00288](https://arxiv.org/abs/2506.00288)

---

## Abstract Summary

This paper investigates how continued pretraining (CPT) on low-resource languages leads to emergent downstream task capabilities, and what conditions enable or block this emergence. The central finding is that **including English in the CPT mix** — even at low proportions — is critical for emergent capabilities to arise in the target language. English-only CPT validation perplexity does not degrade, but removing English entirely prevents capability emergence. The paper also shows that model scale and CPT data diversity interact: larger models require less cross-lingual CPT data to achieve the same capability level.

---

## Key Contributions

- **English-in-mix finding**: English inclusion in CPT mix is necessary (not just beneficial) for capability emergence
- **Perplexity–capability decoupling**: CPT can lower target-language perplexity while failing to enable downstream tasks if English is excluded
- **Scale interaction**: Larger models need less cross-lingual CPT data for emergence
- **Practical CPT recipe**: Provides guidance on data mix ratios for low-resource language adaptation

---

## Relevance to indic-agents

Critical for the project's **effective knowledge assimilation** research direction. When fine-tuning base models for Indic language agents, this paper provides the CPT recipe — specifically the English-inclusion requirement — that enables emergent reasoning in target low-resource Indic languages.
