# Strategy 1: English-pivot CoT (R2 — pro-pivot, like PLUG/Semantic Pivots)
import os
from vllm import LLM, SamplingParams

MODEL_NAME = os.environ.get("AGENT_MODEL", "Qwen/Qwen3-1.7B")
_llm = None

def _load():
    global _llm
    if _llm is None:
        _llm = LLM(model=MODEL_NAME, dtype="bfloat16", max_model_len=4096, gpu_memory_utilization=0.4)
    return _llm

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    opts = "\n".join(f"{{chr(65+i)}}. {{o}}" for i, o in enumerate(options))
    prompt = (
        "<|im_start|>user\n"
        "This is a Malayalam multiple-choice question. Reason step-by-step in English, "
        "then on the LAST LINE write only: ANSWER: X (where X is A/B/C/D).\n\n"
        f"Question (Malayalam): {{question}}\n\nOptions:\n{{opts}}"
        "<|im_end|>\n<|im_start|>assistant\n"
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
