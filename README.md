# Indic Agents Research

**Institution:** IIT Bombay
**Status:** Early Research — v0.1

Agentic memory systems for sovereign AI agents operating in Indian language contexts.

---

## Motivation

India's linguistic landscape comprises 22 scheduled languages, 650+ dialects, and over a billion speakers distributed across communities with radically different levels of NLP resource availability. Existing large language models, even multilingual ones, exhibit systematic performance degradation for Indic languages — higher token fertility, latent space fragmentation, cultural misalignment with Western training data, and near-zero coverage for hundreds of dialects.

Deploying functional AI agents in this context — agents that can remember, reason, and respond reliably in the user's language and cultural frame — is an unsolved problem. This project targets that gap directly: building agentic memory architectures that are **multilingual by design, culturally grounded, and sovereign** (deployable without dependence on Western API ecosystems).

---

## Research Directions

| Direction | Problem | Approach |
|-----------|---------|----------|
| **R1 — Knowledge Assimilation** | Differential resource availability across 22+ Indic languages makes uniform pretrained representations impossible | Language-family-aware continued pretraining; morphology-respecting tokenization; cross-lingual knowledge transfer from high- to low-resource languages |
| **R2 — Synthetic Reasoning Augmentation** | Cross-lingual chain-of-thought reasoning for Indic languages is largely unstudied; models default to English pivot even when prompted in Indic scripts | RLVR-driven emergent native-language reasoning; cross-lingual RAG with Indic-aware retrieval; structured multilingual instruction tuning |
| **R3 — Dynamic Memory Management** | No existing memory system handles cross-lingual memory linking, deduplication, or drift prevention | Zettelkasten-style memory with cross-lingual linking; WISE-style parametric memory editing scoped per language; RLVR-trained memory operations with verifiable retrieval rewards; culturally-verifiable response generation |

---

## Target Applications

| Application | Language Focus | Key Challenge |
|-------------|----------------|---------------|
| Healthcare navigation agent | Malayalam, Hindi, Tamil | Cultural appropriateness; medical accuracy |
| Educator agent (school curriculum) | All 22 scheduled languages | Knowledge retrieval from Indic-language textbooks |
| Rural commerce / banking agent | Dravidian + Indo-Aryan regional languages | Scheme eligibility reasoning; low-literacy interaction |
| Legal information agent | Regional language + official language pairs | Citation accuracy; jurisdiction-specific knowledge |

---

## Repository Structure

```
indic-agents/
├── README.md                          ← this file
├── docs/
│   ├── iitb_mlagentmem_v0.1.pptx     ← project overview presentation
│   ├── use_cases.md                   ← Malayalam use cases + dataset guide
│   ├── research_proposal/
│   │   └── rlvr_indic_agents.md       ← RLVR-based research proposal
│   └── literature_review/
│       ├── literature_review.md       ← full synthesis document
│       ├── references.bib             ← BibTeX for all papers
│       ├── 01_agent_memory/           ← LLM agent memory architectures
│       ├── 02_cross_lingual_rag/      ← cross-lingual RAG
│       ├── 03_indic_multilingual_llms/← multilingual LLMs & Indic languages
│       ├── 04_cross_lingual_alignment/← cross-lingual alignment
│       ├── 05_cultural_bias/          ← cultural bias in LLMs
│       ├── 06_morphological_tokenization/ ← Indic tokenization
│       └── 07_rlvr/                   ← reinforcement learning with verifiable rewards
└── .claude/
    └── skills/
        └── literature_review/         ← /literature_review skill for adding papers
```

---

## Literature Review

**22 papers** across 7 thematic areas from ACL, EMNLP, NeurIPS, NAACL, ICLR, IJCNLP, and arXiv.

[Full synthesis → docs/literature_review/literature_review.md](docs/literature_review/literature_review.md)
[BibTeX → docs/literature_review/references.bib](docs/literature_review/references.bib)

| Theme | Papers | Key Finding |
|-------|--------|-------------|
| LLM Agent Memory | 3 | A-MEM Zettelkasten + WISE parametric editing = R3 foundation |
| Cross-Lingual RAG | 3 | Two failure modes: retrieval mismatch + generation language inconsistency |
| Indic Multilingual LLMs | 5 | English-inclusive CPT necessary; 40 multilingual examples suffice for tuning |
| Cross-Lingual Alignment | 3 | Steering vectors offer data-efficient alignment without generation loss |
| Cultural Bias | 3 | <10% cultural awareness; SCGRD debate = training-free mitigation |
| Morphological Tokenization | 2 | Constrained BPE + related-language transfer = tokenization equity |
| RLVR | 4 | Verifiable rewards enable emergent reasoning without annotated CoT |

---

## Research Proposal

[RLVR-Guided Memory and Reasoning for Sovereign Indic AI Agents →](docs/research_proposal/rlvr_indic_agents.md)

Proposes RLVR as the unifying training mechanism across all four identified research gaps:
- Cross-lingual memory linking via verifiable retrieval rewards
- Emergent native-language CoT via outcome-based RLVR
- Culturally-verifiable response generation via rule-based compliance rewards

---

## Malayalam Use Cases

[Malayalam application roadmap + dataset guide →](docs/use_cases.md)

Concrete deployment targets for Kerala, including healthcare, education, rural banking, and legal use cases — with dataset pointers and data collection roadmap.

---

## Adding Papers

This repo ships with a `/literature_review` Claude Code skill:

```
/literature_review <arxiv_id_or_url_or_title>
```

The skill fetches paper metadata, classifies it into the right theme folder, writes a formatted summary, and surgically updates `literature_review.md`.
