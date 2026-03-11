# CultureLLM: Incorporating Cultural Differences into Large Language Models

**Authors:** Cheng Li, Mengzhou Chen, Jindong Wang, Sunayana Sitaram, Xing Xie

**Venue:** NeurIPS 2024

**ArXiv:** [2402.10946](https://arxiv.org/abs/2402.10946)

---

## Abstract Summary

CultureLLM proposes a cost-effective fine-tuning approach to make LLMs culturally aware using data from the **World Values Survey (WVS)** augmented with semantic data augmentation. The approach trains 9 culture-specific models (Arabic, Bengali, Chinese, English, German, Korean, Portuguese, Spanish, Turkish) and one unified CultureLLM-One model. Evaluated on 59 culturally-specific datasets across 9 cultures, CultureLLM significantly outperforms GPT-3.5 and Gemini on cultural alignment tasks, and CultureLLM-One shows that a single model can capture diverse cultural value distributions.

---

## Key Contributions

- **World Values Survey alignment**: Uses WVS as ground truth for cultural value representation
- **Semantic data augmentation**: Generates culture-specific training data from limited WVS seed items
- **9 culture-specific models + unified model**: First study of this scale on cultural specialization
- **Bengali inclusion**: Includes a South Asian language (Bengali) in the cultural coverage
- **Outperforms GPT-3.5/Gemini**: Demonstrates fine-tuning beats prompting for cultural alignment

---

## Relevance to indic-agents

Bengali is included in CultureLLM, providing a direct model for Indic cultural alignment. The WVS-based fine-tuning methodology — adapted to use India-specific cultural survey data — could be applied to build culturally-grounded Indic agents that accurately represent regional values and norms.
