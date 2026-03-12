# Strategy 4: Kerala cultural system prompt (R1 — cultural alignment)
import os
from vllm import LLM, SamplingParams

MODEL_NAME = os.environ.get("AGENT_MODEL", "Qwen/Qwen3-1.7B")
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
    opts = "\n".join(f"{{chr(65+i)}}. {{o}}" for i, o in enumerate(options))
    prompt = (
        f"<|im_start|>system\n{{SYSTEM}}<|im_end|>\n"
        "<|im_start|>user\n"
        "A, B, C അല്ലെങ്കിൽ D മാത്രം ഉത്തരം നൽകുക.\n\n"
        f"ചോദ്യം: {{question}}\n\n{{opts}}"
        "<|im_end|>\n<|im_start|>assistant\n"
    )
    params = SamplingParams(max_tokens=4, temperature=0)
    out = llm.generate([prompt], params, use_tqdm=False)
    reply = out[0].outputs[0].text.strip()
    for i, l in enumerate("ABCD"):
        if reply.upper().startswith(l): return i
    return 0
