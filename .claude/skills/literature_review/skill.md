# Skill: literature_review

Add a paper to the indic-agents literature review.

## Usage

```
/literature_review <arxiv_id_or_url_or_title>
```

Examples:
- `/literature_review 2502.12110`
- `/literature_review https://arxiv.org/abs/2410.01171`
- `/literature_review "MorphTok: Morphology-aware Tokenization for Hindi"`

---

## What to do

You are given a paper identifier (ArXiv ID, URL, or title). Perform the following steps **in order**:

### Step 1 — Fetch paper details

Use WebFetch or WebSearch to retrieve:
- Full title
- Authors (last names + et al. if >3)
- Venue and year (conference name, e.g. ACL 2024, NeurIPS 2025, or arXiv YYYY)
- ArXiv ID and link (format: `https://arxiv.org/abs/<id>`)
- Abstract (verbatim or near-verbatim)

### Step 2 — Classify into a theme folder

Map the paper to one of these six theme folders under `docs/literature_review/`:

| Folder | Theme | Keywords |
|--------|-------|----------|
| `01_agent_memory/` | LLM Agent Memory Architectures | memory, agent memory, memory editing, lifelong learning, continual learning |
| `02_cross_lingual_rag/` | Cross-Lingual RAG | retrieval-augmented generation, RAG, multilingual retrieval, cross-lingual QA |
| `03_indic_multilingual_llms/` | Multilingual LLMs & Indic Languages | Indic, South Asian, low-resource, multilingual LLM, pretraining, benchmark |
| `04_cross_lingual_alignment/` | Cross-Lingual Alignment | alignment, embedding space, instruction tuning, transfer, cross-lingual |
| `05_cultural_bias/` | Cultural Bias in LLMs | culture, bias, cultural awareness, values, persona, geopolitical |
| `06_morphological_tokenization/` | Morphological Tokenization | tokenization, morphology, BPE, fertility, subword, script |

If a paper spans multiple themes, pick the **primary** theme.

### Step 3 — Choose a filename

Derive a short, lowercase, hyphenated filename from the paper title or first author + year:
- `<keyword>_<venue><year>.md` (e.g., `xrag_emnlp2025.md`, `morphtok_2025.md`)
- Avoid spaces and special characters

### Step 4 — Write the paper summary file

Create `docs/literature_review/<theme_folder>/<filename>.md` with this exact template:

```markdown
# <Full Paper Title>

**Authors:** <Author list>

**Venue:** <Full venue name and year>

**ArXiv:** [<arxiv_id>](https://arxiv.org/abs/<arxiv_id>)

---

## Abstract Summary

<3–5 sentence summary of the paper's problem, method, and findings. Write in present tense.>

---

## Key Contributions

- **<contribution name>**: <1-sentence description>
- **<contribution name>**: <1-sentence description>
- (3–5 bullets)

---

## Relevance to indic-agents

<1–3 sentences. Explicitly mention which research direction(s) this addresses:>
- **R1** — Knowledge assimilation for differential-resource languages
- **R2** — Synthetic reasoning augmentation for cross-lingual text
- **R3** — Dynamic on-read/on-write memory management

<State whether the paper is directly cited in the indic-agents presentation (if known).>
```

### Step 5 — Update `docs/literature_review/literature_review.md`

Make **surgical edits only** — do not rewrite sections that don't need changes.

1. **Scope line** (line 5): Increment the paper count (e.g., "18 papers" → "19 papers") and add the venue if new.

2. **Theme section table**: Find the `### Papers Reviewed` table for the matching theme and append a new row:
   ```
   | [<Short Title>](<theme_folder>/<filename>.md) | <Venue Year> | <One-line contribution> |
   ```

3. **Theme synthesis paragraph**: Append 2–4 sentences to the existing synthesis summarising this paper's finding and how it connects to adjacent papers or the project's research directions. Place them after the last existing paragraph of that theme section, before the `---` separator.

4. **Do NOT touch** other sections, the introduction, research gaps, conclusion table, or references list unless directly relevant.

### Step 6 — Confirm

After writing, output a brief confirmation:
```
Added: docs/literature_review/<theme_folder>/<filename>.md
Updated: docs/literature_review/literature_review.md (section: <theme name>)
Theme: <theme name>
Venue: <venue>
R-directions: <R1/R2/R3 as applicable>
```

---

## Project context (for relevance assessment)

**Project:** indic-agents — IIT Bombay
**Goal:** Agentic memory systems for sovereign AI agents in Indian language contexts

**Three research directions:**
- **R1** — Effective knowledge assimilation for differential-resource languages (low-resource Indic languages, tokenization, pretraining)
- **R2** — Synthetic reasoning augmentation for cross-lingual text (cross-lingual RAG, alignment, instruction tuning)
- **R3** — Dynamic on-read/on-write memory management (memory architectures, cultural alignment, semantic drift prevention)

**Target applications:** Healthcare navigation, educator agents, rural commerce/banking, legal systems in India

**Key challenges:**
- Cross-lingual retrieval: latent space fragmentation across Indic language families
- Morphological tokenization gaps for agglutinative Indic scripts
- Semantic and behavioral memory drift toward dominant (English/Hindi) languages
- Cultural misalignment with South Asian values, dialects, and norms

**Existing theme coverage:**
- 01_agent_memory: A-MEM (NeurIPS 2025), Memory Survey (arXiv 2025), WISE (NeurIPS 2024)
- 02_cross_lingual_rag: XRAG (EMNLP 2025), BordIRLines (arXiv 2025), RAG Multilingual (ACL 2024)
- 03_indic_multilingual_llms: IndicGenBench (ACL 2024), IndicParam (arXiv 2024), Bhaasha Survey (EMNLP 2025), Democratizing LLMs (ACL 2024), Emergent Abilities (ACL 2025)
- 04_cross_lingual_alignment: Alignment Survey (ACL 2024), Steering Embedding Spaces (ACL 2025), Multilingual Instruction Tuning (ACL 2024)
- 05_cultural_bias: CultureLLM (NeurIPS 2024), Multi-Agent Cultural Debate (arXiv 2026), CASA (NAACL 2025)
- 06_morphological_tokenization: MorphTok (arXiv 2025), Multilingual Tokenization Indic (arXiv 2025)
