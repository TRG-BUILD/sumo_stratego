import traci
import copy


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

def add_phase(state, target, tls_id, phase_map):
    phase = traci.trafficlight.getPhase(tls_id)
    phase = phase_map.get(phase)
    if isinstance(state[target], list):
        state[target][phase] = 1
    else:
        state[target] = phase
    return state

def add_duration(state, target, tls_id):
    duration = traci.trafficlight.getPhaseDuration(tls_id)
    state[target] = float(duration)
    return state

def add_queue(state, target, lane):
    value = traci.lane.getLastStepVehicleNumber(lane)
    if isinstance(target, list):
        key, idx = target
        state[key][idx] += value
    else:
        state[target] += value
    return state

class ExtractionPipeline:
    def __init__(self, tls_ext, lane_ext):
        self.tls_ext = tls_ext
        self.lane_ext = lane_ext

    def apply_tls(self, state):
        if "phase_var" in self.tls_ext:            
            state = add_phase(state, 
                target=self.tls_ext["phase_var"],
                tls_id=self.tls_ext.id,
                phase_map=self.tls_ext.phase_map)

        if self.tls_ext.get("duration_var") is not None:
            state = add_duration(state,
                target=self.tls_ext["duration_var"],
                tls_id=self.tls_ext.id)

        return state
    
    def apply_lanes(self, state):
        for ext in self.lane_ext:
            for lane, target in ext["lanes"].items():
                if ext["feature"] == "queue":
                    state = add_queue(state, target, lane)
        return state

    def apply(self, state):
        state = copy.deepcopy(state)
        state = self.apply_tls(state)
        state = self.apply_lanes(state)
        return state





