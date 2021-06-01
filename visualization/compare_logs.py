import sys
import os
import csv
import matplotlib.pyplot as plt
import re
import pandas as pd
import argparse

def get_filenames(folder, ext=".log"):
    paths = []
    for f in os.listdir(folder):
        if f.endswith(ext):
            p = os.path.join(folder, f)
            paths.append(p)
    return paths

def extact_id(text):
    output = ""
    unique_id = re.findall(r"\s*(\d*).log", text)
    if len(unique_id) > 0:
        output = unique_id[0]
    return output

def group_runs(names):
    groups = {}
    for n in names:
        base = os.path.basename(n)
        unique_id = re.findall(r".*(_\d*).log", base)
        base = base.replace(".log", "")
        if len(unique_id) > 0:
            base = base.replace(unique_id[0], "")

        if base not in groups:
            groups[base] = []
        groups[base].append(n)

    return groups

def extract_data(filenames):
    """For now forget about steps, only extract 1st column
    """
    output = {}
    for f in filenames:
        unique_id = extact_id(f)
        with open(f, "r") as fin:
            reader = csv.reader(fin, delimiter=',')
            data = [int(row[1]) for row in reader]
            output.update({unique_id: data})
    return output

def truncate_datadict(datadict):
    min_size = min([len(d) for d in datadict.values()])
    for k, v in datadict.items():
        datadict[k] = datadict[k][:min_size]
    return datadict

def get_run_statistics(datadict):
    """
    Truncate to smallest
    """
    df = pd.DataFrame.from_dict(datadict)
    y = df.mean(axis=1)
    std = df.std(axis=1)
    y0 = y - std
    y1 = y + std
    return y, y0, y1

def setup_axes():
    # report visual 
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax.yaxis.set_major_locator(plt.MaxNLocator(10))
    ax.set_ylabel("objective []")
    ax.set_xlabel("timesteps []")
    return ax

def add_plot(ax, datadict, name):
    y, y0, y1 = get_run_statistics(datadict)
    p = ax.plot(y.index, y, '-', label=name)
    color = p[0].get_color()
    ax.fill_between(y.index, y0, y1, alpha=0.2, color=color)

if __name__ == "__main__":
    ag = argparse.ArgumentParser()
    ag.add_argument("-f", "--folder", type=str, required=True)
    args = ag.parse_args()

    ax = setup_axes()
    paths = get_filenames(folder=args.folder, ext=".log")
    runs = group_runs(paths)
    for run_name, run_files in runs.items():
        datadict = extract_data(run_files)
        datadict = truncate_datadict(datadict)
        add_plot(ax, datadict, name=run_name)

    ax.legend(loc='upper left')
    plt.show()
                
