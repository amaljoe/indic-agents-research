# PLUG: Leveraging Pivot Language in Cross-Lingual Instruction Tuning

**Authors:** Zhang, Lee, Fang, Yu, Jia, Jiang, Barbieri

**Venue:** ACL 2024

**ArXiv:** [2311.08711](https://arxiv.org/abs/2311.08711)

---

## Abstract Summary

PLUG proposes using a high-resource pivot language (primarily English) as an intermediate step during instruction tuning for lower-resource languages. Instead of directly training models to interpret instructions and respond in the target language, PLUG trains models to first understand instructions in the pivot language, then generate responses in the target language. The authors introduce X-AlpacaEval, a benchmark of instructions in Chinese, Korean, Italian, and Spanish annotated by professional translators. Results show approximately 29% average improvement in cross-lingual instruction-following compared to direct target-language baselines. The approach generalizes beyond English as the pivot, validating the pivot language paradigm more broadly.

---

## Key Contributions

- **PLUG method**: Two-stage processing — interpret instruction in pivot language, generate response in target language — improving instruction-following by ~29%
- **X-AlpacaEval benchmark**: Professional-translator-annotated instruction benchmark in 4 languages
- **Pivot generalization**: Demonstrates the approach works with non-English pivots, not just English
- **Instruction gap analysis**: Diagnoses why lower-resource languages underperform: imbalanced foundational abilities from pretraining, not inference-time reasoning failures

---

## Relevance to indic-agents

PLUG is the strongest empirical argument for language pivoting in the indic-agents context. For instruction-following tasks in low-resource Indic languages (where pretraining data is sparse), routing through English may genuinely improve response quality — directly relevant to **R1** (knowledge assimilation for differential-resource languages). However, the 29% gain is measured on European languages with moderate resource levels; the gain for extremely low-resource Indic languages may differ. The tension between PLUG (pro-pivot) and Think Natively / Do Multilingual LLMs Think In English (anti-pivot) is a key research question for the indic-agents R2 direction.
