# A-MEM: Agentic Memory for LLM Agents

**Authors:** Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, Yongfeng Zhang

**Venue:** NeurIPS 2025 (Poster)

**ArXiv:** [2502.12110](https://arxiv.org/abs/2502.12110)

---

## Abstract Summary

A-MEM proposes a novel agentic memory system for LLM agents that dynamically organizes memories following Zettelkasten principles — a note-taking methodology that creates an interconnected knowledge network rather than a flat list. The system generates structured attributes for each memory (contextual descriptions, keywords, tags) and dynamically creates links between related memories. Upon storing a new memory, it analyzes existing memories and establishes semantic connections, enabling associative memory retrieval akin to human memory. Evaluated against SOTA baselines on six foundation models, A-MEM shows superior performance across memory-intensive agent tasks.

---

## Key Contributions

- **Zettelkasten-inspired dynamic indexing**: Moves beyond flat memory stores to a graph-like knowledge network
- **Structured attribute generation**: Automatically generates contextual descriptions, keywords, and tags per memory unit
- **Dynamic memory linking**: On write, creates semantic links to related existing memories for associative retrieval
- **Foundation model agnosticism**: Evaluated across six different LLMs, showing broad applicability

---

## Relevance to indic-agents

Directly addresses the **on-write memory management** challenge identified in the project — the mechanism for forming, linking, and evolving memory in agentic systems. The dynamic indexing approach is critical for multilingual agents that must manage memories across languages without fragmentation.
