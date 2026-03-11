# Democratizing LLMs for Low-Resource Languages by Leveraging their English Dominant Abilities with Linguistically-Diverse Prompts

**Authors:** Xuan-Phi Nguyen, Mahani Aljunied, Shafiq Joty, Lidong Bing

**Venue:** ACL 2024 (Long Papers)

**ArXiv:** [2306.11372](https://arxiv.org/abs/2306.11372)

---

## Abstract Summary

This paper proposes a two-stage prompting strategy for enabling LLMs to perform well on low-resource languages without fine-tuning. First, it assembles synthetic in-context exemplars from a **linguistically-diverse set of high-resource languages** to guide the LLM toward an English pivot translation. Second, it uses the pivot to construct intra-lingual exemplars for the target low-resource language task. The method performs on par with supervised few-shot learning on 13 Indic languages and 21 African languages across classification, QA, and generation tasks — without any model updates.

---

## Key Contributions

- **Zero-shot cross-lingual prompting**: No fine-tuning required for low-resource language tasks
- **English-pivot technique**: Uses LLM's English strength as a bridge to low-resource languages
- **Linguistically-diverse exemplars**: Sampling from typologically varied high-resource languages reduces over-reliance on any single pivot
- **Broad coverage**: Validated on 13 Indic + 21 African low-resource languages

---

## Relevance to indic-agents

Highly relevant to the project's **synthetic reasoning augmentation** research direction. For Indic agents deployed without language-specific fine-tuning (e.g., early deployment phases), this prompting technique enables functional performance on low-resource languages via English-pivot chain-of-thought.
