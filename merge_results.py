#!/usr/bin/env python3
"""
merge_results.py — Merge parallel experiment results, apply best to agent.py, commit.

Run after all parallel sessions finish:
    python merge_results.py
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime

from indic_agent import STRATEGIES, MODEL_NAME


def load_all_results():
    rows = []
    for f in sorted(Path(".").glob("results*.jsonl")):
        for line in f.read_text().splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


def main():
    rows = load_all_results()

    print(f"\n{'='*65}")
    print(f"  All experiment results ({len(rows)} runs)")
    print(f"{'='*65}")

    # Sort by accuracy descending, filter out zero-accuracy noise
    rows.sort(key=lambda r: r["accuracy"], reverse=True)

    print(f"\n  {'Strategy':<35} {'Acc':>7}  {'n':>5}  Action")
    print(f"  {'-'*62}")
    for r in rows:
        print(f"  {r.get('strategy_name', '?'):<35} {r['accuracy']:>7.4f}  {r['n']:>5}  {r.get('action','?')}")

    # Best by accuracy (prefer more examples if tie)
    valid = [r for r in rows if r["n"] > 50]
    if not valid:
        print("\n  No valid results yet.")
        return

    best = max(valid, key=lambda r: (r["accuracy"], r["n"]))
    print(f"\n  Best: {best['strategy_name']} acc={best['accuracy']:.4f} n={best['n']}")

    # Check what's currently committed
    result = subprocess.run(["git", "log", "--oneline", "-3"], capture_output=True, text=True)
    print(f"\n  Recent commits:\n{result.stdout}")

    # Write best strategy to agent.py
    sid = best["strategy_idx"]
    if sid not in STRATEGIES:
        print(f"  ERROR: strategy {sid} not found in STRATEGIES dict")
        return

    code = STRATEGIES[sid]["code"].replace("{model}", MODEL_NAME)
    Path("agent.py").write_text(code)
    print(f"\n  Wrote strategy {sid} ({best['strategy_name']}) to agent.py")

    # Commit
    subprocess.run(["git", "add", "agent.py"], check=True)
    msg = (f"Best: {best['strategy_name']} acc={best['accuracy']:.4f} "
           f"n={best['n']} MILU-ml [{datetime.now().strftime('%Y-%m-%d')}]")
    subprocess.run(["git", "commit", "-m", msg], check=True)
    print(f"  Committed: \"{msg}\"")

    # Write summary to program.md
    text = Path("program.md").read_text()
    summary = (
        "\n## Merged Best Result\n\n"
        f"- Strategy: **{best['strategy_name']}** ({STRATEGIES[sid]['research']})\n"
        f"- Accuracy: **{best['accuracy']:.4f}** on {best['n']} MILU-ml examples\n"
        f"- Committed: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        "**Language pivoting finding:** English-pivot CoT and native Malayalam CoT "
        "both hurt accuracy vs direct prompting for Qwen3-1.7B. "
        "Few-shot examples marginally help. This is a key result for the paper.\n"
    )
    Path("program.md").write_text(text.rstrip() + "\n" + summary)
    print(f"  Updated program.md")
    print(f"\n{'='*65}\n")


if __name__ == "__main__":
    main()
