import traci

def get_vehicle_count(lanes):
    """
    Calculates vehicle count on observed lanes
    """
    outDict = {}
    for lane in lanes:
        count = traci.lane.getLastStepVehicleNumber(lane)
        outDict[lane] = count
    return outDict

def build_state(features_map, phase_map, veh_counts, time, current_phase):

    state = {
        "A": [0, 0, 0],
        "B": [0, 0, 0],
        "x": float(time),
        "is_active": [0, 0, 0, 0]
    }

    for key, value in veh_counts.items():
        target = features_map.get(key)
        if value > 0:
            dir_name, pos = target 
            state[dir_name][pos] += value

    current_phase = phase_map.get(current_phase)
    state["is_active"][current_phase] = 1

    return state

def get_state_objective(state):
    C = state["A"] + state["B"]
    cost = 0
    for elem in C:
        cost += elem * elem
    return cost