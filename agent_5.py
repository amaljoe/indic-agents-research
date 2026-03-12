# Strategy 5: few-shot + English CoT hybrid (R1+R2)
import os
from vllm import LLM, SamplingParams
from datasets import load_dataset

MODEL_NAME = os.environ.get("AGENT_MODEL", "Qwen/Qwen3-1.7B")
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
    opts = "\n".join(f"{{chr(65+i)}}. {{o}}" for i, o in enumerate(exopts))
    return f"Q: {{ex['question']}}\n{{opts}}\nANSWER: {{chr(65+gold)}}"

def answer_question(question: str, options: list[str]) -> int:
    llm = _load()
    opts = "\n".join(f"{{chr(65+i)}}. {{o}}" for i, o in enumerate(options))
    shots = "\n\n".join(_fmt(s) for s in _shots)
    prompt = (
        "<|im_start|>user\n"
        "Malayalam MCQ examples:\n\n" + shots +
        "\n\nReason briefly in English, end with ANSWER: X.\n"
        f"Q: {{question}}\n{{opts}}"
        "<|im_end|>\n<|im_start|>assistant\n"
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
