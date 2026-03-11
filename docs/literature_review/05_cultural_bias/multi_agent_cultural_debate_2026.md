# Mitigating Cultural Bias in LLMs via Multi-Agent Cultural Debate

**Authors:** Tan et al.

**Venue:** arXiv (2026, cited in indic-agents presentation)

**ArXiv:** [2601.12091](https://arxiv.org/abs/2601.12091)

---

## Abstract Summary

This paper proposes a **training-free multi-agent framework** for mitigating cultural bias in LLMs. Multiple agents are assigned distinct cultural personas (Western, East Asian, African, Middle Eastern, South Asian) and engage in structured debate using a "Seeking Common Ground while Reserving Differences" (SCGRD) strategy. The debate resolves cultural disagreements through iterative deliberation rather than forcing consensus. Evaluated on CEBiasBench, the framework achieves a 57.6% average No Bias Rate compared to 47.6% for the single-agent baseline — a 10 percentage-point improvement without any fine-tuning.

---

## Key Contributions

- **Training-free**: No model updates required — pure prompting/multi-agent architecture
- **5 cultural personas**: Western, East Asian, African, Middle Eastern, South Asian
- **SCGRD debate strategy**: Structured debate that preserves cultural nuance rather than collapsing to majority view
- **South Asian persona**: Explicitly represents South Asian cultural values in the agent pool
- **CEBiasBench evaluation**: Systematic cultural bias benchmark with diverse question types

---

## Relevance to indic-agents

**Directly cited** in the indic-agents presentation (Tan et al. 2026). The South Asian cultural persona and the SCGRD debate strategy are immediately applicable to the project's multi-agent architecture. This framework can be deployed as a cultural alignment layer over any Indic agent to prevent majority-culture bias without retraining.
