# RLVR-Guided Memory and Reasoning for Sovereign Indic AI Agents

**Project:** indic-agents — IIT Bombay
**Version:** Draft v0.1 (March 2026)

---

## 1. Problem Statement

The literature review for this project identified four research gaps that currently block the deployment of effective AI agents in Indic language contexts:

| Gap | Description |
|-----|-------------|
| **G1** | No benchmark evaluates agent memory in multilingual / cross-lingual settings |
| **G2** | No cultural alignment data for Indian subcultures beyond Bengali (WVS proxy) |
| **G3** | Cross-lingual chain-of-thought (CoT) reasoning for Indic languages is unstudied; models default to English pivot |
| **G4** | No memory system handles cross-lingual memory deduplication or linking (e.g., "पानी" and "நீர்" as the same concept) |

These four gaps appear to be independent problems requiring four separate solutions. This proposal argues they share a **common root** and a **common solution**.

**Common root:** All four gaps arise from the absence of a language-agnostic, verifiable training signal. Supervised fine-tuning requires human-annotated data — and there is no large-scale annotated corpus of:
- cross-lingual memory retrieval pairs in Indic languages
- Indian cultural compliance ground-truth labels
- Indic-language reasoning chains (CoT traces)
- cross-lingual concept identity graphs

**Common solution:** Reinforcement Learning with Verifiable Rewards (RLVR) — specifically, the GRPO-style training paradigm demonstrated in DeepSeek-R1 — provides outcome-based rewards that do not require explicit annotation of intermediate steps. As long as the *outcome* of a reasoning or memory operation is verifiable, RLVR can train towards it without labeled process data.

The central thesis of this proposal is:

> **RLVR, applied with culturally and linguistically grounded verifiable rewards, is the missing training mechanism that unifies all four research gaps into a single training framework for Indic AI agents.**

---

## 2. Background

### 2.1 RLVR: What It Is

Reinforcement Learning with Verifiable Rewards (RLVR) trains language models using binary or structured reward signals computed directly from model outputs — without a learned reward model. The key insight from DeepSeek-R1 (arXiv:2501.12948) is that when the task has a verifiable ground truth (e.g., mathematical answer correctness, code execution pass/fail), sophisticated reasoning behaviors — self-reflection, error correction, strategy switching — **emerge spontaneously** through GRPO training, without any explicit chain-of-thought supervision.

Memory-R1 (arXiv:2508.19828) extends this to agent memory operations: an agent trained with GRPO to perform ADD/UPDATE/DELETE operations on a memory store, with retrieval accuracy as the verifiable reward, learns structured memory management from only 152 training examples.

### 2.2 What Makes a Reward "Verifiable" in the Indic Context

A reward is verifiable if it can be computed programmatically from model output without human judgment. In the Indic agent context, the following rewards are constructible:

1. **Retrieval correctness** — given a query in language A, did the agent retrieve a memory stored in language B that is semantically equivalent? Verifiable via bilingual lexicons, translation APIs, or parallel corpora (Samanantar provides ~8M Malayalam-English pairs alone).

2. **Answer factual correctness** — is the agent's answer to a knowledge question correct? Verifiable against structured benchmarks (MILU: 150K+ questions across 11 Indic languages; IndicGenBench; IndicParam).

3. **Cultural compliance** — does the agent's response violate a codified cultural norm? Verifiable against a rule-based CASA-style checker adapted to Indian contexts (a side contribution of this project).

4. **Scheme eligibility correctness** — given a user's described circumstances, does the agent correctly determine eligibility for a government scheme? Verifiable against structured eligibility rules extracted from official documents.

None of these rewards require human annotation of reasoning chains, CoT traces, or cultural sentiment — they only require the correct final answer or a programmatic rule check.

---

## 3. Proposed Research Directions

### 3.1 Cross-Lingual Memory Linking via RLVR (Addresses G1 + G4)

**Motivation:** Memory-R1 shows that GRPO can train a memory manager agent with structured operations (ADD, UPDATE, DELETE) from minimal supervision. A-MEM shows that Zettelkasten-style linking between related memories prevents fragmentation. The gap: neither paper addresses multilingual memories — a memory about "पानी" (Hindi) and "நீர்" (Tamil: water) stored separately will not be linked without explicit cross-lingual signals.

**Proposed approach:**
1. Extend the Memory-R1 architecture with a cross-lingual LINK operation.
2. Define verifiable reward: given a memory store containing entries in multiple Indic languages, and a query in language X, the agent receives +1 if it retrieves the semantically correct memory (regardless of what language it was stored in).
3. Generate training pairs automatically using Samanantar parallel corpus: translate a memory entry into 3–5 Indic languages, store all versions, and verify cross-lingual retrieval.
4. Train with GRPO; evaluate on a new **XLMEM benchmark** (cross-lingual memory evaluation — a dataset contribution of this project targeting G1).

**Expected contribution:** First memory system trained end-to-end to link and retrieve cross-lingual memories via RLVR. First benchmark for multilingual agent memory evaluation.

**Research map:** R1 (knowledge assimilation of cross-lingual memories) + R3 (on-write linking, on-read cross-lingual retrieval)

---

### 3.2 Emergent Cross-Lingual CoT via RLVR (Addresses G3)

**Motivation:** DeepSeek-R1 demonstrated that mathematical reasoning chains emerge in LLMs trained purely on answer correctness rewards — no reasoning annotation required. The same phenomenon has been replicated for medical reasoning (Med-RLVR, arXiv:2502.19655) and knowledge-intensive domains (K2V, ICLR 2026). The critical open question for this project: **does native-language reasoning emerge in Indic languages when RLVR is applied to Indic-language question answering?**

Current models use English as a pivot language even when prompted in Tamil or Telugu. This is not just a stylistic issue — English-pivot reasoning loses culture-specific contextual chains and increases latency for the end user.

**Proposed approach:**
1. Start from a model with sufficient Indic-language pretraining (e.g., after continued pretraining on IndicCorp as per Wang et al. ACL 2025 / R1 direction).
2. Apply GRPO with answer correctness on MILU / IndicGenBench reasoning tasks as the verifiable reward.
3. **Key hypothesis:** Given adequate Indic pretraining, native-language CoT emerges in the target language — the same way mathematical CoT emerged in English for DeepSeek-R1.
4. Evaluate: what fraction of generated reasoning chains are in the target Indic language vs English pivot? Does native-language CoT improve accuracy on culturally-grounded tasks?

**Expected contribution:** First systematic study of emergent Indic-language CoT via RLVR. If the hypothesis holds, this is a high-impact result: RLVR + Indic pretraining = native reasoning without any CoT annotation.

**Research map:** R2 (synthetic reasoning augmentation for cross-lingual text)

---

### 3.3 Culturally-Verifiable Response Generation (Addresses G2)

**Motivation:** CultureLLM (NeurIPS 2024) demonstrates that cultural fine-tuning using World Values Survey data improves cultural awareness — but WVS covers only one South Asian culture (Bengali as a proxy) and does not capture India's 22+ culturally distinct linguistic communities. CASA (NAACL 2025) shows that current agents violate cultural norms >40% of the time. The Tan et al. multi-agent debate approach (arXiv:2601.12091) is training-free but does not improve the underlying model.

**Proposed approach:**
1. Construct an **India-CASA** benchmark: adapt CASA evaluation scenarios (shopping, forum, task completion) to Indian cultural contexts using existing structured data sources — National Family Health Survey, Kerala/Tamil Nadu cultural surveys, MILU cultural knowledge domain.
2. Define verifiable cultural compliance reward: a rule-based checker scoring responses against India-CASA scenarios (similar to how code execution verifies program correctness — no ambiguity in the ground truth).
3. Apply GRPO with cultural compliance as the reward signal, initializing from a model already aligned via CultureLLM-style fine-tuning (two-phase: SFT cultural seeds → RLVR compliance refinement).
4. Evaluate on India-CASA; track cultural violation rate reduction.

**Expected contribution:** First RLVR training loop with Indian cultural compliance as the verifiable reward. India-CASA as a standalone dataset contribution (Bengali + Hindi + Tamil + Malayalam + Kannada contexts).

**Research map:** R3 (drift prevention via culturally-grounded memory and response policy)

---

## 4. Unified Framework

The three sub-directions above are not independent — they compose into a single agent training objective:

```
Agent reward = α · retrieval_correctness(cross-lingual)
             + β · answer_correctness(Indic-language reasoning)
             + γ · cultural_compliance(India-CASA)
```

All three components are verifiable without human annotation. The agent that maximizes this joint reward:
- Stores and retrieves cross-lingual memories correctly (**G4**, **G1** solved)
- Reasons natively in the user's language (**G3** solved)
- Generates culturally-safe responses (**G2** partially solved — full solution requires India-CASA data collection)

This is the **indic-agents training objective for v1.0.**

---

## 5. Connections to Existing Literature

| This proposal | Built on | Extends |
|---------------|----------|---------|
| Cross-lingual LINK operation | Memory-R1 (ADD/UPDATE/DELETE via GRPO) | Adds cross-lingual identity reward |
| Cross-lingual memory linking | A-MEM (Zettelkasten structure) | Replaces monolingual assumption with cross-lingual reward |
| Emergent Indic CoT | DeepSeek-R1 (math CoT emerges from RLVR) | Tests hypothesis in Indic language context |
| Emergent Indic CoT | K2V (RLVR for knowledge-intensive domains) | Knowledge-intensive Indic QA as reward source |
| Cultural RLVR | CultureLLM (SFT cultural seeds) | Replaces SFT-only with RLVR refinement loop |
| Cultural RLVR | CASA (violation rate as metric) | Adapts CASA to Indian contexts as verifiable reward |
| Process verification | PRM-Think (ICLR 2025) | Step-level cultural compliance checking |
| Evaluation | MILU, IndicGenBench, IndicParam | Reward signal and evaluation benchmark |
| Tokenization foundation | MorphTok, Karthika et al. | Precondition: correct tokenization before RLVR training |

---

## 6. Why This Is Novel

The novelty lies not in RLVR (established), not in Indic NLP (active area), and not in agent memory (growing area) — but in their **combination**:

1. No paper has applied RLVR to cross-lingual memory management.
2. No paper has tested whether native-language reasoning emerges in Indic languages via RLVR.
3. No paper uses cultural compliance as a verifiable reward in an RLVR training loop.
4. No paper proposes a unified, annotation-free training objective for a multilingual, memory-equipped, culturally-grounded agent.

The project is positioned at the precise intersection where all four gaps converge, and RLVR provides the key that unlocks all of them simultaneously.

---

## 7. Next Steps

| Priority | Action |
|----------|--------|
| P0 | Set up evaluation infrastructure: MILU + IndicGenBench as verifiable reward oracles |
| P0 | Implement cross-lingual memory pair generation pipeline using Samanantar |
| P1 | Run baseline: Memory-R1-style training on monolingual Malayalam memory tasks |
| P1 | Run RLVR CoT experiment: GRPO on MILU Malayalam split; measure CoT language distribution |
| P2 | Construct India-CASA dataset: 500 annotated cultural compliance scenarios (5 languages) |
| P2 | Publish XLMEM benchmark (cross-lingual memory evaluation) as a dataset paper |
| P3 | Joint training: combine all three reward components; evaluate on held-out Indic agent tasks |
