import sys

def main() -> None:
    if len(sys.argv) != 4:
        sys.exit("Usage: python3 sum_chunk.py chunk1 chunk2 output")

    f1_path, f2_path, out_path = sys.argv[1:4]

    with open(f1_path) as a, open(f2_path) as b, open(out_path, "w") as out:
        for l1, l2 in zip(a, b):
            out.write(f"{int(l1) + int(l2)}\n")

if __name__ == "__main__":
    main()

