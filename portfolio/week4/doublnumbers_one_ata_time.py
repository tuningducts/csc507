input_file = "file1.txt"
output_file = "newfile1.txt"

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        line = line.strip()
        if not line:
            continue
        try:
            num = int(line)
            doubled = num * 2
            outfile.write(f"{doubled}\n")
           

        except ValueError:
            print(f"Skipping non-integer line: {line}")
