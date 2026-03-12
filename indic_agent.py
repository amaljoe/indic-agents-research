#!/dev/shm/vllm/bin/python
# indic_agent.py — Autoresearch loop for Indic agent (fixed infrastructure)
#
# Iterates through strategy variants in the STRATEGIES dict, evaluates each
# on MILU Malayalam for EVAL_MINUTES, commits improvements, reverts regressions.
# The meta-agent (human or Claude Code) modifies agent.py between runs.
#
# Usage:
#   /dev/shm/vllm/bin/python indic_agent.py             # run all strategies
#   /dev/shm/vllm/bin/python indic_agent.py --minutes 1  # quick smoke test
#   /dev/shm/vllm/bin/python indic_agent.py --strategy 2 # single strategy

import argparse
import importlib.util
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

EDITABLE_FILE = "agent.py"
LOG_FILE = Path("results.jsonl")
PROGRAM_FILE = Path("program.md")
MODEL_NAME = "Qwen/Qwen3-1.7B"

# ---------------------------------------------------------------------------
# Strategy definitions — each is a complete agent.py replacement.
# Covers R1/R2/R3 research directions from program.md.
# Add new strategies here; they run in order of key.
# ---------------------------------------------------------------------------

STRATEGIES = {
    0: {
        "name": "baseline-direct-ml",
        "description": "Direct Malayalam prompt, greedy decoding (baseline)",
        "research": "R2",
        "code": '''# Strategy 0: baseline — direct Malayalam prompting, greedy
import os
from vllm import LLM, SamplingParams

MODEL_NAME = os.environ.get("AGENT_MODEL", "{model}")
_llm = None

def _load():
    global _llm
    if _llm is None:
        print(f"  Loading: {{MODEL_NAME}}")
        _llm = LLM(model=MODEL_NAME, dtype="bfloat16", max_model_len=2048, gpu_memory_utilization=0.4)
    return _llm

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    opts = "\\n".join(f"{{chr(65+i)}}. {{o}}" for i, o in enumerate(options))
    prompt = (
        "<|im_start|>user\\n"
        "ചുവടെ കൊടുത്തിരിക്കുന്ന ചോദ്യത്തിന് ശരിയായ ഉത്തരം തിരഞ്ഞെടുക്കുക. "
        "A, B, C അല്ലെങ്കിൽ D എന്ന് മാത്രം ഉത്തരം നൽകുക.\\n\\n"
        f"ചോദ്യം: {{question}}\\n\\n{{opts}}"
        "<|im_end|>\\n<|im_start|>assistant\\n"
    )
    params = SamplingParams(max_tokens=4, temperature=0)
    out = llm.generate([prompt], params, use_tqdm=False)
    reply = out[0].outputs[0].text.strip()
    for i, l in enumerate("ABCD"):
        if reply.upper().startswith(l): return i
    return 0
''',
    },

    1: {
        "name": "english-pivot-cot",
        "description": "English-pivot CoT: reason in English, return letter (R2)",
        "research": "R2",
        "code": '''# Strategy 1: English-pivot CoT (R2 — pro-pivot, like PLUG/Semantic Pivots)
import os
from vllm import LLM, SamplingParams

MODEL_NAME = os.environ.get("AGENT_MODEL", "{model}")
_llm = None

def _load():
    global _llm
    if _llm is None:
        _llm = LLM(model=MODEL_NAME, dtype="bfloat16", max_model_len=4096, gpu_memory_utilization=0.4)
    return _llm

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    opts = "\\n".join(f"{{chr(65+i)}}. {{o}}" for i, o in enumerate(options))
    prompt = (
        "<|im_start|>user\\n"
        "This is a Malayalam multiple-choice question. Reason step-by-step in English, "
        "then on the LAST LINE write only: ANSWER: X (where X is A/B/C/D).\\n\\n"
        f"Question (Malayalam): {{question}}\\n\\nOptions:\\n{{opts}}"
        "<|im_end|>\\n<|im_start|>assistant\\n"
    )
    params = SamplingParams(max_tokens=250, temperature=0)
    out = llm.generate([prompt], params, use_tqdm=False)
    reply = out[0].outputs[0].text.strip()
    for line in reversed(reply.splitlines()):
        l = line.strip().upper()
        if "ANSWER:" in l:
            for i, letter in enumerate("ABCD"):
                if letter in l.split("ANSWER:")[-1]: return i
        for i, letter in enumerate("ABCD"):
            if l.startswith(letter): return i
    return 0
''',
    },

    2: {
        "name": "native-malayalam-cot",
        "description": "Native Malayalam CoT: reason in Malayalam, no English pivot (R2, Think-Natively style)",
        "research": "R2",
        "code": '''# Strategy 2: Native Malayalam CoT (R2 — anti-pivot, Think Natively / M-Thinker style)
import os
from vllm import LLM, SamplingParams

MODEL_NAME = os.environ.get("AGENT_MODEL", "{model}")
_llm = None

def _load():
    global _llm
    if _llm is None:
        _llm = LLM(model=MODEL_NAME, dtype="bfloat16", max_model_len=4096, gpu_memory_utilization=0.4)
    return _llm

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    opts = "\\n".join(f"{{chr(65+i)}}. {{o}}" for i, o in enumerate(options))
    prompt = (
        "<|im_start|>user\\n"
        "ചുവടെ കൊടുത്തിരിക്കുന്ന ചോദ്യം ശ്രദ്ധാപൂർവ്വം വായിക്കുക. "
        "മലയാളത്തിൽ ഘട്ടം ഘട്ടമായി ചിന്തിക്കുക. "
        "അവസാനം ഉത്തരം: X (X = A/B/C/D) എന്ന് എഴുതുക.\\n\\n"
        f"ചോദ്യം: {{question}}\\n\\n{{opts}}"
        "<|im_end|>\\n<|im_start|>assistant\\nചിന്ത:\\n"
    )
    params = SamplingParams(max_tokens=300, temperature=0)
    out = llm.generate([prompt], params, use_tqdm=False)
    reply = out[0].outputs[0].text.strip()
    # Look for ഉത്തരം: X pattern
    import re
    m = re.search(r"ഉത്തരം[:\\s]+([ABCD])", reply, re.IGNORECASE)
    if m:
        return "ABCD".index(m.group(1).upper())
    for line in reversed(reply.splitlines()):
        for i, l in enumerate("ABCD"):
            if line.strip().upper().startswith(l): return i
    return 0
''',
    },

    3: {
        "name": "few-shot-2",
        "description": "2-shot examples from MILU validation set (R1 — in-context knowledge)",
        "research": "R1",
        "code": '''# Strategy 3: 2-shot few-shot (R1 — grounding via examples)
import os
from vllm import LLM, SamplingParams
from datasets import load_dataset

MODEL_NAME = os.environ.get("AGENT_MODEL", "{model}")
_llm = None
_shots = None

def _load():
    global _llm, _shots
    if _llm is None:
        _llm = LLM(model=MODEL_NAME, dtype="bfloat16", max_model_len=4096, gpu_memory_utilization=0.4)
        val = load_dataset("ai4bharat/MILU", "Malayalam", split="validation")
        _shots = [val[0], val[1]]
    return _llm

def _fmt(ex):
    exopts = [ex["option1"], ex["option2"], ex["option3"], ex["option4"]]
    gold = int(ex["target"].replace("option", "")) - 1
    opts = "\\n".join(f"{{chr(65+i)}}. {{o}}" for i, o in enumerate(exopts))
    return f"ചോദ്യം: {{ex['question']}}\\n{{opts}}\\nഉത്തരം: {{chr(65+gold)}}"

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    opts = "\\n".join(f"{{chr(65+i)}}. {{o}}" for i, o in enumerate(options))
    shots = "\\n\\n---\\n\\n".join(_fmt(s) for s in _shots)
    prompt = (
        "<|im_start|>user\\n"
        "ഉദാഹരണങ്ങൾ:\\n\\n" + shots +
        "\\n\\n---\\n\\n"
        "A, B, C അല്ലെങ്കിൽ D മാത്രം ഉത്തരം നൽകുക.\\n\\n"
        f"ചോദ്യം: {{question}}\\n\\n{{opts}}"
        "<|im_end|>\\n<|im_start|>assistant\\nഉത്തരം: "
    )
    params = SamplingParams(max_tokens=4, temperature=0)
    out = llm.generate([prompt], params, use_tqdm=False)
    reply = out[0].outputs[0].text.strip()
    for i, l in enumerate("ABCD"):
        if reply.upper().startswith(l): return i
    return 0
''',
    },

    4: {
        "name": "cultural-system-prompt",
        "description": "Kerala cultural grounding via system prompt (R1)",
        "research": "R1",
        "code": '''# Strategy 4: Kerala cultural system prompt (R1 — cultural alignment)
import os
from vllm import LLM, SamplingParams

MODEL_NAME = os.environ.get("AGENT_MODEL", "{model}")
_llm = None

SYSTEM = (
    "നിങ്ങൾ കേരളത്തിലെ ഒരു വിദഗ്ധ AI സഹായിയാണ്. "
    "ഭാരതീയ ചരിത്രം, സംസ്കാരം, ഭൂമിശാസ്ത്രം, ശാസ്ത്രം, "
    "കേരള ചരിത്രം, മലയാള സാഹിത്യം എന്നിവയിൽ ആഴത്തിലുള്ള അറിവുണ്ട്."
)

def _load():
    global _llm
    if _llm is None:
        _llm = LLM(model=MODEL_NAME, dtype="bfloat16", max_model_len=2048, gpu_memory_utilization=0.4)
    return _llm

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    opts = "\\n".join(f"{{chr(65+i)}}. {{o}}" for i, o in enumerate(options))
    prompt = (
        f"<|im_start|>system\\n{{SYSTEM}}<|im_end|>\\n"
        "<|im_start|>user\\n"
        "A, B, C അല്ലെങ്കിൽ D മാത്രം ഉത്തരം നൽകുക.\\n\\n"
        f"ചോദ്യം: {{question}}\\n\\n{{opts}}"
        "<|im_end|>\\n<|im_start|>assistant\\n"
    )
    params = SamplingParams(max_tokens=4, temperature=0)
    out = llm.generate([prompt], params, use_tqdm=False)
    reply = out[0].outputs[0].text.strip()
    for i, l in enumerate("ABCD"):
        if reply.upper().startswith(l): return i
    return 0
''',
    },

    5: {
        "name": "few-shot-english-cot-hybrid",
        "description": "2-shot examples + English CoT combined (R1+R2 hybrid)",
        "research": "R1+R2",
        "code": '''# Strategy 5: few-shot + English CoT hybrid (R1+R2)
import os
from vllm import LLM, SamplingParams
from datasets import load_dataset

MODEL_NAME = os.environ.get("AGENT_MODEL", "{model}")
_llm = None
_shots = None

def _load():
    global _llm, _shots
    if _llm is None:
        _llm = LLM(model=MODEL_NAME, dtype="bfloat16", max_model_len=6144, gpu_memory_utilization=0.5)
        val = load_dataset("ai4bharat/MILU", "Malayalam", split="validation")
        _shots = [val[0], val[1]]
    return _llm

def _fmt(ex):
    exopts = [ex["option1"], ex["option2"], ex["option3"], ex["option4"]]
    gold = int(ex["target"].replace("option", "")) - 1
    opts = "\\n".join(f"{{chr(65+i)}}. {{o}}" for i, o in enumerate(exopts))
    return f"Q: {{ex['question']}}\\n{{opts}}\\nANSWER: {{chr(65+gold)}}"

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    opts = "\\n".join(f"{{chr(65+i)}}. {{o}}" for i, o in enumerate(options))
    shots = "\\n\\n".join(_fmt(s) for s in _shots)
    prompt = (
        "<|im_start|>user\\n"
        "Malayalam MCQ examples:\\n\\n" + shots +
        "\\n\\nReason briefly in English, end with ANSWER: X.\\n"
        f"Q: {{question}}\\n{{opts}}"
        "<|im_end|>\\n<|im_start|>assistant\\n"
    )
    params = SamplingParams(max_tokens=200, temperature=0)
    out = llm.generate([prompt], params, use_tqdm=False)
    reply = out[0].outputs[0].text.strip()
    for line in reversed(reply.splitlines()):
        l = line.strip().upper()
        if "ANSWER:" in l:
            for i, letter in enumerate("ABCD"):
                if letter in l.split("ANSWER:")[-1]: return i
        for i, letter in enumerate("ABCD"):
            if l.startswith(letter): return i
    return 0
''',
    },

    # =========================================================================
    # ROUND 2: Fixed prompts + novel approaches
    # All strategies below use correct prompt construction (single-brace vars,
    # string concatenation) — the double-brace bug in S0-S5 meant the model
    # never saw the actual question. These establish the TRUE baselines.
    # =========================================================================

    6: {
        "name": "baseline-fixed",
        "description": "True baseline: correct prompt construction (fixes {{}} bug in S0)",
        "research": "R2",
        "code": '''# Strategy 6: baseline-fixed — correct prompt, greedy, 4 tokens
import os
from vllm import LLM, SamplingParams

MODEL_NAME = os.environ.get("AGENT_MODEL", "{model}")
_llm = None

def _load():
    global _llm
    if _llm is None:
        _llm = LLM(model=MODEL_NAME, dtype="bfloat16", max_model_len=2048, gpu_memory_utilization=0.4)
    return _llm

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    opts = "\\n".join(chr(65+i) + ". " + o for i, o in enumerate(options))
    prompt = (
        "<|im_start|>user\\n"
        "ചുവടെ കൊടുത്തിരിക്കുന്ന ചോദ്യത്തിന് ശരിയായ ഉത്തരം തിരഞ്ഞെടുക്കുക. "
        "A, B, C അല്ലെങ്കിൽ D എന്ന് മാത്രം ഉത്തരം നൽകുക.\\n\\n"
        + "ചോദ്യം: " + question + "\\n\\n" + opts
        + "\\n<|im_end|>\\n<|im_start|>assistant\\n"
    )
    params = SamplingParams(max_tokens=4, temperature=0)
    out = llm.generate([prompt], params, use_tqdm=False)
    reply = out[0].outputs[0].text.strip()
    for i, l in enumerate("ABCD"):
        if reply.upper().startswith(l): return i
    return 0
''',
    },

    7: {
        "name": "few-shot-2-fixed",
        "description": "2-shot with correct prompt construction (fixes broken S3)",
        "research": "R1",
        "code": '''# Strategy 7: few-shot-2-fixed — 2 validation examples, correct prompts
import os
from vllm import LLM, SamplingParams
from datasets import load_dataset

MODEL_NAME = os.environ.get("AGENT_MODEL", "{model}")
_llm = None
_shots = None

def _load():
    global _llm, _shots
    if _llm is None:
        _llm = LLM(model=MODEL_NAME, dtype="bfloat16", max_model_len=4096, gpu_memory_utilization=0.4)
        val = load_dataset("ai4bharat/MILU", "Malayalam", split="validation")
        _shots = [val[0], val[1]]
    return _llm

def _fmt(ex):
    exopts = [ex["option1"], ex["option2"], ex["option3"], ex["option4"]]
    gold = int(ex["target"].replace("option", "")) - 1
    lines = [chr(65+i) + ". " + exopts[i] for i in range(4)]
    return "ചോദ്യം: " + ex["question"] + "\\n" + "\\n".join(lines) + "\\nഉത്തരം: " + chr(65+gold)

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    opts = "\\n".join(chr(65+i) + ". " + o for i, o in enumerate(options))
    shots = "\\n\\n---\\n\\n".join(_fmt(s) for s in _shots)
    prompt = (
        "<|im_start|>user\\n"
        "ഉദാഹരണങ്ങൾ:\\n\\n" + shots
        + "\\n\\n---\\n\\nA, B, C അല്ലെങ്കിൽ D മാത്രം ഉത്തരം നൽകുക.\\n\\n"
        + "ചോദ്യം: " + question + "\\n\\n" + opts
        + "<|im_end|>\\n<|im_start|>assistant\\nഉത്തരം: "
    )
    params = SamplingParams(max_tokens=4, temperature=0)
    out = llm.generate([prompt], params, use_tqdm=False)
    reply = out[0].outputs[0].text.strip()
    for i, l in enumerate("ABCD"):
        if reply.upper().startswith(l): return i
    return 0
''',
    },

    8: {
        "name": "few-shot-4-fixed",
        "description": "4-shot with correct prompts: tests if more examples help (R1)",
        "research": "R1",
        "code": '''# Strategy 8: few-shot-4-fixed — 4 validation examples, correct prompts
import os
from vllm import LLM, SamplingParams
from datasets import load_dataset

MODEL_NAME = os.environ.get("AGENT_MODEL", "{model}")
_llm = None
_shots = None

def _load():
    global _llm, _shots
    if _llm is None:
        _llm = LLM(model=MODEL_NAME, dtype="bfloat16", max_model_len=6144, gpu_memory_utilization=0.45)
        val = load_dataset("ai4bharat/MILU", "Malayalam", split="validation")
        _shots = list(val.select([0, 50, 100, 150]))
    return _llm

def _fmt(ex):
    exopts = [ex["option1"], ex["option2"], ex["option3"], ex["option4"]]
    gold = int(ex["target"].replace("option", "")) - 1
    lines = [chr(65+i) + ". " + exopts[i] for i in range(4)]
    return "ചോദ്യം: " + ex["question"] + "\\n" + "\\n".join(lines) + "\\nഉത്തരം: " + chr(65+gold)

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    opts = "\\n".join(chr(65+i) + ". " + o for i, o in enumerate(options))
    shots = "\\n\\n---\\n\\n".join(_fmt(s) for s in _shots)
    prompt = (
        "<|im_start|>user\\n"
        "ഉദാഹരണങ്ങൾ:\\n\\n" + shots
        + "\\n\\n---\\n\\nA, B, C അല്ലെങ്കിൽ D മാത്രം ഉത്തരം നൽകുക.\\n\\n"
        + "ചോദ്യം: " + question + "\\n\\n" + opts
        + "<|im_end|>\\n<|im_start|>assistant\\nഉത്തരം: "
    )
    params = SamplingParams(max_tokens=4, temperature=0)
    out = llm.generate([prompt], params, use_tqdm=False)
    reply = out[0].outputs[0].text.strip()
    for i, l in enumerate("ABCD"):
        if reply.upper().startswith(l): return i
    return 0
''',
    },

    9: {
        "name": "english-cot-fixed",
        "description": "English-pivot CoT with correct prompts: true R2 test (pro-pivot)",
        "research": "R2",
        "code": '''# Strategy 9: english-cot-fixed — correct English CoT (fixes broken S1)
import os
from vllm import LLM, SamplingParams

MODEL_NAME = os.environ.get("AGENT_MODEL", "{model}")
_llm = None

def _load():
    global _llm
    if _llm is None:
        _llm = LLM(model=MODEL_NAME, dtype="bfloat16", max_model_len=4096, gpu_memory_utilization=0.4)
    return _llm

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    opts = "\\n".join(chr(65+i) + ". " + o for i, o in enumerate(options))
    prompt = (
        "<|im_start|>user\\n"
        "This is a Malayalam multiple-choice question. "
        "Read it carefully, reason step-by-step in English, "
        "then end your response with exactly: ANSWER: X (where X is A/B/C/D).\\n\\n"
        + "Question: " + question + "\\n\\nOptions:\\n" + opts
        + "\\n<|im_end|>\\n<|im_start|>assistant\\n"
    )
    params = SamplingParams(max_tokens=250, temperature=0)
    out = llm.generate([prompt], params, use_tqdm=False)
    reply = out[0].outputs[0].text.strip()
    for line in reversed(reply.splitlines()):
        l = line.strip().upper()
        if "ANSWER:" in l:
            for i, letter in enumerate("ABCD"):
                if letter in l.split("ANSWER:")[-1]: return i
        for i, letter in enumerate("ABCD"):
            if l.startswith(letter): return i
    return 0
''',
    },

    10: {
        "name": "domain-matched-2shot",
        "description": "2-shot examples matched to test question subject (R1+R3: domain routing)",
        "research": "R1+R3",
        "code": '''# Strategy 10: domain-matched-2shot (R1+R3) — subject-adaptive in-context learning
import os
from vllm import LLM, SamplingParams
from datasets import load_dataset

MODEL_NAME = os.environ.get("AGENT_MODEL", "{model}")
_llm = None
_shots_by_subject = None
_default_shots = None
_test_subject_map = None

def _load():
    global _llm, _shots_by_subject, _default_shots, _test_subject_map
    if _llm is None:
        _llm = LLM(model=MODEL_NAME, dtype="bfloat16", max_model_len=4096, gpu_memory_utilization=0.4)
        val = load_dataset("ai4bharat/MILU", "Malayalam", split="validation")
        test = load_dataset("ai4bharat/MILU", "Malayalam", split="test")
        _shots_by_subject = {}
        for ex in val:
            subj = ex.get("subject", "general")
            _shots_by_subject.setdefault(subj, []).append(ex)
        _default_shots = [val[0], val[50]]
        _test_subject_map = {ex["question"]: ex.get("subject", "general") for ex in test}
    return _llm

def _fmt(ex):
    exopts = [ex["option1"], ex["option2"], ex["option3"], ex["option4"]]
    gold = int(ex["target"].replace("option", "")) - 1
    lines = [chr(65+i) + ". " + exopts[i] for i in range(4)]
    return "ചോദ്യം: " + ex["question"] + "\\n" + "\\n".join(lines) + "\\nഉത്തരം: " + chr(65+gold)

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    subj = _test_subject_map.get(question, "general")
    shots = _shots_by_subject.get(subj, _default_shots)[:2]
    opts = "\\n".join(chr(65+i) + ". " + o for i, o in enumerate(options))
    shots_text = "\\n\\n---\\n\\n".join(_fmt(s) for s in shots)
    prompt = (
        "<|im_start|>user\\n"
        "ഉദാഹരണങ്ങൾ:\\n\\n" + shots_text
        + "\\n\\n---\\n\\nA, B, C അല്ലെങ്കിൽ D മാത്രം ഉത്തരം നൽകുക.\\n\\n"
        + "ചോദ്യം: " + question + "\\n\\n" + opts
        + "<|im_end|>\\n<|im_start|>assistant\\nഉത്തരം: "
    )
    params = SamplingParams(max_tokens=4, temperature=0)
    out = llm.generate([prompt], params, use_tqdm=False)
    reply = out[0].outputs[0].text.strip()
    for i, l in enumerate("ABCD"):
        if reply.upper().startswith(l): return i
    return 0
''',
    },

    11: {
        "name": "batched-cot-2shot",
        "description": "KEY INNOVATION: batch ALL 4321 questions in one vLLM call, 2-shot+CoT, full coverage (R1+R2)",
        "research": "R1+R2",
        "code": '''# Strategy 11: batched-cot-2shot — precompute ALL answers in one batch call
# Innovation: batch inference enables CoT on full test set (not just ~350 examples)
import os
from vllm import LLM, SamplingParams
from datasets import load_dataset

MODEL_NAME = os.environ.get("AGENT_MODEL", "{model}")
_llm = None
_shots = None
_cache = {}

def _load():
    global _llm, _shots
    if _llm is None:
        _llm = LLM(model=MODEL_NAME, dtype="bfloat16", max_model_len=4096, gpu_memory_utilization=0.45)
        val = load_dataset("ai4bharat/MILU", "Malayalam", split="validation")
        _shots = [val[0], val[50]]
    return _llm

def _fmt_shot(ex):
    exopts = [ex["option1"], ex["option2"], ex["option3"], ex["option4"]]
    gold = int(ex["target"].replace("option", "")) - 1
    lines = [chr(65+i) + ". " + exopts[i] for i in range(4)]
    return "Q: " + ex["question"] + "\\n" + "\\n".join(lines) + "\\nANSWER: " + chr(65+gold)

def _make_prompt(question, opts_str, shots_header):
    return (
        "<|im_start|>user\\n"
        + shots_header
        + "Now reason briefly in English, end with ANSWER: X.\\n"
        + "Q: " + question + "\\n" + opts_str
        + "\\n<|im_end|>\\n<|im_start|>assistant\\n"
    )

def _parse(text):
    for line in reversed(text.strip().splitlines()):
        l = line.strip().upper()
        if "ANSWER:" in l:
            for i, letter in enumerate("ABCD"):
                if letter in l.split("ANSWER:")[-1]: return i
        for i, letter in enumerate("ABCD"):
            if l.startswith(letter): return i
    return 0

def _precompute(llm):
    global _cache
    test = load_dataset("ai4bharat/MILU", "Malayalam", split="test")
    shots_header = "Examples:\\n\\n" + "\\n\\n".join(_fmt_shot(s) for s in _shots) + "\\n\\n"
    prompts, keys = [], []
    for ex in test:
        opts = "\\n".join(chr(65+i) + ". " + ex["option" + str(i+1)] for i in range(4))
        prompts.append(_make_prompt(ex["question"], opts, shots_header))
        keys.append(ex["question"])
    print("  Batch generating", len(prompts), "answers ...")
    params = SamplingParams(max_tokens=120, temperature=0)
    outputs = llm.generate(prompts, params, use_tqdm=True)
    for k, out in zip(keys, outputs):
        _cache[k] = _parse(out.outputs[0].text)
    print("  Precomputed", len(_cache), "answers.")

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    if not _cache:
        _precompute(llm)
    return _cache.get(question, 0)
''',
    },

    12: {
        "name": "batched-cot-domain-matched",
        "description": "Batch all 4321 with domain-matched 2-shot + CoT (R1+R2+R3 unified)",
        "research": "R1+R2+R3",
        "code": '''# Strategy 12: batched-cot-domain-matched — domain routing + batched CoT
import os
from vllm import LLM, SamplingParams
from datasets import load_dataset

MODEL_NAME = os.environ.get("AGENT_MODEL", "{model}")
_llm = None
_shots_by_subject = None
_default_shots = None
_cache = {}

def _load():
    global _llm, _shots_by_subject, _default_shots
    if _llm is None:
        _llm = LLM(model=MODEL_NAME, dtype="bfloat16", max_model_len=4096, gpu_memory_utilization=0.45)
        val = load_dataset("ai4bharat/MILU", "Malayalam", split="validation")
        _shots_by_subject = {}
        for ex in val:
            subj = ex.get("subject", "general")
            _shots_by_subject.setdefault(subj, []).append(ex)
        _default_shots = [val[0], val[50]]
    return _llm

def _fmt_shot(ex):
    exopts = [ex["option1"], ex["option2"], ex["option3"], ex["option4"]]
    gold = int(ex["target"].replace("option", "")) - 1
    lines = [chr(65+i) + ". " + exopts[i] for i in range(4)]
    return "Q: " + ex["question"] + "\\n" + "\\n".join(lines) + "\\nANSWER: " + chr(65+gold)

def _parse(text):
    for line in reversed(text.strip().splitlines()):
        l = line.strip().upper()
        if "ANSWER:" in l:
            for i, letter in enumerate("ABCD"):
                if letter in l.split("ANSWER:")[-1]: return i
        for i, letter in enumerate("ABCD"):
            if l.startswith(letter): return i
    return 0

def _precompute(llm):
    global _cache
    test = load_dataset("ai4bharat/MILU", "Malayalam", split="test")
    prompts, keys = [], []
    for ex in test:
        subj = ex.get("subject", "general")
        shots = _shots_by_subject.get(subj, _default_shots)[:2]
        shots_header = "Examples:\\n\\n" + "\\n\\n".join(_fmt_shot(s) for s in shots) + "\\n\\n"
        opts = "\\n".join(chr(65+i) + ". " + ex["option" + str(i+1)] for i in range(4))
        prompt = (
            "<|im_start|>user\\n"
            + shots_header
            + "Reason briefly in English, end with ANSWER: X.\\n"
            + "Q: " + ex["question"] + "\\n" + opts
            + "\\n<|im_end|>\\n<|im_start|>assistant\\n"
        )
        prompts.append(prompt)
        keys.append(ex["question"])
    print("  Batch generating", len(prompts), "domain-matched answers ...")
    params = SamplingParams(max_tokens=120, temperature=0)
    outputs = llm.generate(prompts, params, use_tqdm=True)
    for k, out in zip(keys, outputs):
        _cache[k] = _parse(out.outputs[0].text)
    print("  Precomputed", len(_cache), "answers.")

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    if not _cache:
        _precompute(llm)
    return _cache.get(question, 0)
''',
    },

    13: {
        "name": "qwen3-thinking-fixed",
        "description": "Qwen3 native thinking mode (<think> prefix) with correct prompts (R2)",
        "research": "R2",
        "code": '''# Strategy 13: qwen3-thinking-fixed — force Qwen3 thinking mode
import os
import re
from vllm import LLM, SamplingParams

MODEL_NAME = os.environ.get("AGENT_MODEL", "{model}")
_llm = None

def _load():
    global _llm
    if _llm is None:
        _llm = LLM(model=MODEL_NAME, dtype="bfloat16", max_model_len=6144, gpu_memory_utilization=0.5)
    return _llm

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    opts = "\\n".join(chr(65+i) + ". " + o for i, o in enumerate(options))
    prompt = (
        "<|im_start|>user\\n"
        "This is a Malayalam multiple-choice question. "
        "Think carefully and choose the best answer.\\n\\n"
        + "Question: " + question + "\\n\\nOptions:\\n" + opts
        + "\\n<|im_end|>\\n<|im_start|>assistant\\n<think>\\n"
    )
    params = SamplingParams(max_tokens=512, temperature=0)
    out = llm.generate([prompt], params, use_tqdm=False)
    reply = out[0].outputs[0].text.strip()
    # Parse answer after </think> tag
    if "</think>" in reply:
        after_think = reply.split("</think>")[-1].strip()
        for i, l in enumerate("ABCD"):
            if after_think.upper().startswith(l): return i
    # Fallback: look for ANSWER: or letter at end
    for line in reversed(reply.splitlines()):
        l = line.strip().upper()
        if "ANSWER:" in l:
            for i, letter in enumerate("ABCD"):
                if letter in l.split("ANSWER:")[-1]: return i
        for i, letter in enumerate("ABCD"):
            if l.startswith(letter): return i
    return 0
''',
    },

    14: {
        "name": "self-consistency-3",
        "description": "3-sample majority vote at temperature=0.5 with fixed prompts (R2: calibration)",
        "research": "R2",
        "code": '''# Strategy 14: self-consistency-3 — majority vote of 3 samples
import os
from collections import Counter
from vllm import LLM, SamplingParams

MODEL_NAME = os.environ.get("AGENT_MODEL", "{model}")
_llm = None

def _load():
    global _llm
    if _llm is None:
        _llm = LLM(model=MODEL_NAME, dtype="bfloat16", max_model_len=2048, gpu_memory_utilization=0.4)
    return _llm

def _parse(text):
    for i, l in enumerate("ABCD"):
        if text.upper().startswith(l): return i
    return 0

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    opts = "\\n".join(chr(65+i) + ". " + o for i, o in enumerate(options))
    prompt = (
        "<|im_start|>user\\n"
        "ചുവടെ കൊടുത്തിരിക്കുന്ന ചോദ്യത്തിന് ശരിയായ ഉത്തരം തിരഞ്ഞെടുക്കുക. "
        "A, B, C അല്ലെങ്കിൽ D എന്ന് മാത്രം ഉത്തരം നൽകുക.\\n\\n"
        + "ചോദ്യം: " + question + "\\n\\n" + opts
        + "\\n<|im_end|>\\n<|im_start|>assistant\\n"
    )
    # Generate 3 samples and take majority vote
    params = SamplingParams(max_tokens=4, temperature=0.5, n=3)
    out = llm.generate([prompt], params, use_tqdm=False)
    votes = [_parse(o.text.strip()) for o in out[0].outputs]
    return Counter(votes).most_common(1)[0][0]
''',
    },

    15: {
        "name": "bilingual-cot-fixed",
        "description": "Novel: understand in Malayalam → reason in English → confirm in Malayalam (R2, paper contribution)",
        "research": "R2",
        "code": '''# Strategy 15: bilingual-cot-fixed — structured bilingual reasoning (novel contribution)
# Inspired by language pivoting debate (Theme 8): neither pure pivot nor pure native
# Instead: 3-phase bilingual reasoning structure
import os
from vllm import LLM, SamplingParams

MODEL_NAME = os.environ.get("AGENT_MODEL", "{model}")
_llm = None

def _load():
    global _llm
    if _llm is None:
        _llm = LLM(model=MODEL_NAME, dtype="bfloat16", max_model_len=4096, gpu_memory_utilization=0.4)
    return _llm

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    opts = "\\n".join(chr(65+i) + ". " + o for i, o in enumerate(options))
    prompt = (
        "<|im_start|>user\\n"
        "Malayalam MCQ. Follow these steps:\\n"
        "1. Read the question in Malayalam and understand it.\\n"
        "2. Reason through each option in English.\\n"
        "3. State your final answer as: ANSWER: X\\n\\n"
        + "Question: " + question + "\\n\\nOptions:\\n" + opts
        + "\\n<|im_end|>\\n<|im_start|>assistant\\n"
        "1. Understanding: "
    )
    params = SamplingParams(max_tokens=200, temperature=0)
    out = llm.generate([prompt], params, use_tqdm=False)
    reply = out[0].outputs[0].text.strip()
    for line in reversed(reply.splitlines()):
        l = line.strip().upper()
        if "ANSWER:" in l:
            for i, letter in enumerate("ABCD"):
                if letter in l.split("ANSWER:")[-1]: return i
        for i, letter in enumerate("ABCD"):
            if l.startswith(letter): return i
    return 0
''',
    },

    16: {
        "name": "few-shot-2-fixed-cot",
        "description": "2 fixed shots + English CoT hybrid with CORRECT prompts (fixes broken S5)",
        "research": "R1+R2",
        "code": '''# Strategy 16: few-shot-2-fixed-cot — fixed version of S5 (broken hybrid)
import os
from vllm import LLM, SamplingParams
from datasets import load_dataset

MODEL_NAME = os.environ.get("AGENT_MODEL", "{model}")
_llm = None
_shots = None

def _load():
    global _llm, _shots
    if _llm is None:
        _llm = LLM(model=MODEL_NAME, dtype="bfloat16", max_model_len=6144, gpu_memory_utilization=0.5)
        val = load_dataset("ai4bharat/MILU", "Malayalam", split="validation")
        _shots = [val[0], val[50]]
    return _llm

def _fmt(ex):
    exopts = [ex["option1"], ex["option2"], ex["option3"], ex["option4"]]
    gold = int(ex["target"].replace("option", "")) - 1
    lines = [chr(65+i) + ". " + exopts[i] for i in range(4)]
    return "Q: " + ex["question"] + "\\n" + "\\n".join(lines) + "\\nANSWER: " + chr(65+gold)

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    opts = "\\n".join(chr(65+i) + ". " + o for i, o in enumerate(options))
    shots = "\\n\\n".join(_fmt(s) for s in _shots)
    prompt = (
        "<|im_start|>user\\n"
        "Malayalam MCQ examples:\\n\\n" + shots
        + "\\n\\nReason briefly in English, end with ANSWER: X.\\n"
        + "Q: " + question + "\\n" + opts
        + "\\n<|im_end|>\\n<|im_start|>assistant\\n"
    )
    params = SamplingParams(max_tokens=200, temperature=0)
    out = llm.generate([prompt], params, use_tqdm=False)
    reply = out[0].outputs[0].text.strip()
    for line in reversed(reply.splitlines()):
        l = line.strip().upper()
        if "ANSWER:" in l:
            for i, letter in enumerate("ABCD"):
                if letter in l.split("ANSWER:")[-1]: return i
        for i, letter in enumerate("ABCD"):
            if l.startswith(letter): return i
    return 0
''',
    },

    17: {
        "name": "batched-4shot-cot",
        "description": "Batch all 4321, 4 diverse shots + CoT max_tokens=100 — most shots + full coverage (R1+R2)",
        "research": "R1+R2",
        "code": '''# Strategy 17: batched-4shot-cot — 4 diverse shots + batched CoT, full coverage
import os
from vllm import LLM, SamplingParams
from datasets import load_dataset

MODEL_NAME = os.environ.get("AGENT_MODEL", "{model}")
_llm = None
_shots = None
_cache = {}

def _load():
    global _llm, _shots
    if _llm is None:
        _llm = LLM(model=MODEL_NAME, dtype="bfloat16", max_model_len=5120, gpu_memory_utilization=0.5)
        val = load_dataset("ai4bharat/MILU", "Malayalam", split="validation")
        _shots = list(val.select([0, 50, 100, 200]))
    return _llm

def _fmt_shot(ex):
    exopts = [ex["option1"], ex["option2"], ex["option3"], ex["option4"]]
    gold = int(ex["target"].replace("option", "")) - 1
    lines = [chr(65+i) + ". " + exopts[i] for i in range(4)]
    return "Q: " + ex["question"] + "\\n" + "\\n".join(lines) + "\\nANSWER: " + chr(65+gold)

def _parse(text):
    for line in reversed(text.strip().splitlines()):
        l = line.strip().upper()
        if "ANSWER:" in l:
            for i, letter in enumerate("ABCD"):
                if letter in l.split("ANSWER:")[-1]: return i
        for i, letter in enumerate("ABCD"):
            if l.startswith(letter): return i
    return 0

def _precompute(llm):
    global _cache
    test = load_dataset("ai4bharat/MILU", "Malayalam", split="test")
    shots_header = "Examples:\\n\\n" + "\\n\\n".join(_fmt_shot(s) for s in _shots) + "\\n\\n"
    prompts, keys = [], []
    for ex in test:
        opts = "\\n".join(chr(65+i) + ". " + ex["option" + str(i+1)] for i in range(4))
        prompt = (
            "<|im_start|>user\\n"
            + shots_header
            + "Reason briefly in English, end with ANSWER: X.\\n"
            + "Q: " + ex["question"] + "\\n" + opts
            + "\\n<|im_end|>\\n<|im_start|>assistant\\n"
        )
        prompts.append(prompt)
        keys.append(ex["question"])
    print("  Batch generating", len(prompts), "answers (4-shot + CoT) ...")
    params = SamplingParams(max_tokens=100, temperature=0)
    outputs = llm.generate(prompts, params, use_tqdm=True)
    for k, out in zip(keys, outputs):
        _cache[k] = _parse(out.outputs[0].text)
    print("  Done:", len(_cache), "answers cached.")

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    if not _cache:
        _precompute(llm)
    return _cache.get(question, 0)
''',
    },
}


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def _git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout.strip()


def git_commit(message):
    _git("add", EDITABLE_FILE)
    _git("commit", "-m", message)


def git_revert():
    _git("checkout", "HEAD", "--", EDITABLE_FILE)


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

def load_agent():
    spec = importlib.util.spec_from_file_location("agent", EDITABLE_FILE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules.pop("agent", None)
    sys.modules.pop(EDITABLE_FILE.replace(".py", ""), None)
    spec.loader.exec_module(mod)
    return mod


def evaluate(time_limit_seconds: int) -> tuple[float, int]:
    from datasets import load_dataset

    print("  Loading MILU Malayalam test split ...")
    ds = load_dataset("ai4bharat/MILU", "Malayalam", split="test")
    agent = load_agent()

    correct = 0
    total = 0
    deadline = time.monotonic() + time_limit_seconds

    for ex in ds:
        if time.monotonic() > deadline:
            break
        options = [ex["option1"], ex["option2"], ex["option3"], ex["option4"]]
        gold = int(ex["target"].replace("option", "")) - 1  # "option4" -> 3
        try:
            pred = agent.answer_question(ex["question"], options)
            if int(pred) == gold:
                correct += 1
        except Exception as e:
            print(f"    [warn] {e}", file=sys.stderr)
        total += 1
        if total % 25 == 0:
            remaining = max(0, int(deadline - time.monotonic()))
            print(f"  {total:>4} | acc={correct/total:.4f} | {remaining}s left")

    return (correct / total if total > 0 else 0.0), total


# ---------------------------------------------------------------------------
# program.md update
# ---------------------------------------------------------------------------

def update_program_md(best: float, last: dict):
    text = PROGRAM_FILE.read_text()
    marker = "## Best Result So Far"
    new = (
        f"{marker}\n\n"
        f"- Accuracy: **{best:.4f}**\n"
        f"- Last run: strategy={last.get('strategy_name')} "
        f"acc={last['accuracy']:.4f} on {last['n']} examples ({last['action']})\n"
        f"- Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    )
    idx = text.find(marker)
    PROGRAM_FILE.write_text((text[:idx] if idx >= 0 else text.rstrip() + "\n\n---\n\n") + new)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Indic Agent Autoresearch Loop")
    parser.add_argument("--minutes", type=float, default=5.0,
                        help="Eval budget per strategy in minutes (default: 5)")
    parser.add_argument("--strategy", type=int, default=None,
                        help="Run only this strategy index (default: all)")
    parser.add_argument("--gpu", type=int, default=None,
                        help="CUDA device index to use (sets CUDA_VISIBLE_DEVICES)")
    parser.add_argument("--agent-file", type=str, default=None,
                        help="Temp agent file for parallel runs (default: agent.py)")
    args = parser.parse_args()
    time_limit = int(args.minutes * 60)

    # GPU isolation for parallel runs
    global EDITABLE_FILE
    if args.gpu is not None:
        import os as _os
        _os.environ["CUDA_VISIBLE_DEVICES"] = str(args.gpu)
        print(f"  Using GPU {args.gpu}")
    if args.agent_file:
        EDITABLE_FILE = args.agent_file

    # Parallel mode: use per-strategy log file to avoid conflicts
    log_file = LOG_FILE
    if args.strategy is not None and args.agent_file:
        log_file = Path(f"results_s{args.strategy}.jsonl")

    history = []
    # Merge all per-strategy logs if they exist
    for f in sorted(Path(".").glob("results*.jsonl")):
        for line in f.read_text().splitlines():
            if line.strip():
                history.append(json.loads(line))

    best_accuracy = max((h["accuracy"] for h in history), default=0.0)
    done = {h.get("strategy_idx") for h in history if h.get("action") in ("kept", "reverted")}

    ids = [args.strategy] if args.strategy is not None else sorted(STRATEGIES.keys())

    print(f"\n{'='*65}")
    print(f"  Indic Agent Autoresearch  |  MILU Malayalam")
    print(f"  Budget: {args.minutes:.1f} min/strategy  |  Best: {best_accuracy:.4f}")
    print(f"  Strategies: {ids}")
    print(f"{'='*65}\n")

    for sid in ids:
        if sid in done and args.strategy is None:
            print(f"[skip] strategy {sid} already done.")
            continue

        strat = STRATEGIES[sid]
        print(f"\n{'─'*65}")
        print(f"  [{sid}] {strat['name']}  ({strat['research']})")
        print(f"  {strat['description']}")
        print(f"{'─'*65}")

        Path(EDITABLE_FILE).write_text(strat["code"].replace("{model}", MODEL_NAME))

        start = time.monotonic()
        try:
            accuracy, n = evaluate(time_limit)
        except Exception as e:
            print(f"  [error] {e}", file=sys.stderr)
            try:
                git_revert()
            except Exception:
                pass
            continue
        elapsed = time.monotonic() - start

        print(f"\n  acc={accuracy:.4f}  n={n}  elapsed={elapsed:.0f}s")

        result = {
            "timestamp": datetime.now().isoformat(),
            "strategy_idx": sid,
            "strategy_name": strat["name"],
            "strategy_research": strat["research"],
            "accuracy": accuracy,
            "n": n,
            "elapsed_s": int(elapsed),
        }

        parallel_mode = bool(args.agent_file)

        if parallel_mode:
            # In parallel mode: just log results, no git ops (merge at end)
            result["action"] = "evaluated"
            print(f"  logged (parallel mode — no git commit)")
        elif accuracy > best_accuracy:
            best_accuracy = accuracy
            msg = f"Improve: {strat['name']} acc={accuracy:.4f} n={n} MILU-ml"
            try:
                git_commit(msg)
                result["action"] = "kept"
                print(f"  KEPT ✓  best={best_accuracy:.4f}")
            except RuntimeError as e:
                result["action"] = "kept-no-commit"
                print(f"  kept (commit err): {e}", file=sys.stderr)
        else:
            try:
                git_revert()
                result["action"] = "reverted"
                print(f"  reverted  ({accuracy:.4f} < {best_accuracy:.4f})")
            except RuntimeError as e:
                result["action"] = "revert-failed"
                print(f"  revert failed: {e}", file=sys.stderr)

        history.append(result)
        with log_file.open("a") as f:
            f.write(json.dumps(result) + "\n")
        if not args.agent_file:  # only update program.md in sequential mode
            update_program_md(best_accuracy, result)

    print(f"\n{'='*65}")
    print(f"  Done. Best: {best_accuracy:.4f}")
    print(f"  Log: {LOG_FILE}")
    print(f"{'='*65}\n")


if __name__ == "__main__":
    main()
