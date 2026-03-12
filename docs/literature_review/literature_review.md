# Literature Review: Agentic Memory for Sovereign Indic AI Agents

**Project:** indic-agents — IIT Bombay
**Review Date:** March 2026
**Scope:** 28 papers from top-tier venues (ACL, EMNLP, NeurIPS, NAACL, ICLR, IJCNLP) across 8 thematic areas
**BibTeX:** [references.bib](references.bib)

---

## 1. Introduction

The **indic-agents** project aims to build agentic memory systems for sovereign AI agents operating in Indian language contexts. India's linguistic landscape comprises 22 scheduled languages, 650+ dialects, and communities with varying degrees of NLP resource availability. Deploying functional AI agents in this context requires solving four intersecting challenges:

1. **Memory architecture** — agents must retain, update, and retrieve knowledge across multilingual contexts without semantic drift
2. **Cross-lingual retrieval** — knowledge bases are predominantly English-dominant while queries arrive in Indic languages
3. **Cultural alignment** — agents must reflect local cultural values rather than defaulting to Western or Hindi-majority norms
4. **Tokenization fidelity** — morphologically complex Indic scripts are systematically under-served by standard tokenizers

This review surveys the state of the art across all four challenges, organized into six thematic sections. Each section synthesizes key papers, identifies convergent findings, and maps them to the project's three research directions:

> **R1** — Effective knowledge assimilation for differential-resource languages
> **R2** — Synthetic reasoning augmentation for cross-lingual text
> **R3** — Dynamic on-read/on-write memory management for multilingual alignment and drift

---

## 2. LLM Agent Memory Architectures

### Papers Reviewed
| Paper | Venue | Key Contribution |
|-------|-------|-----------------|
| [A-MEM: Agentic Memory for LLM Agents](01_agent_memory/a-mem_neurips2025.md) | NeurIPS 2025 | Zettelkasten-style dynamic memory indexing and linking |
| [Memory in the Age of AI Agents: A Survey](01_agent_memory/memory_survey_2025.md) | arXiv 2025 | Unified taxonomy: forms, functions, dynamics |
| [WISE: Lifelong Model Editing](01_agent_memory/wise_neurips2024.md) | NeurIPS 2024 | Dual parametric memory with knowledge sharding |

### Synthesis

Agent memory has matured into a multi-dimensional research area. The survey by Hu et al. (2025) establishes a three-axis taxonomy: **forms** (token-level, parametric, latent), **functions** (factual, experiential, working), and **dynamics** (formation, evolution, retrieval). This taxonomy maps directly onto the indic-agents architecture:

- **Token-level memory** → in-context agent history (textual memory layer)
- **Parametric memory** → fine-tuned adapters and model edits (parameterized internal memory)
- **Latent memory** → vector-DB retrieval stores (parameterized external memory)

**A-MEM** (Xu et al., NeurIPS 2025) addresses the critical gap of *memory organization*. Prior systems store memories as flat lists; A-MEM uses Zettelkasten-style linking where each stored memory generates structured attributes (keywords, tags, contextual descriptions) and dynamically links to related existing memories. This associative structure is essential for multilingual agents where the same semantic concept may be stored in different languages — links prevent memory fragmentation across language boundaries.

**WISE** (Wang et al., NeurIPS 2024) targets parametric memory specifically: how to edit a model's knowledge without overwriting earlier edits (catastrophic forgetting). Its dual-memory scheme — frozen pretrained weights + flexible side memory with knowledge sharding — provides the blueprint for language-specific knowledge injection into Indic agents. A dialect-specific medical term or a state-specific legal fact can be injected into the side memory without disrupting the model's general capabilities.

**Convergent finding:** Dynamic memory organization (A-MEM) and non-destructive parametric editing (WISE) together address **R3** — the on-write memory management challenge is a combination of structural organization (how memories are linked) and edit isolation (how parametric updates are scoped).

---

## 3. Cross-Lingual Retrieval-Augmented Generation

### Papers Reviewed
| Paper | Venue | Key Contribution |
|-------|-------|-----------------|
| [XRAG: Cross-lingual RAG](02_cross_lingual_rag/xrag_emnlp2025.md) | EMNLP 2025 | Benchmark for query-document language mismatch |
| [Multilingual RAG for Culturally-Sensitive Tasks](02_cross_lingual_rag/multilingual_rag_culturally_sensitive.md) | arXiv 2024 | Multilingual retrieval reduces geopolitical bias |
| [RAG in Multilingual Settings](02_cross_lingual_rag/rag_multilingual_acl2024.md) | ACL 2024 | Language consistency failures and prompt mitigations |

### Synthesis

The indic-agents project's RAG pipeline faces a fundamental mismatch: user queries arrive in Indic languages, but most knowledge bases are English-dominant. This **cross-lingual RAG** challenge has received dedicated study only recently.

**XRAG** (Liu et al., EMNLP 2025) is the most direct prior work, providing the first systematic taxonomy of cross-lingual RAG failures. It identifies two distinct modes: (1) *response language correctness* — the model generates in the wrong language despite being queried in the user's language — and (2) *cross-lingual reasoning* — the model cannot reason coherently across documents in different languages. For Indic agents, mode (1) is the immediate deployment risk (a rural healthcare agent responding in English to a Hindi query) while mode (2) is the harder research challenge.

**Chirkova et al.** (ACL 2024) demonstrate that these failures persist even with high-quality multilingual retrievers and generators, and that task-specific prompt engineering (explicit "respond in [LANGUAGE]" instructions) is a necessary, though partial, fix. This motivates the project's context engineering layer as a non-trivial component, not a thin wrapper.

**BordIRLines** (Li et al., 2024) introduces an important equity perspective: multilingual retrieval doesn't just improve accuracy — it reduces *bias*. Retrieving documents only from English-language sources systematically skews responses toward Western perspectives on contested topics. For Indic agents covering legal, civic, and historical domains, retrieving from multilingual Indic sources is essential for culturally-fair responses.

**Convergent finding:** Cross-lingual RAG requires both infrastructure (multilingual retrieval and generation) and policy (language-explicit prompting, multilingual source inclusion). Both must be part of the indic-agents memory retrieval design, addressing **R1** and **R2**.

---

## 4. Multilingual LLMs and Indic Languages

### Papers Reviewed
| Paper | Venue | Key Contribution |
|-------|-------|-----------------|
| [IndicGenBench](03_indic_multilingual_llms/indicgenbench_acl2024.md) | ACL 2024 | 29 Indic languages generation benchmark |
| [IndicParam](03_indic_multilingual_llms/indicparam_2024.md) | arXiv 2024 | 11 low-resource Indic languages benchmark |
| [Bhaasha Survey](03_indic_multilingual_llms/bhaasha_survey_emnlp2025.md) | EMNLP 2025 | 650+ South Asian language landscape survey |
| [Democratizing LLMs](03_indic_multilingual_llms/democratizing_llms_acl2024.md) | ACL 2024 | Low-resource LLMs via linguistically-diverse prompting |
| [Emergent Abilities via CPT](03_indic_multilingual_llms/continued_pretraining_acl2025.md) | ACL 2025 | English-inclusive CPT required for emergence |

### Synthesis

The landscape of Indic NLP is starkly uneven. **Poria & Huang** (EMNLP 2025) document this comprehensively: Indo-Aryan languages (Hindi, Bengali, Gujarati, Marathi) have reasonable NLP infrastructure, while Tibeto-Burman (Manipuri, Bodo) and Austroasiatic (Santali) languages have almost no modern NLP resources. The indic-agents project must explicitly account for this disparity in its language roadmap.

**IndicGenBench** (Singh et al., ACL 2024) provides the evaluation infrastructure for 29 Indic languages across four generation tasks. Its consistent finding is that even frontier models (GPT-4) underperform significantly on low-resource Indic languages, especially for generation tasks requiring morphological fidelity (translation, dialogue). **IndicParam** extends this to 11 specifically low-resource languages, showing that the best model achieves only 58% accuracy — underscoring that current LLMs are not production-ready for many Indic language communities.

Two papers address how to improve LLM performance on low-resource Indic languages. **Nguyen et al.** (ACL 2024) show that LLMs can be prompted into low-resource language performance without fine-tuning by routing through an English pivot using linguistically-diverse exemplars — directly applicable to the project's synthetic reasoning augmentation direction (**R2**). **Wang et al.** (ACL 2025) show that continued pretraining (CPT) on low-resource language data enables emergent task capabilities, but only if English is included in the CPT data mix. Removing English prevents capability emergence even when target-language perplexity improves — a practical constraint for **R1** knowledge assimilation strategies.

**Convergent finding:** A two-tier strategy is appropriate for indic-agents: (1) for higher-resource Indic languages, fine-tuning with English-inclusive CPT following Wang et al.; (2) for extremely low-resource languages, the prompting strategy of Nguyen et al. using English-pivot reasoning.

---

## 5. Cross-Lingual Alignment

### Papers Reviewed
| Paper | Venue | Key Contribution |
|-------|-------|-----------------|
| [Cross-Lingual Alignment Survey](04_cross_lingual_alignment/alignment_survey_acl2024.md) | ACL 2024 | Taxonomy of alignment techniques 2019-2023 |
| [Steering into New Embedding Spaces](04_cross_lingual_alignment/steering_embedding_spaces_2025.md) | ACL 2025 | Steering vectors for data-efficient alignment |
| [Multilingual Instruction Tuning](04_cross_lingual_alignment/multilingual_instruction_tuning.md) | ACL 2024 | 40 examples suffice for cross-lingual generalization |

### Synthesis

Cross-lingual alignment — ensuring that semantically equivalent content in different languages maps to similar representations — is foundational to the indic-agents memory system. The **Liu et al. survey** (ACL 2024) provides the theoretical grounding, revealing a key paradox: maximizing representational alignment can cause *wrong-language generation*, where the model loses the ability to produce text in the target language. This alignment–generation trade-off means aggressive alignment of Indic language representations in the memory store could cause agents to generate in Hindi or English instead of the user's language.

**Sundar et al.** (ACL 2025) — directly cited in the indic-agents presentation — propose a resolution: **steering vectors** applied to intermediate model layers can reshape cross-lingual embedding geometry without full retraining. This is more data-efficient than parallel-corpus fine-tuning and avoids the alignment-generation trade-off because it targets specific layers rather than globally aligning all representations. This finding directly enables the project's parameterized external memory (steering vectors as adapters).

**Shaham et al.** (ACL 2024) provide a critical practical result: as few as 40 multilingual instruction examples added to an English instruction set significantly improves cross-lingual instruction following, including for languages not present in the multilingual examples. This severely reduces the data collection burden for the project — a small, high-quality Indic instruction set paired with an English-dominant instruction corpus is sufficient.

**Convergent finding:** The path to aligned multilingual Indic agents is: (1) steering-vector-based representation alignment for the embedding space (**R3**), combined with (2) minimal multilingual instruction tuning (40-example "pinch") for instruction following (**R1**). These are complementary and feasible.

---

## 6. Cultural Bias in LLMs

### Papers Reviewed
| Paper | Venue | Key Contribution |
|-------|-------|-----------------|
| [CultureLLM](05_cultural_bias/culturellm_neurips2024.md) | NeurIPS 2024 | WVS-based cultural fine-tuning for 9 cultures |
| [Multi-Agent Cultural Debate](05_cultural_bias/multi_agent_cultural_debate_2026.md) | arXiv 2026 | Training-free cultural bias mitigation via agent debate |
| [CASA Benchmark](05_cultural_bias/casa_benchmark_naacl2025.md) | NAACL 2025 | Cultural/social awareness benchmark for LLM agents |

### Synthesis

Cultural alignment is the least technically mature but arguably most socially critical component of the indic-agents project. Current LLMs exhibit strong Western cultural bias — as measured by the CASA benchmark (Qiu et al., NAACL 2025), agents violate cultural norms more than 40% of the time, with less than 10% cultural awareness coverage. For the project's healthcare, legal, and civic agent use cases, this is not an abstract concern: culturally-inappropriate agent behavior can cause real harm.

**CultureLLM** (Li et al., NeurIPS 2024) demonstrates that systematic cultural fine-tuning using World Values Survey data is effective. Critically, Bengali (a major South Asian language) is included in their 9-culture study, providing a direct model for extending the approach to Hindi, Tamil, Kannada, and other Indic languages. The semantic data augmentation technique they propose can be applied to India-specific cultural surveys (National Family Health Survey, ASER data) to generate training data.

**Tan et al.** (arXiv 2026) — directly cited in the indic-agents presentation — offer a training-free alternative: assign agents distinct cultural personas (explicitly including South Asian) and use a structured debate protocol (SCGRD) to resolve cultural disagreements. This is deployable immediately, without cultural fine-tuning data, making it suitable for early agent versions or for use cases where fine-tuning is infeasible.

**CASA** (Qiu et al., NAACL 2025) provides the evaluation methodology. Adapting the CASA benchmark to Indian cultural norms (adapting shopping and forum scenarios to Indian e-commerce and social media contexts) would give the indic-agents project a concrete metric for tracking cultural safety across deployment.

**Convergent finding:** A two-phase approach is optimal for cultural alignment in indic-agents: deploy the Tan et al. multi-agent cultural debate immediately for cultural safety guardrails, while collecting Indic cultural survey data to enable CultureLLM-style fine-tuning in later project phases.

---

## 7. Morphological Tokenization for Indic Languages

### Papers Reviewed
| Paper | Venue | Key Contribution |
|-------|-------|-----------------|
| [MorphTok](06_morphological_tokenization/morphtok_2025.md) | arXiv 2025 | Sandhi splitting + Constrained BPE for Devanagari |
| [Multilingual Tokenization: Indian Languages](06_morphological_tokenization/multilingual_tokenization_indic.md) | arXiv 2025 | 17-language tokenization evaluation and recommendations |

### Synthesis

Tokenization is the most foundational yet most underappreciated challenge in Indic NLP. Indic languages are morphologically rich and agglutinative — a single Kannada word may encode what English expresses in an entire clause. Standard BPE tokenizers, trained predominantly on English, systematically over-segment Indic scripts, leading to higher token counts per word (higher *fertility*) and loss of morphological structure.

**Mahurkar & Joshi** (MorphTok, arXiv 2025) quantify and address this for Hindi and Marathi: standard BPE incorrectly merges across morpheme boundaries (e.g., treating a sandhi junction as a single token), while their Constrained BPE prevents this. The 1.68% fertility reduction translates directly to reduced inference cost and better downstream task performance. For an agent running millions of inferences, this is both a quality and cost improvement.

**Karthika et al.** (arXiv 2025) extend this analysis to 17 Indian languages. Their key finding — that low-resource Indic languages benefit from tokenizers trained on related high-resource languages — justifies a family-based tokenizer strategy: a tokenizer trained on Hindi/Bengali/Gujarati (Indo-Aryan family) should be reused for closely related low-resource languages rather than training a from-scratch tokenizer on insufficient data.

**Convergent finding:** The indic-agents vLLM inference stack should adopt MorphTok-style constrained tokenization for the Devanagari-script languages in its initial deployment, and use related-language tokenizer transfer for low-resource Indic languages in other script families. This addresses the **tokenization inequality** that creates latency disparities between Indic language users and English users.

---

## 8. Reinforcement Learning with Verifiable Rewards (RLVR)

### Papers Reviewed
| Paper | Venue | Key Contribution |
|-------|-------|-----------------|
| [DeepSeek-R1](07_rlvr/deepseek_r1_2025.md) | arXiv / Nature 2025 | GRPO training; emergent CoT reasoning from outcome rewards alone |
| [Memory-R1](07_rlvr/memory_r1_2025.md) | arXiv 2025 | GRPO for agent memory ops (ADD/UPDATE/DELETE); 152-example sample efficiency |
| [Process Reward Models That Think](07_rlvr/prm_think_iclr2025.md) | ICLR 2025 | CoT-enhanced PRM for step-level verification; PRM quality limits RLVR ceiling |
| [Knowledge-to-Verification (K2V)](07_rlvr/k2v_iclr2026.md) | ICLR 2026 | Knowledge graph as verifiable reward scaffold for knowledge-intensive domains |

### Synthesis

RLVR has emerged as the most significant training paradigm shift in LLM research since instruction tuning. The core insight — crystallized in DeepSeek-R1 (arXiv:2501.12948) — is that sophisticated reasoning behaviors emerge spontaneously when models are trained with outcome-based rewards on verifiable tasks, without any supervision of intermediate reasoning steps. Group Relative Policy Optimization (GRPO) makes this tractable at scale by eliminating the learned critic model, instead computing advantages relative to a group of sampled rollouts.

**Memory-R1** (Yan et al., 2025) demonstrates that the same GRPO paradigm transfers directly to agent memory management: structured ADD/UPDATE/DELETE operations emerge from retrieval accuracy rewards with only 152 training examples. This is the closest existing work to the cross-lingual memory management problem in indic-agents — the key extension is adding a cross-lingual LINK operation with retrieval correctness across language boundaries as the verifiable reward.

**Process Reward Models That Think** (Khalifa et al., ICLR 2025) identifies a critical bottleneck: PRM quality limits the ceiling of RLVR training. For the cultural compliance RLVR sub-direction in this project, a thinking PRM that evaluates Indic cultural norm adherence at each response turn — rather than only at the terminal output — would provide substantially denser training signal than a final-output rule checker.

**K2V** (Yuan et al., ICLR 2026) extends RLVR to knowledge-intensive domains by using knowledge graph completion as the verifiable reward scaffold. This is directly applicable to Indic-language knowledge-intensive QA (MILU, IndicGenBench): a KG built from SCERT textbooks or Kerala government scheme documents provides dense intermediate rewards for multi-hop reasoning chains that cannot be verified by a single answer extraction alone.

**Convergent finding:** The four research gaps identified in this review (multilingual memory evaluation, Indian cultural alignment data, cross-lingual CoT, cross-lingual memory linking) share a common root — the absence of verifiable, language-agnostic training signals. RLVR resolves this: retrieval correctness (verified via Samanantar parallel pairs), answer correctness (verified via MILU/IndicGenBench), and cultural compliance (verified via India-CASA rule checker) are all constructible as verifiable rewards without human annotation of reasoning chains. This positions RLVR as the unifying training mechanism for the indic-agents v1.0 objective.

---

## 9. Language Pivoting and Multilingual Reasoning

### Papers Reviewed
| Paper | Venue | Key Contribution |
|-------|-------|-----------------|
| [Language Models are Multilingual CoT Reasoners (MGSM)](08_language_pivoting/mgsm_emnlp2022.md) | EMNLP 2022 | Foundational benchmark: CoT works in 10 languages including Bengali |
| [PLUG: Pivot Language in Cross-Lingual Instruction Tuning](08_language_pivoting/plug_acl2024.md) | ACL 2024 | English-pivot instruction tuning yields ~29% gain for lower-resource languages |
| [Semantic Pivots Enable Cross-Lingual Transfer](08_language_pivoting/semantic-pivots_2025.md) | arXiv 2025 | Identifies English as implicit semantic pivot in LLM internals; targeted pretraining improves it |
| [Do Multilingual LLMs Think In English?](08_language_pivoting/do-multilingual-llms-think-in-english_2025.md) | arXiv 2025 | Logit lens shows implicit English-pivot even for non-English inputs; a transparency problem |
| [Think Natively: Multilingual Reasoning via Consistency-Enhanced RL](08_language_pivoting/think-natively_2024.md) | arXiv 2025 | RL rewards for language consistency enforce native-language CoT; RLVR controls language behavior |
| [Could Thinking Multilingually Empower LLM Reasoning?](08_language_pivoting/could-thinking-multilingually_2025.md) | arXiv 2025 | ~10 Acc@k headroom over English-only reasoning by allowing optimal language selection |

### Synthesis

**Language pivoting** refers to using a high-resource language — almost always English — as an intermediate reasoning step in multilingual LLMs. The debate on whether to pivot to English for reasoning is one of the most practically consequential open questions for the indic-agents project.

**Arguments for pivoting** are empirically grounded in instruction quality. **PLUG** (Zhang et al., ACL 2024) demonstrates a ~29% improvement in cross-lingual instruction-following by routing interpretation through English, attributing the gain to the mismatch between English-dominant pretraining and lower-resource target languages. This is reinforced by **He et al.** (2025), who show that English *is* the semantic pivot structurally embedded in LLM internals — the model has learned to use English as the conceptual hub during pretraining, and this mechanism enables cross-lingual transfer.

**Arguments against pivoting** are equally empirical but more recent. **Gao et al.** (2025) demonstrate ~10 Acc@k points of headroom above English-only reasoning when models are free to reason in their most capable language, revealing that forced English pivoting is leaving performance on the table. **Schut et al.** (2025) expose a transparency dimension: current LLMs already implicitly pivot through English without user awareness, introducing invisible semantic distortions for concepts that don't translate cleanly. **Zhang et al.** (2025) directly address this with M-Thinker: RL-trained language consistency rewards can suppress English drift and enforce native-language reasoning chains, with generalization to unseen languages — demonstrating that the English bias is a learned artifact correctable by RLVR.

**The foundational question** — posed implicitly by **MGSM** (Shi et al., 2022) — is whether the CoT reasoning ability itself is language-agnostic, or whether English provides genuine cognitive advantage as a reasoning medium. Current evidence suggests the former: at sufficient model scale and with appropriate training signals, reasoning quality in non-English languages can match or exceed English. The performance gap is an artifact of data imbalance and training signal design, not an inherent property of language.

**Implications for indic-agents:** The pivot debate maps directly onto **R2** (synthetic reasoning augmentation). For low-resource Indic languages with sparse pretraining data, a transitional English-pivot approach (PLUG-style) may be necessary in the short term. However, the long-term goal — and the RLVR research direction — is to train models with language consistency rewards (M-Thinker-style) that reason natively in Indic languages, eliminating the implicit English distortion that Schut et al. identify. The ~10-point multilingual reasoning headroom provides a quantifiable target for this research direction.

---

## 10. Research Gaps and Open Problems

Based on the reviewed literature, the following gaps are most relevant to the indic-agents project:

### 8.1 Multilingual Agent Memory Evaluation
No existing benchmark evaluates agent memory specifically in multilingual or cross-lingual settings. IndicGenBench and IndicParam evaluate LLM generation, XRAG evaluates cross-lingual RAG — but no work measures whether an agent can correctly *retrieve* a memory stored in one language when queried in another. This is the core evaluation gap for **R3**.

### 8.2 Cultural Alignment for Indian Subcultures
CultureLLM covers Bengali as a proxy for South Asia, but India has 22+ culturally distinct linguistic communities. Neither WVS nor existing surveys capture the full diversity of Indian cultural norms. There is no benchmark comparable to CASA for Indian cultural contexts. The project should target this as a dataset contribution.

### 8.3 Cross-Lingual Chain-of-Thought (CoT) Reasoning
Cross-lingual RAG is well-studied; cross-lingual *reasoning* is not. The indic-agents project identifies "cross-lingual chain-of-thought" as a challenge, but no existing paper provides a dedicated treatment of multilingual CoT specifically for Indic languages. Democratizing LLMs (Nguyen et al.) addresses this via prompting, but it uses English as an explicit pivot — true cross-lingual CoT (reasoning natively in the target language) remains open. This is the most novel gap for **R2**.

### 8.4 Memory Fragmentation in Multilingual Contexts
A-MEM's dynamic linking addresses memory organization in monolingual settings. For multilingual agents, a memory about "पानी" (Hindi: water) and "நீர்" (Tamil: water) should be recognized as the same concept and linked accordingly. No existing memory system handles cross-lingual memory deduplication and linking. This is the most technically novel contribution opportunity for **R3**.

---

## 11. Conclusion: Mapping to Project Research Directions

| Research Direction | Most Relevant Papers | Key Insight |
|--------------------|---------------------|-------------|
| **R1: Knowledge assimilation** | Wang et al. 2025, Nguyen et al. 2024, Shaham et al. 2024 | English-inclusive CPT for fine-tuning; 40-example multilingual instruction pinch; English-pivot prompting for zero-shot |
| **R2: Synthetic reasoning augmentation** | DeepSeek-R1 2025, K2V (ICLR 2026), Nguyen et al. 2024, Liu et al. 2025 (XRAG) | Emergent Indic CoT via RLVR (no CoT annotation); K2V dense rewards for knowledge-intensive Indic QA; English-pivot baseline |
| **R3: Dynamic memory management** | Memory-R1 2025, Xu et al. 2025 (A-MEM), Wang et al. 2024 (WISE), Khalifa et al. (PRM-Think) | GRPO for cross-lingual memory ops; Zettelkasten linking for cross-lingual memories; WISE sharding for multilingual edits; thinking PRM for cultural compliance verification |

The indic-agents project is positioned at the intersection of all seven literature streams reviewed here. No single existing paper addresses the full scope of the project; the novelty lies precisely in the integration: a memory system that is simultaneously agentic (A-MEM-style), multilingual (steering-vector-aligned), culturally-safe (SCGRD-debate-protected), Indic-tokenization-aware, and RLVR-trained with verifiable cross-lingual and cultural rewards. RLVR is the missing piece that makes annotation-free training possible across all four identified research gaps.

---

## References

Full BibTeX entries for all papers: [references.bib](references.bib)

### Theme 1: LLM Agent Memory Architectures
- Xu et al. (NeurIPS 2025) — A-MEM: Agentic Memory for LLM Agents. arXiv:2502.12110
- Hu et al. (2025) — Memory in the Age of AI Agents: A Survey. arXiv:2512.13564
- Wang et al. (NeurIPS 2024) — WISE: Rethinking Knowledge Memory for Lifelong Model Editing. arXiv:2405.14768

### Theme 2: Cross-Lingual RAG
- Liu et al. (EMNLP 2025) — XRAG: Cross-lingual Retrieval-Augmented Generation. arXiv:2505.10089
- Li et al. (2024) — Multilingual RAG for Culturally-Sensitive Tasks (BordIRLines). arXiv:2410.01171
- Chirkova et al. (ACL 2024) — Retrieval-augmented generation in multilingual settings. arXiv:2407.01463

### Theme 3: Multilingual LLMs & Indic Languages
- Singh et al. (ACL 2024) — IndicGenBench. arXiv:2404.16816
- Raj et al. (2024) — IndicParam. arXiv:2512.00333
- Poria & Huang (EMNLP 2025) — Bhaasha, Bhāṣā, Zaban: South Asian Language Survey. arXiv:2509.11570
- Nguyen et al. (ACL 2024) — Democratizing LLMs for Low-Resource Languages. arXiv:2306.11372
- Wang et al. (ACL 2025) — Emergent Abilities via Continued Pretraining. arXiv:2506.00288

### Theme 4: Cross-Lingual Alignment
- Liu et al. (ACL 2024) — Understanding Cross-Lingual Alignment: A Survey. arXiv:2404.06228
- Sundar et al. (ACL 2025) — Steering into New Embedding Spaces. arXiv:2502.15639
- Shaham et al. (ACL 2024) — Multilingual Instruction Tuning with Just a Pinch of Multilinguality. arXiv:2401.01854

### Theme 5: Cultural Bias in LLMs
- Li et al. (NeurIPS 2024) — CultureLLM: Incorporating Cultural Differences into LLMs. arXiv:2402.10946
- Tan et al. (2026) — Mitigating Cultural Bias via Multi-Agent Cultural Debate. arXiv:2601.12091
- Qiu et al. (NAACL 2025) — Evaluating Cultural and Social Awareness of LLM Web Agents (CASA). arXiv:2410.23252

### Theme 6: Morphological Tokenization
- Mahurkar & Joshi (2025) — MorphTok: Morphologically Grounded Tokenization for Indian Languages. arXiv:2504.10335
- Karthika et al. (2025) — Multilingual Tokenization through the Lens of Indian Languages. arXiv:2506.17789

### Theme 7: Reinforcement Learning with Verifiable Rewards (RLVR)
- DeepSeek-AI (2025) — DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning. arXiv:2501.12948
- Yan et al. (2025) — Memory-R1: Enhancing LLM Agents to Manage and Utilize Memories via Reinforcement Learning. arXiv:2508.19828
- Khalifa et al. (ICLR 2025) — Process Reward Models That Think. arXiv:2504.16828
- Yuan et al. (ICLR 2026) — Knowledge-to-Verification: Unlocking RLVR for Knowledge-Intensive Domains. OpenReview:EVS7SeKBqI

### Theme 8: Language Pivoting and Multilingual Reasoning
- Shi et al. (EMNLP 2022) — Language Models are Multilingual Chain-of-Thought Reasoners. arXiv:2210.03057
- Zhang et al. (ACL 2024) — PLUG: Leveraging Pivot Language in Cross-Lingual Instruction Tuning. arXiv:2311.08711
- He et al. (2025) — Semantic Pivots Enable Cross-Lingual Transfer in Large Language Models. arXiv:2505.16385
- Schut et al. (2025) — Do Multilingual LLMs Think In English? arXiv:2502.15603
- Zhang et al. (2025) — Think Natively: Unlocking Multilingual Reasoning with Consistency-Enhanced RL. arXiv:2510.07300
- Gao et al. (2025) — Could Thinking Multilingually Empower LLM Reasoning? arXiv:2504.11833
