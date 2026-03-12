# Think Natively: Unlocking Multilingual Reasoning with Consistency-Enhanced Reinforcement Learning

**Authors:** Zhang, Liang, Meng, Zhang, Huang, Chen, Xu, Zhou

**Venue:** arXiv, October 2025

**ArXiv:** [2510.07300](https://arxiv.org/abs/2510.07300)

---

## Abstract Summary

Large Reasoning Models (LRMs) trained with RLVR exhibit a strong English bias — they default to English-language chain-of-thought even when the input is in another language. This paper proposes M-Thinker, which uses two complementary RL reward signals to overcome this: a *language consistency reward* that penalizes language switching between input, reasoning chain, and answer; and a *cross-lingual reasoning transfer reward* that compares non-English reasoning paths against English ones, transferring reasoning quality across languages. M-Thinker models (1.5B/4B/7B) achieve near-complete language consistency and strong multilingual benchmark scores on MMATH and PolyMath, with generalization to unseen languages.

---

## Key Contributions

- **Language consistency reward**: RL signal specifically penalizing language switching in reasoning chains, enforcing native-language CoT
- **Cross-lingual reasoning transfer reward**: Distills English reasoning quality into non-English reasoning paths without requiring parallel reasoning annotations
- **M-Thinker models**: 1.5B–7B parameter models demonstrating near-100% language consistency with competitive reasoning accuracy
- **Unseen language generalization**: RL-trained consistency generalizes to languages not in the training set

---

## Relevance to indic-agents

This paper is one of the most directly relevant to the indic-agents RLVR research direction (**R2** and **R3**). It demonstrates that RLVR can be used not just for reasoning correctness but for *language behavior control* — specifically, preventing the English drift that Schut et al. (2025) identify as a structural problem. The language consistency reward is directly applicable to indic-agents: an agent that reasons internally in Kannada for a Kannada-speaking user will produce responses with better cultural and linguistic coherence than one that silently pivots through English. The cross-lingual reasoning transfer reward also provides a feasible training signal for low-resource Indic languages — bootstrapping from English reasoning quality without English pivot at inference time.
