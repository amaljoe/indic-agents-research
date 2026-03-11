# WISE: Rethinking the Knowledge Memory for Lifelong Model Editing of Large Language Models

**Authors:** Peng Wang, Zexi Li, Ningyu Zhang, Ziwen Xu, Yunzhi Yao, Yong Jiang, Pengjun Xie, Fei Huang, Huajun Chen

**Venue:** NeurIPS 2024 (Poster)

**ArXiv:** [2405.14768](https://arxiv.org/abs/2405.14768)

---

## Abstract Summary

WISE addresses the challenge of continual knowledge editing in LLMs without catastrophic forgetting of previously edited facts. It proposes a **dual parametric memory scheme**: a frozen main memory (pretrained weights) and a flexible side memory (for edited knowledge). A knowledge-sharding mechanism ensures that different edits reside in distinct subspaces within the side memory, preventing edit conflicts during lifelong updating. Experiments show WISE significantly outperforms prior editing methods in multi-edit settings while preserving general model capabilities.

---

## Key Contributions

- **Dual parametric memory**: Separation of pretrained (main) and edited (side) knowledge stores
- **Knowledge sharding**: Edits mapped to distinct subspaces preventing write conflicts
- **Lifelong editing support**: Handles sequential edits without degrading earlier edits
- **Locality preservation**: Maintains factual recall on unedited knowledge throughout editing process

---

## Relevance to indic-agents

Maps to the project's **parameterized internal memory** component. For Indic agents that may need language-specific knowledge updates (e.g., new dialect terms, cultural facts), WISE's dual-memory scheme provides a blueprint for non-destructive knowledge injection into multilingual models.
