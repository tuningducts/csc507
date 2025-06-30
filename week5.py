import subprocess
import time
import matplotlib.pyplot as plt

def parse_vmstat_line(line):
    parts = line.strip().split()
    if len(parts) < 17 or not parts[0].isdigit():
        return None
    return {
        'swpd': int(parts[2]),
        'free': int(parts[3]),
        'cache': int(parts[5]),
        'si': int(parts[6]),
        'so': int(parts[7]),
        'wa': int(parts[16]),
        'id': int(parts[15]),
    }

def collect_vmstat_data(duration_seconds=60):
    print(f"Collecting vmstat data for {duration_seconds} seconds...")
    process = subprocess.Popen(['vmstat', '1'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)

    # Skip headers
    process.stdout.readline()
    process.stdout.readline()

    data = {
        'time': [],
        'swpd': [],
        'free': [],
        'cache': [],
        'si': [],
        'so': [],
        'wa': [],
        'id': []
    }

    start = time.time()
    try:
        while time.time() - start < duration_seconds:
            line = process.stdout.readline()
            sample = parse_vmstat_line(line)
            if sample:
                t = int(time.time() - start)
                data['time'].append(t)
                for k in sample:
                    data[k].append(sample[k])
    except KeyboardInterrupt:
        pass
    finally:
        process.terminate()

    return data

def plot_vmstat_data(data):
    time_axis = data['time']

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.plot(time_axis, data['id'], label='CPU Idle (%)')
    plt.plot(time_axis, data['wa'], label='IO Wait (%)')
    plt.title("CPU Idle vs IO Wait")
    plt.xlabel("Time (s)")
    plt.ylabel("Percentage")
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.plot(time_axis, data['swpd'], label='Swap Used (KB)')
    plt.plot(time_axis, data['so'], label='Swap Out (KB/s)')
    plt.title("Swap Usage")
    plt.xlabel("Time (s)")
    plt.ylabel("KB")
    plt.legend()

    plt.subplot(2, 2, 3)
    plt.plot(time_axis, data['free'], label='Free Memory (KB)')
    plt.plot(time_axis, data['cache'], label='Cache Memory (KB)')
    plt.title("Memory Usage")
    plt.xlabel("Time (s)")
    plt.ylabel("KB")
    plt.legend()

    plt.subplot(2, 2, 4)
    plt.plot(time_axis, data['si'], label='Swap In (KB/s)')
    plt.plot(time_axis, data['so'], label='Swap Out (KB/s)')
    plt.title("Swap In/Out Rates")
    plt.xlabel("Time (s)")
    plt.ylabel("KB/s")
    plt.legend()

    plt.tight_layout()
    plt.savefig("vmstat_performance_idle.png")
    plt.show()
    print("Plot saved as vmstat_performance.png")

if __name__ == "__main__":
    data = collect_vmstat_data(duration_seconds=60)
    plot_vmstat_data(data)
