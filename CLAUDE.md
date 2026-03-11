# CLAUDE.md — indic-agents-research

Instructions for Claude Code when working in this repository.

---

## Project Overview

Research repository for **agentic memory systems for sovereign Indic AI agents** — IIT Bombay.

Key files:
- `README.md` — project overview, research directions, repo structure
- `docs/literature_review/literature_review.md` — synthesis of 22 papers across 7 themes
- `docs/research_proposal/rlvr_indic_agents.md` — RLVR-based research proposal connecting all gaps
- `docs/use_cases.md` — Malayalam application roadmap and dataset guide

---

## Skills

### `/literature_review`

Adds a paper to the literature review. Usage:

```
/literature_review <arxiv_id_or_url_or_title>
```

The skill is defined in `.claude/skills/literature_review/skill.md`. It:
1. Fetches paper metadata
2. Classifies into one of 7 theme folders (`01_agent_memory/` through `07_rlvr/`)
3. Writes a formatted `<name>.md` summary
4. Surgically updates `docs/literature_review/literature_review.md`

---

## Literature Review Structure

```
docs/literature_review/
├── literature_review.md   ← main synthesis (22 papers, 7 themes)
├── references.bib         ← BibTeX for all papers
├── 01_agent_memory/       ← A-MEM, Memory Survey, WISE
├── 02_cross_lingual_rag/  ← XRAG, BordIRLines, RAG Multilingual
├── 03_indic_multilingual_llms/ ← IndicGenBench, IndicParam, Bhaasha, Democratizing LLMs, CPT
├── 04_cross_lingual_alignment/ ← Alignment Survey, Steering Vectors, Multilingual IT
├── 05_cultural_bias/      ← CultureLLM, Multi-Agent Debate, CASA
├── 06_morphological_tokenization/ ← MorphTok, Multilingual Tokenization Indic
└── 07_rlvr/               ← DeepSeek-R1, Memory-R1, PRM-Think, K2V
```

When adding a new paper:
- Use `/literature_review` skill — do not manually edit `literature_review.md` without following its surgical-edit instructions
- Update `references.bib` with the new BibTeX entry

---

## Research Directions

- **R1** — Knowledge assimilation for differential-resource languages
- **R2** — Synthetic reasoning augmentation for cross-lingual text
- **R3** — Dynamic on-read/on-write memory management

All paper summaries must map relevance to one or more of R1/R2/R3.

---

## Conventions

- Paper summary files: lowercase, hyphenated, `<keyword>_<venue><year>.md`
- All paths relative to repo root (`/home/compiling-ganesh/24m0797/workspace/indic-agents/`)
- Remote: `git@github.com:amaljoe/indic-agents-research.git` — branch `main`
- Commit style: imperative, concise (e.g. "Add MorphTok paper summary and update literature review")
