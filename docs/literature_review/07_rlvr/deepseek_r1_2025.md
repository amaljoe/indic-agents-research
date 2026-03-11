# DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning

**Authors:** DeepSeek-AI

**Venue:** arXiv January 2025 (Nature 2025, Vol. 645, pp. 633–638)

**ArXiv:** [2501.12948](https://arxiv.org/abs/2501.12948)

---

## Abstract Summary

DeepSeek-R1 demonstrates that large language models can develop sophisticated reasoning capabilities — including self-reflection, verification, and dynamic strategy switching — through pure reinforcement learning without any human-annotated reasoning demonstrations. The paper introduces Group Relative Policy Optimization (GRPO), a variant of PPO that eliminates the need for a learned critic model, using a group of sampled responses to estimate relative advantages. Applied to mathematical and coding benchmarks, DeepSeek-R1 achieves 77.9% on AIME 2024 (matching OpenAI o1) and 96.3% on MATH-500, purely from outcome-based rewards. The key finding is that "aha moments" — where the model spontaneously begins to re-examine its reasoning — emerge as learned behaviors from the RLVR training signal alone.

---

## Key Contributions

- **GRPO (Group Relative Policy Optimization)**: Eliminates the critic model by computing advantages relative to a group of sampled rollouts — significantly more efficient than standard PPO for language model training
- **Emergent reasoning without supervision**: Sophisticated CoT behaviors (self-correction, step verification, strategy switching) emerge from outcome reward signals alone — no CoT annotation required
- **Cold-start training recipe**: Demonstrates that a small set of long-CoT examples helps RLVR training stability, but reasoning quality scales with RL training, not with the CoT seed data
- **Distillation findings**: Reasoning capabilities can be distilled from R1 into smaller models (1.5B–70B) while retaining most of the performance gain

---

## Relevance to indic-agents

Foundational for **R2 (synthetic reasoning augmentation)**. The central hypothesis of the RLVR proposal in this project — that native-language CoT emerges in Indic languages when RLVR is applied with answer correctness rewards on Indic-language benchmarks — is directly analogous to DeepSeek-R1's core finding. If the hypothesis holds, GRPO training on MILU/IndicGenBench would produce Indic-language reasoning chains without requiring any annotated CoT traces in Tamil, Malayalam, or Telugu — resolving Gap G3 (cross-lingual CoT) identified in the literature review.
