# Malayalam Use Cases: Applying Indic Agents Research

**Focus language:** Malayalam (മലയാളം)
**Why Malayalam:** Personal motivation + strong research case

---

## Why Malayalam Is the Right Starting Point

Malayalam is spoken by approximately 38 million native speakers, primarily in Kerala, Lakshadweep, and among diaspora communities globally. It is the 8th scheduled language of India and has a literary tradition spanning over a millennium — yet it remains severely under-served by current large language models.

**The technical case:**
- Malayalam is highly agglutinative and morphologically rich: a single Malayalam word can carry tense, aspect, mood, subject agreement, and object agreement simultaneously. Standard BPE tokenizers systematically over-segment Malayalam, producing 2–3× higher token counts than English equivalents — inflating inference costs and degrading representation quality.
- Malayalam belongs to the Dravidian language family, structurally distant from Hindi (Indo-Aryan), which means Hindi-centric multilingual models transfer poorly to Malayalam — making it a genuinely hard, publishable test case.
- IndicGenBench data shows Malayalam accuracy drops exceed 20% compared to Hindi on most generation tasks across frontier models.

**The social case:**
- Kerala has the highest literacy rate in India (~96%) and among the highest smartphone penetration in rural India — a realistic deployment population exists right now.
- Kerala's healthcare system (one of India's best) is actively digitalizing; Malayalam-language healthcare agents would serve a population that is educated, digitally active, and underserved by English-only AI tools.
- The state's strong cooperative banking network, Kudumbashree women's self-help groups, and SCERT school system are all potential institutional partners for data collection and deployment pilots.

**The research case:**
- Malayalam's morphological complexity makes it a harder test case than Hindi for tokenization experiments (MorphTok addresses Hindi/Marathi; extending to Malayalam is a natural paper).
- Malayalam-English is one of the better-resourced Dravidian language pairs (Samanantar: ~8M sentence pairs) — sufficient for RLVR training without additional data collection in Phase 1.
- A Malayalam agent that works well generalizes more confidently to Tamil, Kannada, and Telugu (other Dravidian languages with similar structural properties) than a Hindi agent would.

---

## Use Case 1: Healthcare Navigation Agent

### Scenario
A patient in a rural district of Kerala needs to understand whether they qualify for treatment coverage under the Karunya Arogya Suraksha Padhathi (KASP) or Pradhan Mantri Jan Arogya Yojana (PM-JAY) schemes. They speak Malayalam, may have limited health literacy, and cannot navigate English-language government portals.

The agent should:
1. Understand the patient's described symptoms or diagnosis in Malayalam
2. Retrieve relevant scheme eligibility criteria
3. Explain what documentation is required, in plain Malayalam
4. Answer follow-up questions about nearby empanelled hospitals

### Why RLVR Works Here
Scheme eligibility is fully rule-based and verifiable: the government publishes structured eligibility criteria (income threshold, disease list, BPL card requirements). These rules can be parsed into a verifiable checker — if the agent says "eligible," a rule engine can confirm or deny. No human annotation of reasoning chains needed.

The medical factual accuracy component maps directly to Med-RLVR (arXiv:2502.19655): answer correctness on medical Q&A is verifiable against clinical knowledge bases.

### Datasets and Resources

**Immediately usable:**
- [FutureBee AI Malayalam Healthcare Chat Dataset](https://www.futurebeeai.com/dataset/chat-data-sets/malayalam) — domain-specific dialogues in banking, healthcare, telecom
- [IndicCorp Malayalam](https://ai4bharat.github.io/indicnlp_catalog/) — 721M tokens for general pretraining
- [Samanantar ml-en](https://huggingface.co/datasets/ai4bharat/samanantar) — ~8M Malayalam-English pairs for cross-lingual memory pair generation

**To collect:**
- KASP and PM-JAY scheme documents in Malayalam (available from Kerala government health portal — publicly accessible PDFs)
- List of empanelled hospitals with districts — structured, verifiable
- Kerala health portal FAQ content in Malayalam

**Data collection approach:**
- Scrape Kerala Health Department website (Malayalam content, government-licensed)
- Convert PDF scheme documents to structured eligibility rules (Python: pdfplumber + rule extraction)
- Create 200–500 Q&A pairs from scheme rules as initial RLVR training data

---

## Use Case 2: Educator Agent (Kerala State Curriculum)

### Scenario
A Class 10 student in Kerala asks questions about their SCERT (State Council of Educational Research and Training) syllabus in Malayalam — history of Kerala, social science concepts, basic science. The agent retrieves relevant textbook passages, explains concepts at the right level, and generates practice questions.

### Why RLVR Works Here
MILU (Multi-task Indic Language Understanding) benchmark includes regional and state-level examination content across 11 Indic languages. This provides an immediately available verifiable reward oracle: answer correctness on MILU Malayalam split. No annotation needed — MILU already has 150K+ questions with ground-truth answers.

Kerala PSC (Public Service Commission) exam Q&A banks are publicly available and contain thousands of verified Malayalam-language questions — directly usable as RLVR training signal.

### Datasets and Resources

**Immediately usable:**
- [MILU Benchmark](https://huggingface.co/datasets/ai4bharat/MILU) — 150K+ questions, 11 Indic languages, includes state history, culture, arts (arXiv:2411.02538)
- [IndicBERT](https://huggingface.co/ai4bharat/indic-bert) — pretrained multilingual model for Malayalam downstream tasks
- [IndicBART](https://huggingface.co/ai4bharat/IndicBART) — seq2seq model for summarization and generation

**To collect:**
- SCERT Kerala textbooks (Classes 1–12 are available as PDFs from scert.kerala.gov.in — Creative Commons licensed)
- Kerala PSC exam question banks (past papers publicly available)
- Previous Kerala SSLC/Plus Two board exam papers

**Data collection approach:**
- Download SCERT PDFs; extract chapter text (pdfplumber)
- Parse Kerala PSC question banks into QA format
- Generate additional QA pairs from textbook passages using IndicBART as a synthetic data generator (then use MILU accuracy as verification)
- Target: 5,000 curriculum-aligned QA pairs in Malayalam for initial training

---

## Use Case 3: Rural Commerce and Banking Agent

### Scenario
A Kudumbashree member in a rural Palakkad district wants to understand eligibility for a self-help group loan, check current procurement prices at the nearest cooperative society, or understand the steps to register a micro-enterprise under the MSME scheme. All in Malayalam.

### Why RLVR Works Here
Government scheme eligibility rules are structured and verifiable (same mechanism as Use Case 1). Procurement prices can be fetched from Kerala Agricultural Prices portal and verified programmatically. MSME registration steps are fixed — correct answer is verifiable.

### Datasets and Resources

**Immediately usable:**
- [FutureBee AI Malayalam Banking Chat](https://www.futurebeeai.com/dataset/chat-data-sets/malayalam) — banking and real estate domain dialogues
- [Samanantar ml-en](https://huggingface.co/datasets/ai4bharat/samanantar) — for cross-lingual memory training

**To collect:**
- Kudumbashree scheme documents: kudumbashree.org (Malayalam PDFs, publicly available)
- NABARD Kerala circulars (English; translate to Malayalam using IndicTrans2 as synthetic training data)
- Kerala cooperative bank loan product documents (publicly listed)
- Kerala Agricultural Prices portal data (structured, scrapeable)

**Data collection approach:**
- Download and OCR Kudumbashree documents (Malayalam text available directly)
- Structure loan eligibility criteria into rule-based verifier (Python dict → RLVR checker)
- Scrape Kerala AgriPrice portal for structured price data
- Target: 300–500 scheme eligibility QA pairs as initial RLVR training data

---

## Use Case 4: Legal Information Agent

### Scenario
A tenant in Thrissur wants to understand their rights if a landlord cuts water supply; a consumer in Kozhikode wants to file a complaint against a defective appliance. The agent explains relevant laws in plain Malayalam, outlines the correct complaint procedure, and cites the relevant section of Kerala's Rent Control Act or Consumer Protection Act.

### Why RLVR Works Here
Legal citations are verifiable: if the agent cites Section 12 of the Kerala Buildings (Lease and Rent Control) Act, a rule-based checker can verify whether that section actually pertains to the described situation. The IL-TUR benchmark (arXiv:2407.05399) covers 9 Indian languages for legal text understanding and provides an evaluation framework.

### Datasets and Resources

**Immediately usable:**
- [IL-TUR Benchmark](https://arxiv.org/html/2407.05399v1) — Indian Legal Text Understanding and Reasoning, 9 languages
- [InLegalBERT](https://huggingface.co/) — pretrained model for Indian legal texts
- [LLM Fine-Tuning Dataset of Indian Legal Texts (Kaggle)](https://www.kaggle.com/datasets/akshatgupta7/llm-fine-tuning-dataset-of-indian-legal-texts)

**To collect:**
- Kerala High Court judgements: ecourts.gov.in (Malayalam + English; structured metadata)
- Kerala Rent Control Act, Consumer Protection Act (Malayalam versions: niyamasabha.org)
- Consumer Forum decisions from Kerala State Consumer Disputes Redressal Commission

**Data collection approach:**
- Download Kerala High Court judgements (public domain); extract headnotes in Malayalam
- Parse Acts into section-level chunks with semantic labels
- Build a citation verifier: given an agent response with a legal citation, verify section text relevance
- Target: 200–300 legal QA pairs with citation verification as initial RLVR reward

---

## Existing Malayalam Datasets: Quick Reference

| Dataset | Type | Size | Access |
|---------|------|------|--------|
| IndicCorp Malayalam | Monolingual | 721M tokens / 50.2M sentences | [ai4bharat.github.io/indicnlp_catalog](https://ai4bharat.github.io/indicnlp_catalog/) |
| Samanantar (ml↔en) | Parallel | ~8M sentence pairs | [huggingface.co/datasets/ai4bharat/samanantar](https://huggingface.co/datasets/ai4bharat/samanantar) |
| MILU | Multi-task eval | 150K+ questions, 11 languages | [huggingface.co/datasets/ai4bharat/MILU](https://huggingface.co/datasets/ai4bharat/MILU) |
| MABSA | Aspect-based sentiment | 4K movie reviews | [data.mendeley.com/datasets/f3ftpd7xpg](https://data.mendeley.com/datasets/f3ftpd7xpg/3) |
| Naamapadam (IndicNER) | Named entity recognition | 11 languages | HuggingFace: ai4bharat/naamapadam |
| BhasaAnuvaad | Speech translation | 44,400 hrs (13 langs) | [indiaai.gov.in](https://indiaai.gov.in) |
| Mlmorph | Morphological analyzer | Lexicon + API | [morph.smc.org.in](https://morph.smc.org.in/) |
| Indic NLP Library | Morphological tools | Python library | [github.com/anoopkunchukuttan/indic_nlp_library](https://github.com/anoopkunchukuttan/indic_nlp_library) |
| FutureBee Malayalam chat | Domain dialogues | Healthcare, banking, telecom | [futurebeeai.com](https://www.futurebeeai.com/dataset/chat-data-sets/malayalam) |
| IL-TUR Legal Benchmark | Legal QA | 9 Indic languages | [arxiv.org/abs/2407.05399](https://arxiv.org/abs/2407.05399) |
| South Asian NLP Survey | Catalog | Jan 2022–Oct 2024 coverage | [arxiv.org/abs/2501.00029](https://arxiv.org/abs/2501.00029) |

---

## Data Collection Roadmap

### Phase 1 — Leverage Existing (0–3 months)
- Use IndicCorp + Samanantar for pretraining / cross-lingual memory pair generation
- Use MILU Malayalam split as primary RLVR reward oracle for Use Case 2
- Use MABSA for sentiment evaluation baseline
- Set up Mlmorph + Indic NLP Library for morphological tokenization experiments

### Phase 2 — Targeted Collection (3–6 months)
- Download and parse SCERT Kerala textbooks (SCERT website, CC-licensed)
- Mine Kerala PSC past papers into QA format
- Extract KASP/PM-JAY/Kudumbashree eligibility rules into structured verifiers
- Annotate 500–1000 culturally-sensitive Q&A pairs for India-CASA (Malayalam cultural norms: Onam gifting etiquette, communal harmony norms, healthcare decision-making with family elders)
- Build citation verifier using Kerala Acts text

### Phase 3 — Community and Institutional (6–12 months)
- Partner with **Kerala Bhasha Institute** (Thiruvananthapuram) for literary and cultural data
- Pilot healthcare dialogue collection with District Medical Officer offices in Kerala
- Contact **SMC (Swathanthra Malayalam Computing)** — active Malayalam open-source computing community; they maintain Mlmorph and have extensive text resources
- Release **XLMEM-Malayalam** benchmark (cross-lingual memory evaluation, a dataset contribution from the RLVR proposal)
- Release **India-CASA-Malayalam** benchmark (100+ cultural compliance scenarios)

---

## Why This Strengthens the Research

**Harder test case = stronger paper:**
Malayalam's agglutinative morphology and Dravidian structure make it harder than Hindi. A positive result on Malayalam is more publishable than a positive result on a well-resourced language.

**All four RLVR rewards are constructible without expensive annotation:**
- Retrieval correctness: Samanantar parallel pairs → cross-lingual memory ground truth
- Answer correctness: MILU + PSC exam banks → reward oracle
- Scheme eligibility: structured government rules → programmatic verifier
- Cultural compliance: CASA-style rule checker → India-CASA annotation (500 examples, achievable by 2 annotators in 2 weeks)

**Realistic deployment path:**
Kerala's digital infrastructure (high smartphone penetration, active e-governance portals, cooperative banking network) makes the path from research prototype to field pilot shorter than most Indian states.

**Generalizes to other Dravidian languages:**
A memory and reasoning system that works for Malayalam with RLVR transfers directly to Tamil, Kannada, and Telugu — four of India's major languages — through the same framework with language-specific data substitution.
