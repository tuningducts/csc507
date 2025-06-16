input_file  = "file1.txt"
output_file = "newfile1.txt"

with open(input_file, "r") as infile:
    lines = [line.strip() for line in infile if line.strip()]  

mid = len(lines) // 2
part1, part2 = lines[:mid], lines[mid:]

def double_list(str_list):
    result = []
    for s in str_list:
        try:
            result.append(str(int(s) * 2))   
        except ValueError:
            print(f"Skipping non‑integer line: {s}")
    return result

doubled1 = double_list(part1)
doubled2 = double_list(part2)

combined = doubled1 + doubled2

with open(output_file, "w") as outfile:
    outfile.write("\n".join(combined) + "\n")       
