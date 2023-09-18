import os
import glob

import json
import matplotlib.pyplot as plt

# Load data from the JSON file
def load_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

# Extract statistical measures from the JSON data
def extract_data(data):
    stats = data["stats"]
    measures = ["median", "q1", "q3", "ld15iqr", "hd15iqr"]
    keys     = ['med', 'q1', 'q3', 'whislo', 'whishi']

    values = {}
    for k, m in zip(keys, measures):
        values[k] = stats[m]*1e9
    
    return values

# Plot a Tukey boxplot
def plot_tukey_box(data, save_path, title="Speed in Nanoseconds (ns)"):
    plt.figure(figsize=(8, 6))
    plt.subplot().bxp(data, showfliers=False)
    plt.xlabel("Categories")
    plt.ylabel("Duration")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a file
    plt.savefig(save_path)
    #plt.show()


def filter_data_by_name(data, name):
    data_name = []
    #data_name = list(filter(lambda d: d['name'] in [name], data))
    for d in data:
        if d['name'] == name:
            data_name.append(extract_data(d))
            data_name[-1]['label'] = d['name']

    return data_name

def filter_data_by_group(data, group):
    data_group = []

    for d in data:
        if d['group'] == group:
            data_group.append(extract_data(d))
            data_group[-1]['label'] = d['name']

    return data_group
    

def get_names(data):
    names = []
    for json_file in json_files:
        data = load_json(json_file)
        data = data['benchmarks']
        names += [benchmark['name'] for benchmark in data]
    names = list(set(names))
    return names
    
def get_groups(data):
    return [benchmark['group'] for benchmark in data]

    
def get_history_by_name(name, json_files):
    history_name = []
    
    for file_path in json_files:
        try:
            commit_hash = file_path.split('_')[1][:7]
            data = load_json(file_path)
            commit_time = data['commit_info']['time']
            data = data['benchmarks']
            data_name = filter_data_by_name(data, name)
            history_name.append(data_name[0])
            data_name[-1]['label'] = commit_hash
            data_name[-1]['time'] = commit_time
        except IndexError:
            pass

    return sorted(history_name, key=lambda d: d['time']) 

def plot_history_by_name(name, json_files):
    history_name = get_history_by_name(name, json_files)
    plot_name = f"{name}_history_boxplot.png"
    title = f"Speed in Nanoseconds (ns) - {name}"
    plot_tukey_box(history_name, plot_name, title = title)

def plot_benchmark_by_group(data, group, plot_name):
    data_group = filter_data_by_group(data, group)
    plot_tukey_box(data_group, plot_name)
    
def plot_history(json_files):
    names = get_names(json_files)
    for name in names:
        plot_history_by_name(name, json_files)

def plot_benchmark(json_file_path):
    commit_hash = json_file_path.split('_')[1][:7]

    # Load data from the JSON file
    data = load_json(json_file_path)
    data = data['benchmarks']

    groups = get_groups(data)
    
    for group in groups:
        plot_name = f"{commit_hash}_{group}_boxplot.png"
        plot_benchmark_by_group(data, group, plot_name)

if __name__ == "__main__":
    main_folder = os.path.dirname(os.getcwd())
    
    # Specify the folder path where you want to search for JSON files
    benchmark_folder = main_folder + "\.benchmarks\Windows-CPython-3.10-64bit"  # Replace with the actual folder path

    # Change the current working directory
    os.chdir(benchmark_folder)

    # Create a list to store the paths of JSON files
    json_files = []

    # Use glob to search for JSON files in the folder
    json_pattern = os.path.join(benchmark_folder, "*.json")
    json_files = glob.glob(json_pattern)

    # Print the list of JSON file paths
    #for file_path in json_files:
        #plot_benchmark(file_path)

    plot_history(json_files)
