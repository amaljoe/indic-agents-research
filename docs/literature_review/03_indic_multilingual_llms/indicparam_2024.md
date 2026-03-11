# IndicParam: Benchmark to Evaluate LLMs on Low-Resource Indic Languages

**Authors:** Aman Raj, Anupam Singh, and others

**Venue:** arXiv (2024)

**ArXiv:** [2512.00333](https://arxiv.org/abs/2512.00333)

---

## Abstract Summary

IndicParam introduces a benchmark with 13,000+ questions covering 11 low-resource and extremely-low-resource Indic languages, including several with fewer than 1 million native speakers. The benchmark also includes English-Sanskrit code-mixing as a special category. Questions have granular annotations for question type (factual, reasoning, cultural) and category, enabling fine-grained analysis that discriminates between factual recall ability and grammatical proficiency. The top-performing model (Gemini 2.5) achieves only 58% average accuracy, underscoring the difficulty of these low-resource languages.

---

## Key Contributions

- **Focus on low-resource**: Targets 11 languages that larger benchmarks ignore
- **Granular annotations**: Question-type (factual/reasoning/cultural) and category labels
- **Code-mixing support**: English-Sanskrit code-mixed test set reflecting real-world usage
- **Discrimination of skills**: Separates grammatical proficiency from factual recall evaluation
- **Leaderboard**: Benchmarks Gemini, GPT-4o, Claude, LLaMA, and Mistral families

---

## Relevance to indic-agents

Essential for evaluating agents targeting India's linguistic minorities. Many of the project's target communities (rural services, healthcare navigation) use exactly these low-resource languages — this benchmark allows measuring whether agents meet minimum usability thresholds for those populations.
