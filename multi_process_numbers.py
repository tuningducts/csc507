import random
import time
from concurrent.futures import ProcessPoolExecutor

def make_numbers(n):
    return [f"{random.randint(0, 32767)}\n" for _ in range(n)]

if __name__ == "__main__":
    start = time.time()
    N = 10_000_000
    workers = 4
    chunk = N // workers

    with ProcessPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(make_numbers, [chunk]*workers))

    with open("file2.txt", "a") as f:
        for lines in results:
            f.writelines(lines)

    end = time.time()
    print(f"program took {end - start:.3f} seconds")
