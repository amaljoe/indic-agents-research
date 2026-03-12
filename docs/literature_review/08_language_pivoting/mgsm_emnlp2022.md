# Language Models are Multilingual Chain-of-Thought Reasoners

**Authors:** Shi, Suzgun, Freitag, Wang, Srivats, Vosoughi, Chung, Tay, Ruder, Zhou, Das, Wei

**Venue:** arXiv (cs.CL), October 2022 (EMNLP 2022 findings)

**ArXiv:** [2210.03057](https://arxiv.org/abs/2210.03057)

---

## Abstract Summary

This paper evaluates the multilingual reasoning capabilities of large language models by constructing the **Multilingual Grade School Math (MGSM)** benchmark — 250 grade-school math problems from GSM8K translated into ten typologically diverse languages. The study finds that chain-of-thought (CoT) prompting enables strong multilingual reasoning, with performance improving with model scale. Notably, models demonstrate surprisingly strong reasoning abilities even in underrepresented languages such as Bengali and Swahili. The work establishes that the choice of language for intermediate reasoning steps is a viable research dimension — models can reason in the language of the question rather than requiring an English pivot.

---

## Key Contributions

- **MGSM benchmark**: 250 math problems in 10 typologically diverse languages for evaluating multilingual CoT reasoning
- **Multilingual CoT viability**: Demonstrates that models can reason correctly in non-English languages without routing through English
- **Scale dependency**: Shows that multilingual CoT performance improves markedly with model scale
- **Low-resource reach**: Even underrepresented languages (Bengali, Swahili) support non-trivial CoT reasoning at sufficient model scale

---

## Relevance to indic-agents

This foundational benchmark establishes that CoT reasoning in the native language is viable, directly challenging the assumption that English-pivot reasoning is necessary for non-English tasks. For indic-agents, MGSM (specifically the Bengali subset) provides an evaluation baseline for **R2** (synthetic reasoning augmentation for cross-lingual text): if a reasoning model trained with RLVR is capable of CoT in Indic languages at all, MGSM-style benchmarks can measure it. The benchmark motivates the research question of whether native-language reasoning or English-pivot reasoning produces better outcomes for low-resource Indic language users.
