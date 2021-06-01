from tqdm import tqdm
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

def extract_lanes_tripinfo(lanes, fcd_file,
    metrics=["duration", "waitingTime", "timeLoss"]):
    tree = ET.parse(fcd_file)

    output = {m: [] for m in metrics}

    for trip in tree.getroot():
        if trip.attrib["departLane"] in lanes:

            for metric, array in output.items():
                array.append(float(trip.attrib[metric]))
    
    return output

def report_output(outputDict):
    """
    write min, max, mean of some metrics
    """
    for k, v in outputDict.items():
        print("    {:<15}: min: {:<7.2f} max: {:<7.2f}, mean: {:<7.2f}".format(
            k, min(v), max(v), sum(v) / len(v)))

if __name__ == "__main__":
    import sys
    import matplotlib.pyplot as plt
    
    
    if len(sys.argv) > 1:
        fcd_files = sys.argv[1:]
    else:
        raise ValueError("No arguments supplied")
    

    LANES = {
        "EW": ["51o_0", "52o_0"],
        "NS": ["53o_0", "54o_0"]
    }
    metrics=["duration", "timeLoss"]

    # report written
    outputAll = {}
    for f in fcd_files:
        testName = f.split(".xml")[0].split("tripinfo_")[1]
        outputAll[testName] = {}
        print("\n[File]: ", f)
        for lane, sumoLane in LANES.items():
            outputAll[testName][lane] = {}
            output = extract_lanes_tripinfo(sumoLane, f, metrics)
            outputAll[testName][lane] = output  
            print("  [Lane]: ", lane)
            report_output(output)



    # report visual
    fig, ax = plt.subplots(nrows=len(metrics), ncols=len(fcd_files))

    for i, (test, lanes) in enumerate(outputAll.items()):
        for (lane, laneOutput) in lanes.items():
            for j, (metric, data) in enumerate(laneOutput.items()):
                ax[j,i].hist(data, bins=20, density=True, label=lane)
                ax[-1,i].set_xlabel("time [s]")
                ax[j,i].legend()

    for col, test in enumerate(outputAll.keys()):
        ax[0,col].set_title(test)

    for row, metr in enumerate(metrics):
        ax[row, 0].set_ylabel(metr, rotation=0, size='large',ha='right')


    plt.show()
    



