# Multilingual Instruction Tuning With Just a Pinch of Multilinguality

**Authors:** Uri Shaham, Jonathan Herzig, Roee Aharoni, Idan Szpektor, Reut Tsarfaty, Matan Gonen

**Venue:** ACL 2024 (Long Papers)

**ArXiv:** [2401.01854](https://arxiv.org/abs/2401.01854)

---

## Abstract Summary

This paper challenges the assumption that multilingual instruction tuning requires large multilingual instruction datasets. It demonstrates that incorporating as few as **40 multilingual examples** into an otherwise English-only instruction tuning set substantially improves multilingual instruction following — both for languages seen during tuning and unseen languages. The improvement holds across classification, generation, and reasoning tasks. This "pinch of multilinguality" effect suggests that multilingual generalization is an emergent property that requires only minimal cross-lingual supervision to unlock.

---

## Key Contributions

- **40-example threshold**: Empirically shows 40 multilingual examples suffice for meaningful cross-lingual generalization
- **Seen vs. unseen language generalization**: Improvements transfer to languages not present in the multilingual instruction data
- **Task coverage**: Validated on classification, generation, and multi-step reasoning tasks
- **Efficiency finding**: Removes the need for massive multilingual instruction datasets in practice

---

## Relevance to indic-agents

Critical for the project's fine-tuning strategy. When creating instruction-tuned agents for Indic languages, this paper justifies a **cost-efficient approach**: build a high-quality English instruction set and add a small Indic-language component rather than collecting full multilingual instruction data for each target language.
