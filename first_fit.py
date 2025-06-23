import random

def first_fit(memory_blocks, process_sizes):
    allocation = [-1] * len(process_sizes)
    blocks = memory_blocks.copy()
    for pid, size in enumerate(process_sizes):
        for i, block in enumerate(blocks):
            if block >= size:
                allocation[pid] = i
                blocks[i] -= size
                break
    return allocation, blocks

def metric_success_rate(allocation):
    return sum(1 for a in allocation if a != -1) / len(allocation)

def metric_unused_memory(blocks):
    return sum(blocks)

def metric_external_fragmentation(blocks, min_proc_size):
    return sum(block for block in blocks if block < min_proc_size)


def scenario_large_processes(num_blocks=10, num_procs=10):
    blocks = [random.randint(256*1024, 2*1024*1024) for _ in range(num_blocks)]
    largest_block = max(blocks)
    processes = [random.randint(largest_block//2, largest_block) for _ in range(num_procs)]
    return blocks, processes

def scenario_high_variance(num_blocks=10, num_procs=10):
    blocks = [random.randint(32*1024, 2*1024*1024) for _ in range(num_blocks)]
    processes = [random.choice([
        random.randint(4*1024, 32*1024),           # tiny
        random.randint(256*1024, 2*1024*1024)      # large
    ]) for _ in range(num_procs)]
    return blocks, processes

def scenario_similar_processes(num_blocks=10, num_procs=10):
    blocks = [random.randint(128*1024, 1*1024*1024) for _ in range(num_blocks)]
    psize = random.randint(32*1024, 64*1024)
    processes = [psize for _ in range(num_procs)]
    return blocks, processes

def run_and_report(scenario_func, scenario_name):
    blocks, processes = scenario_func()
    allocation, remaining_blocks = first_fit(blocks, processes)
    min_proc_size = min([p for a, p in zip(allocation, processes) if a == -1], default=0)
    print(f"--- Scenario: {scenario_name} ---")
    print(f"Memory blocks: {blocks}")
    print(f"Process sizes: {processes}")
    print(f"Allocation: {allocation}")
    print(f"Success rate: {metric_success_rate(allocation):.2f}")
    print(f"Total unused memory: {metric_unused_memory(remaining_blocks)} bytes")
    print(f"External fragmentation: {metric_external_fragmentation(remaining_blocks, min_proc_size)} bytes")
    print()

if __name__ == "__main__":
    run_and_report(scenario_large_processes, "Large Process Sizes")
    run_and_report(scenario_high_variance, "High Variance Process Sizes")
    run_and_report(scenario_similar_processes, "Similar Process Sizes")
