#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path
from statistics import mean
from collections import defaultdict

TIME_BIN = "/usr/bin/time"            
def elapsed_seconds(script: Path, chunks: int) -> dict[str, float]:
    cmd = [TIME_BIN, "-f", "%e", "python3", str(script), "--chunks", str(chunks)]
    result = subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )

    json_dict: dict | None = None
    for line in result.stderr.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            parsed = json.loads(line)
            if isinstance(parsed, dict):
                json_dict = parsed
                break          # found it!
        except json.JSONDecodeError:
            pass              # keep looking

    if json_dict is None:
        raise RuntimeError(
            "Could not find JSON timing data in stderr:\n" + result.stderr
        )

    return json_dict

def main() -> None:
    if not Path(TIME_BIN).exists():
        sys.exit(f"{TIME_BIN} not found install GNU/BSD time or edit TIME_BIN.")

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Benchmark SCRIPT for several --chunks values."
    )
    parser.add_argument("script", metavar="SCRIPT",
                        help="Path to the Python script to benchmark")
    parser.add_argument("--chunks-list", "-c", nargs="+", type=int, required=True,
                        metavar="N", help="Values to supply to --chunks")
    parser.add_argument("--runs", "-n", type=int, default=10,
                        help="Repetitions for each chunk value")

    args = parser.parse_args()
    script_path = Path(args.script)

    all_results = {}

    for chunks in args.chunks_list:
        print(f"\n=== --chunks {chunks}  (runs={args.runs}) ===")
        aggregated = defaultdict(list)

        for i in range(1, args.runs + 1):
            times = elapsed_seconds(script_path, chunks)
            print(f"  run {i:2d}: total={times['total']:.6f}s  "
                  f"chunk={times['chunking']:.6f}s  "
                  f"proc={times['processing']:.6f}s  "
                  f"comb={times['combining']:.6f}s")

            for k, v in times.items():
                aggregated[k].append(v)

        summary = {k: round(mean(vs), 6) for k, vs in aggregated.items()}
        summary["runs"] = args.runs
        all_results[chunks] = summary

    print("\n" + json.dumps(all_results, indent=2))

if __name__ == "__main__":
    main()
