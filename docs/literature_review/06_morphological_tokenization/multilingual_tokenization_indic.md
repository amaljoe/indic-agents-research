# Multilingual Tokenization through the Lens of Indian Languages: Challenges and Insights

**Authors:** N J Karthika, Gokul Karthik Kumar, Karthik Nandakumar

**Venue:** arXiv (2025)

**ArXiv:** [2506.17789](https://arxiv.org/abs/2506.17789)

---

## Abstract Summary

This paper provides a systematic intrinsic evaluation of tokenization strategies across **17 Indian languages**, quantifying the trade-offs between BPE and Unigram LM algorithms across different vocabulary sizes. A key finding is that extremely low-resource Indic languages (e.g., Santali, Manipuri) benefit significantly from tokenizers trained on typologically related high-resource languages rather than language-specific tokenizers (which suffer from insufficient training data). The paper provides practical guidance for fair multilingual tokenizer design that does not systematically disadvantage Indic language speakers.

---

## Key Contributions

- **17-language coverage**: Broadest intrinsic tokenization study for Indian languages
- **BPE vs. Unigram analysis**: Systematic comparison across vocabulary sizes and language families
- **Cross-lingual tokenizer benefit**: Low-resource languages gain from related high-resource tokenizers
- **Fairness framing**: Quantifies tokenization inequality (fertility disparity) across Indic languages
- **Practical guidelines**: Provides vocabulary size and algorithm recommendations per language family

---

## Relevance to indic-agents

Directly addresses the **tokenization inequality** that causes higher inference costs for Indic language users. An agent responding in Telugu or Kannada consumes more tokens than the same response in English, creating latency and cost disparities. This paper's cross-lingual tokenizer recommendations can reduce that gap in the project's vLLM stack.
