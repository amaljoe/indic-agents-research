# MorphTok: Morphologically Grounded Tokenization for Indian Languages

**Authors:** Siddhant Mahurkar, Raviraj Joshi

**Venue:** arXiv (2025)

**ArXiv:** [2504.10335](https://arxiv.org/abs/2504.10335)

---

## Abstract Summary

MorphTok proposes morphology-aware pre-tokenization for Indian languages as a preprocessing step before standard BPE. For Hindi and Marathi, it implements **sandhi splitting** — the process of separating morphologically fused word junctions that are common in Sanskrit-derived Indic languages. It also introduces **Constrained BPE (CBPE)** that prevents BPE merges from crossing morpheme boundaries, ensuring that dependent vowels (matras) in Devanagari script are kept with their base consonants. The approach achieves 1.68% reduction in fertility scores (tokens per word) with improved downstream performance on MT and language modeling.

---

## Key Contributions

- **Sandhi splitting**: Pre-tokenization that separates Sanskrit-derived morpheme fusions in Hindi/Marathi
- **Constrained BPE (CBPE)**: Morpheme-boundary-aware BPE preventing linguistically invalid merges
- **Fertility reduction**: 1.68% fewer tokens per word compared to standard BPE
- **Downstream improvement**: Better MT and LM task performance with morphologically faithful tokens
- **Script-aware**: Handles Devanagari script's dependent vowel system correctly

---

## Relevance to indic-agents

Addresses the **morphological tokenization gap** identified in the indic-agents project. Poor tokenization of Indic scripts inflates token counts, degrades semantic understanding, and wastes context window budget in agent memory. MorphTok's CBPE approach is directly applicable to improving tokenization quality in the project's vLLM inference stack.
