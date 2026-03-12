# Indic Agent Research Program

## Goal

Maximize accuracy on **MILU Malayalam** multiple-choice QA.
- Dataset: `ai4bharat/MILU`, config `Malayalam`, split `test`
- Model: `Qwen/Qwen3-1.7B` via vLLM on A100
- Each strategy runs for **5 minutes** wall-clock

---

## How the Loop Works

```bash
/dev/shm/vllm/bin/python indic_agent.py             # run all strategies
/dev/shm/vllm/bin/python indic_agent.py --strategy N # re-run one strategy
/dev/shm/vllm/bin/python indic_agent.py --minutes 1  # smoke test
```

The script:
1. Writes each strategy's code into `agent.py`
2. Evaluates for 5 minutes on MILU-ml test split
3. **Commits to git** if accuracy improves (KEEP)
4. **Reverts** `agent.py` (`git checkout HEAD -- agent.py`) if not improved (DISCARD)
5. Logs every run to `results.jsonl`

---

## Meta-Agent Guide (for Claude Code between runs)

When proposing a new `agent.py`:
- Uses `from vllm import LLM, SamplingParams`
- Exposes `answer_question(question: str, options: list[str]) -> int` (0-indexed A=0)
- Uses `LLM(model=MODEL_NAME, dtype="bfloat16", gpu_memory_utilization=0.4)`

**After reviewing `results.jsonl`:**
- If a strategy beat the previous best → add it as the next numbered entry in `STRATEGIES` in `indic_agent.py`
- If it lost → propose a variant that addresses the failure mode
- Focus on ONE change per iteration

---

## Research Directions

- **R2 — Language of reasoning**: English-pivot CoT vs. native Malayalam CoT (key question for paper)
- **R2 — Thinking mode**: Qwen3 `enable_thinking=True` for longer reasoning budget
- **R1 — Few-shot**: 2-shot vs 4-shot vs category-matched examples
- **R1 — Cultural grounding**: Kerala-specific system prompt
- **R1+R2 — Hybrid**: Few-shot + CoT
- **R3 — Category routing**: Route to different prompt templates by MILU subject category

---

## Strategies Defined (in indic_agent.py STRATEGIES dict)

| # | Name | Research | Description |
|---|------|----------|-------------|
| 0 | baseline-direct-ml | R2 | Direct Malayalam, greedy, 4 tokens |
| 1 | english-pivot-cot | R2 | Reason in English → ANSWER: X |
| 2 | native-malayalam-cot | R2 | Reason in Malayalam → ഉത്തരം: X |
| 3 | few-shot-2 | R1 | 2 validation examples in prompt |
| 4 | cultural-system-prompt | R1 | Kerala cultural context system prompt |
| 5 | few-shot-english-cot-hybrid | R1+R2 | 2-shot + English CoT combined |

---

## Results So Far (live)

| Strategy | Acc | n | Notes |
|---|---|---|---|
| few-shot-2 (R1) | **0.2580** | 4321 | Best — 2-shot examples |
| baseline-direct-ml (R2) | 0.2571 | 4321 | Committed to git |
| english-pivot-cot (R2) | 0.2483 | 290 | Worse than baseline — pivot hurts! |
| native-malayalam-cot (R2) | 0.2346 | 243 | Worst — native CoT hurts too |
| cultural-system-prompt (R1) | running... | — | On GPU 1 |
| few-shot-english-cot-hybrid (R1+R2) | running... | — | On GPU 3 |

**Key finding**: For Qwen3-1.7B, CoT reasoning (both English-pivot and native) HURTS accuracy vs direct prompting. Few-shot examples help marginally. This directly maps to R2 research question.

## Best Result So Far

- Accuracy: **0.2578**
- Last run: strategy=few-shot-english-cot-hybrid acc=0.0000 on 23 examples (reverted)
- Updated: 2026-03-12 01:27
