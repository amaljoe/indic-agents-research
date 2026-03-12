# Strategy 2: Native Malayalam CoT (R2 — anti-pivot, Think Natively / M-Thinker style)
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
        "ചുവടെ കൊടുത്തിരിക്കുന്ന ചോദ്യം ശ്രദ്ധാപൂർവ്വം വായിക്കുക. "
        "മലയാളത്തിൽ ഘട്ടം ഘട്ടമായി ചിന്തിക്കുക. "
        "അവസാനം ഉത്തരം: X (X = A/B/C/D) എന്ന് എഴുതുക.\n\n"
        f"ചോദ്യം: {{question}}\n\n{{opts}}"
        "<|im_end|>\n<|im_start|>assistant\nചിന്ത:\n"
    )
    params = SamplingParams(max_tokens=300, temperature=0)
    out = llm.generate([prompt], params, use_tqdm=False)
    reply = out[0].outputs[0].text.strip()
    # Look for ഉത്തരം: X pattern
    import re
    m = re.search(r"ഉത്തരം[:\s]+([ABCD])", reply, re.IGNORECASE)
    if m:
        return "ABCD".index(m.group(1).upper())
    for line in reversed(reply.splitlines()):
        for i, l in enumerate("ABCD"):
            if line.strip().upper().startswith(l): return i
    return 0
