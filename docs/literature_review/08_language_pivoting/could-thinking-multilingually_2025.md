# Could Thinking Multilingually Empower LLM Reasoning?

**Authors:** Gao, Huang, Zhu, Huang, Li, Yuan

**Venue:** arXiv, April 2025

**ArXiv:** [2504.11833](https://arxiv.org/abs/2504.11833)

---

## Abstract Summary

This paper challenges the dominant assumption that English-only reasoning maximizes LLM performance. Through systematic experiments, the authors find that non-English CoT responses frequently achieve higher accuracy than English ones, and that the best individual-language performance exceeds English-only performance by approximately 10 Acc@k points. The study investigates why current models fail to exploit this multilingual reasoning potential, identifying conventional answer selection methods as a key bottleneck: standard greedy decoding and majority voting over reasoning paths don't leverage multilingual diversity. The authors propose that unlocking multilingual reasoning — allowing models to reason in the most capable language for each step — could substantially improve overall performance.

---

## Key Contributions

- **Multilingual upper bound**: Demonstrates ~10 Acc@k point headroom over English-only reasoning by allowing optimal language selection
- **English bias critique**: Shows English is often *not* the best reasoning language for a given model and task
- **Answer selection bottleneck**: Identifies that current selection methods fail to leverage multilingual reasoning diversity
- **Robustness of multilingual gains**: Gains persist even under noisy translation, indicating the effect is not an artifact of translation quality

---

## Relevance to indic-agents

This paper directly motivates the language pivoting question for indic-agents: if English is not always the optimal reasoning language, then forcing an English pivot in low-resource Indic language settings may be actively harmful. For **R2** (synthetic reasoning augmentation), the 10-point headroom suggests that allowing agents to reason in whichever language they are most capable in — potentially Indic languages for culturally-specific knowledge — could meaningfully improve task accuracy. The bottleneck identified (answer selection over multilingual reasoning paths) also maps to **R3**: a memory system that stores reasoning traces in multiple languages and selects the best one at retrieval time is a concrete architectural implication.
