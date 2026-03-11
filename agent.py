# Strategy 3: 2-shot few-shot (R1 — grounding via examples)
import os
from vllm import LLM, SamplingParams
from datasets import load_dataset

MODEL_NAME = os.environ.get("AGENT_MODEL", "Qwen/Qwen3-1.7B")
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
    opts = "\n".join(f"{{chr(65+i)}}. {{o}}" for i, o in enumerate(exopts))
    return f"ചോദ്യം: {{ex['question']}}\n{{opts}}\nഉത്തരം: {{chr(65+gold)}}"

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    opts = "\n".join(f"{{chr(65+i)}}. {{o}}" for i, o in enumerate(options))
    shots = "\n\n---\n\n".join(_fmt(s) for s in _shots)
    prompt = (
        "<|im_start|>user\n"
        "ഉദാഹരണങ്ങൾ:\n\n" + shots +
        "\n\n---\n\n"
        "A, B, C അല്ലെങ്കിൽ D മാത്രം ഉത്തരം നൽകുക.\n\n"
        f"ചോദ്യം: {{question}}\n\n{{opts}}"
        "<|im_end|>\n<|im_start|>assistant\nഉത്തരം: "
    )
    params = SamplingParams(max_tokens=4, temperature=0)
    out = llm.generate([prompt], params, use_tqdm=False)
    reply = out[0].outputs[0].text.strip()
    for i, l in enumerate("ABCD"):
        if reply.upper().startswith(l): return i
    return 0
