# Process Reward Models That Think

**Authors:** Muhammad Khalifa, Rishabh Agarwal, Lajanugen Logeswaran, Jaekyeom Kim, Hao Peng, Moontae Lee, Honglak Lee, Lu Wang

**Venue:** ICLR 2025

**ArXiv:** [2504.16828](https://arxiv.org/abs/2504.16828)

---

## Abstract Summary

Standard process reward models (PRMs) assign scalar scores to intermediate reasoning steps but do so without any explicit reasoning about why a step is correct or incorrect. This paper introduces "thinking PRMs" — reward models that generate a chain-of-thought verification before producing a reward signal, enabling more discriminative assessment of intermediate solution steps. By allowing the PRM to "think through" its evaluation, the model better identifies subtle errors in multi-step reasoning chains. Evaluated on mathematical reasoning benchmarks integrated with RLVR pipelines, thinking PRMs improve both accuracy of step-level reward assignment and overall solution quality. The paper demonstrates that the discriminative quality of process-level rewards directly limits the ceiling of RLVR training, making better PRMs a critical component of any RLVR system.

---

## Key Contributions

- **Reasoning-enhanced PRM**: PRMs augmented with chain-of-thought verification before scoring — improving granularity of step-level reward signals
- **PRM as a bottleneck insight**: Demonstrates that PRM quality, not just policy optimization, limits RLVR training ceiling — motivating investment in better reward model design
- **Scalable verification**: CoT-based PRM verification scales better than rule-based step checking for complex, multi-step problems
- **Integration with RLVR pipelines**: Demonstrates plug-in compatibility with standard GRPO and PPO training loops

---

## Relevance to indic-agents

Relevant to **R3 (dynamic memory management)** and the cultural compliance sub-direction of the RLVR proposal. The key insight — that process-level reward quality limits the training ceiling — directly applies to cultural compliance RLVR: a PRM-style checker that evaluates whether individual response steps comply with Indian cultural norms (rather than only the final response) would provide denser, more informative reward signals than a terminal outcome reward alone. For the India-CASA cultural compliance training loop, a thinking PRM adapted to evaluate Indic cultural norms at each response turn would be the most powerful implementation of the cultural RLVR sub-direction.
