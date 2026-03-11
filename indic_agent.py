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
MODEL_NAME = "Qwen/Qwen3.5-2B"

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
    args = parser.parse_args()
    time_limit = int(args.minutes * 60)

    history = []
    if LOG_FILE.exists():
        for line in LOG_FILE.read_text().splitlines():
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

        if accuracy > best_accuracy:
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
        with LOG_FILE.open("a") as f:
            f.write(json.dumps(result) + "\n")
        update_program_md(best_accuracy, result)

    print(f"\n{'='*65}")
    print(f"  Done. Best: {best_accuracy:.4f}")
    print(f"  Log: {LOG_FILE}")
    print(f"{'='*65}\n")


if __name__ == "__main__":
    main()
