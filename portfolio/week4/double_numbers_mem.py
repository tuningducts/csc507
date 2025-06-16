input_file = "file1.txt"
output_file = "newfile1.txt"


with open(input_file, "r") as infile:
    numbers = [int(line.strip()) for line in infile if line.strip().isdigit()]


with open(output_file, "w") as outfile:
    for i, num in enumerate(numbers):
        doubled = num * 2
        outfile.write(f"{doubled}\n")
