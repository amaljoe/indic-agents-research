# Do Multilingual LLMs Think In English?

**Authors:** Schut, Gal, Farquhar

**Venue:** arXiv, February 2025

**ArXiv:** [2502.15603](https://arxiv.org/abs/2502.15603)

---

## Abstract Summary

This paper investigates whether multilingual LLMs internally reason in English regardless of the input or output language. Using logit lens analysis on French, German, Dutch, and Mandarin inputs, the authors show that models first emit representations close to English for semantically-loaded words before translating them into the target language. This implicit English-pivot behavior is confirmed through activation steering experiments: steering vectors computed in English are more effective than those computed in the input/output language. The result implies that English-centric internal representations are a structural property of current multilingual LLMs — not a deliberate design choice — creating transparency problems for non-English users.

---

## Key Contributions

- **Logit lens evidence**: Intermediate layer representations for non-English tokens are demonstrably closer to English representations than to the target language, especially for semantically-loaded words
- **Activation steering validation**: English-computed steering vectors transfer more effectively cross-lingually than target-language vectors
- **Transparency concern**: Users interacting in their native language are unaware that key decisions are being made via English-shaped representations
- **Implicit vs. explicit pivot**: Distinguishes between deliberate pivot strategies (e.g., PLUG) and this *unintended* implicit pivot — both result in English-mediated reasoning but with different controllability

---

## Relevance to indic-agents

This paper is critically relevant to **R3** (dynamic memory management and semantic drift) and **R2**. For Indic language agents, the finding means that even when a model appears to respond in Tamil or Kannada, its semantic decisions may have been made through English representations — a form of invisible cultural/linguistic drift. This has direct implications for memory systems: memories stored and retrieved via Indic-language queries may be silently re-interpreted through English representations, causing semantic distortion for concepts without direct English equivalents (especially culturally specific terms). The transparency problem identified here motivates explicit monitoring of representation geometry in indic-agents memory operations.
