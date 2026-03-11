# Knowledge-to-Verification (K2V): Unlocking RLVR for Knowledge-Intensive Domains

**Authors:** Zhonghang Yuan, Zhefan Wang, Fang Hu, Zihong Chen, Huanjun Kong, Songyang Zhang, Wanli Ouyang, Nanqing Dong

**Venue:** ICLR 2026 (submitted; OpenReview)

**ArXiv / OpenReview:** [OpenReview: EVS7SeKBqI](https://openreview.net/forum?id=EVS7SeKBqI)

---

## Abstract Summary

DeepSeek-R1-style RLVR is highly effective for tasks with unambiguous final-answer verifiability (mathematics, code), but struggles in knowledge-intensive domains where verification requires multi-hop factual reasoning rather than a single checkable answer. K2V addresses this by constructing knowledge graphs from domain text and framing verification as knowledge graph completion — enabling dense, intermediate reward signals across the reasoning chain rather than only terminal outcome rewards. The system automatically generates verifiable reward checkpoints by traversing knowledge graph edges, providing training signal at each reasoning step that links to a document-grounded fact. Applied to knowledge-intensive QA benchmarks, K2V maintains training stability while substantially outperforming outcome-only RLVR in domains where final answer extraction is ambiguous.

---

## Key Contributions

- **Knowledge graph as reward scaffold**: Converts unstructured domain knowledge into a verifiable reward structure without human annotation of reasoning chains
- **Dense intermediate rewards**: Knowledge graph traversal provides a reward signal at each reasoning step — addresses the sparse reward problem in multi-hop knowledge reasoning
- **Domain generalization of RLVR**: Extends RLVR beyond math/code to any domain where a knowledge graph can be automatically constructed
- **Training stability**: Dense rewards from KG completion reduce variance in GRPO training compared to sparse terminal rewards

---

## Relevance to indic-agents

Directly relevant to **R2 (synthetic reasoning augmentation)** and the emergent Indic CoT sub-direction. Indic-language question answering (MILU, IndicGenBench, IndicParam) is inherently knowledge-intensive — questions about Kerala history, Dravidian literature, or regional legal procedures require multi-hop factual reasoning that cannot be verified by a single answer extraction. The K2V framework provides the mechanism to construct dense RLVR rewards for these tasks: build a knowledge graph from SCERT textbook content or Kerala government scheme documents, then use graph completion as the verifiable reward. This resolves the main technical obstacle to applying RLVR to Indic knowledge-intensive QA (Use Cases 2 and 4 in the Malayalam deployment roadmap).
