import os
import multiprocessing as mp
import argparse
import time
import sys
import json

input_file = "large_file.txt"
output_file = "large_new_file.txt"


def chunk_file(file, chunks: int):
    # Count total lines in the file
    with open(file, 'r') as f:
        total_lines = sum(1 for _ in f)

    lines_per_chunk = total_lines // chunks
    remainder = total_lines % chunks

    chunked_files = []
    with open(file, 'r') as f:
        for i in range(chunks):
            chunk_lines = lines_per_chunk + (1 if i < remainder else 0)
            chunk_filename = f"{os.path.splitext(file)[0]}_chunk_{i}.txt"
            with open(chunk_filename, 'w') as chunk_file:
                for _ in range(chunk_lines):
                    line = f.readline()
                    if not line:
                        break
                    chunk_file.write(line)
            chunked_files.append(chunk_filename)

    return chunked_files


def cleanup_files(files):
    deleted = []
    for file in files:
        try:
            os.remove(file)
            deleted.append(file)
        except FileNotFoundError:
            print(f"File not found: {file}")
        except PermissionError:
            print(f"Permission denied: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")
    return deleted

def process_single_file(input_file):
    output_file = f"out_{input_file}"
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            try:
                doubled = int(line) * 2
                outfile.write(f"{doubled}\n")
            except ValueError:
                print(f"Skipping non-integer line in {input_file}: {line}")
    return output_file


def process_chunk_files_parallel(input_files):
    with mp.Pool(processes=mp.cpu_count()) as pool:
        output_files = pool.map(process_single_file, input_files)
    return output_files

def combine_output_files(output_files, final_output_file):
    with open(final_output_file, "w") as fout:
        for file in output_files:
            with open(file, "r") as fin:
                fout.writelines(fin)


def get_chunks_arg_or_prompt(arg_val, prompt="Enter number of chunks"):
    if arg_val is not None:
        try:
            return int(arg_val)
        except ValueError:
            print(f"Invalid argument value: {arg_val} (must be an integer)")

    # Interactive fallback
    while True:
        try:
            value = int(input(f"{prompt}: "))
            return value
        except ValueError:
            print("That's not a valid integer. Try again.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunks", help="Number of chunks (integer)")
    args = parser.parse_args()
    chunk_count = get_chunks_arg_or_prompt(args.chunks)

    times = {}
    start_total = time.perf_counter()

    # Step 1: Chunking
    start = time.perf_counter()
    chunks = chunk_file(input_file, chunk_count)
    times["chunking"] = round(time.perf_counter() - start, 6)

    # Step 2: Processing
    start = time.perf_counter()
    processed_chunks = process_chunk_files_parallel(chunks)
    times["processing"] = round(time.perf_counter() - start, 6)

    # Step 3: Combining
    start = time.perf_counter()
    combine_output_files(processed_chunks, output_file)
    times["combining"] = round(time.perf_counter() - start, 6)

    # Cleanup
    cleanup_files(chunks)
    cleanup_files(processed_chunks)

    times["total"] = round(time.perf_counter() - start_total, 6)

    print(json.dumps(times), file=sys.stderr)
