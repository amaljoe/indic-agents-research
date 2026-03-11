# IndicGenBench: A Multilingual Benchmark to Evaluate Generation Capabilities of LLMs on Indic Languages

**Authors:** Harman Singh, Nitish Gupta, Shikhar Bharadwaj, Dinesh Tewari, Partha Talukdar

**Venue:** ACL 2024 (Long Papers, pp. 11047–11073)

**ArXiv:** [2404.16816](https://arxiv.org/abs/2404.16816)

---

## Abstract Summary

IndicGenBench is the largest benchmark for evaluating LLM generation capabilities across 29 Indic languages covering 13 scripts and 4 language families (Indo-Aryan, Dravidian, Austroasiatic, Tibeto-Burman). The benchmark covers four generation tasks: cross-lingual summarization, machine translation, cross-lingual question answering, and cross-lingual dialogue. All test data is multi-way parallel across languages, enabling fair comparison. Extensive evaluation reveals significant performance gaps for low-resource Indic languages — even GPT-4 underperforms on Tibeto-Burman and Austroasiatic languages.

---

## Key Contributions

- **Scale**: 29 Indic languages across 13 scripts, the largest Indic generation benchmark
- **Multi-way parallel**: All tasks have parallel evaluation data across all 29 languages
- **Diverse task coverage**: Summarization, MT, QA, and dialogue generation
- **Gap analysis**: Quantifies performance gap between high-resource (Hindi, Bengali) and low-resource (Santali, Bodo) Indic languages
- **Model evaluation**: Benchmarks GPT-4, ChatGPT, LLaMA-2, and several open-source multilingual models

---

## Relevance to indic-agents

Provides the **evaluation infrastructure** for testing Indic agent capabilities. The benchmark directly quantifies which languages the project's target agents can reliably operate in, and which require specialized fine-tuning or retrieval augmentation.
