import random
import time

start= time.time()
file = "file2.txt"

with open(file, "a") as file:
    for _ in range(1_000_000):
        num = random.randint(0, 32767)
        file.write(f"{num}\n")

end = time.time()
elapsed_time = end - start
print(f"program took {elapsed_time:.3f} seconds")
