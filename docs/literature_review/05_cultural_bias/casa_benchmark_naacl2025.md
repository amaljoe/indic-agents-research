# Evaluating Cultural and Social Awareness of LLM Web Agents

**Authors:** Haoyi Qiu, Alexander R. Fabbri, Divyansh Agarwal, Kung-Hsiang Huang, Sarah Tan, Nanyun Peng, Chien-Sheng Wu

**Venue:** NAACL 2025 (Findings)

**ArXiv:** [2410.23252](https://arxiv.org/abs/2410.23252)

---

## Abstract Summary

This paper introduces **CASA** (Cultural And Social Awareness), a benchmark assessing whether LLM-based web agents respect cultural and social norms when performing online tasks (shopping, forum interactions). The benchmark evaluates agents across 5 countries and 8 social groups. Alarmingly, current LLM agents achieve less than **10% cultural awareness coverage** and **over 40% violation rates** — meaning agents actively act against social norms more than they respect them. The paper proposes a combined prompting + fine-tuning approach that reduces violation rates to below 20%.

---

## Key Contributions

- **CASA benchmark**: First cultural/social norm awareness benchmark for LLM *agents* (not just LLMs)
- **10% coverage / 40% violation**: Quantifies the scale of cultural unawareness in current agents
- **Multi-country evaluation**: 5 countries, 8 social groups
- **Mitigation approach**: Combined prompting + fine-tuning reduces violations from 40%+ to <20%
- **Agentic framing**: Addresses cultural awareness at the *task-execution* level, not just QA level

---

## Relevance to indic-agents

Provides the **evaluation framework for culturally-safe Indic agents** in real-world deployment scenarios (healthcare navigation, commerce). The CASA methodology can be adapted to create an India-specific cultural safety benchmark for the project's target agent applications.
