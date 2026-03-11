# Memory-R1: Enhancing LLM Agents to Manage and Utilize Memories via Reinforcement Learning

**Authors:** Sikuan Yan, Xiufeng Yang, Zuchao Huang, Ercong Nie, Zifeng Ding, Zongyi Li, Xiaowen Ma, Hinrich Schütze, Volker Tresp, Yunpu Ma

**Venue:** arXiv 2025

**ArXiv:** [2508.19828](https://arxiv.org/abs/2508.19828)

---

## Abstract Summary

Memory-R1 presents an RL-based training framework for LLM agents to learn structured memory management from minimal supervision. The system introduces two cooperating agents: a Memory Manager that learns to perform structured ADD, UPDATE, and DELETE operations on a memory store, and an Answer Agent that distills and applies stored memories to answer questions. Both agents are trained jointly using PPO and GRPO with outcome-driven rewards — specifically, retrieval accuracy and answer correctness on downstream tasks. Evaluated on the LOCOMO long-term conversation benchmark, Memory-R1 achieves strong performance with only 152 training examples, demonstrating exceptional sample efficiency. The paper shows that structured memory operations emerge from RL training on retrieval outcomes, without any annotation of what operations should be performed or when.

---

## Key Contributions

- **Structured memory operations via RLVR**: ADD, UPDATE, DELETE memory operations emerge from retrieval accuracy rewards — not from supervised annotation of when to perform each operation
- **Dual-agent architecture**: Separates memory management (Memory Manager) from response generation (Answer Agent) — each trained with appropriate reward signals
- **Extreme sample efficiency**: 152 training examples sufficient for learning structured memory management — relevant for low-resource Indic language settings
- **Memory distillation**: The Answer Agent learns to compress and apply memory summaries rather than operating on raw memory stores — reduces context length pressure

---

## Relevance to indic-agents

The most directly relevant RLVR paper for **R3 (dynamic on-read/on-write memory management)**. The ADD/UPDATE/DELETE framework maps exactly onto the memory operations needed in indic-agents, and the GRPO training approach (outcome reward = retrieval correctness) is the template for extending to cross-lingual memory operations (Gap G4). The key extension this project proposes: adding a cross-lingual LINK operation, with verifiable reward defined as correct retrieval across language boundaries using Samanantar parallel corpus pairs as ground truth.
