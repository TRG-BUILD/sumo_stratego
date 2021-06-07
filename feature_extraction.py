import traci
import copy

def add_phase(state, target, tls_id, phase_map):
    """
    Extracts and inserts TLS phase with traci 
    to the state passed to Stratego
    """
    phase = traci.trafficlight.getPhase(tls_id)
    phase = phase_map.get(phase)
    if isinstance(state[target], list):
        state[target][phase] = 1
    else:
        state[target] = phase
    return state

def add_duration(state, target, tls_id):
    """
    Extracts and inserts TLS phase duration with traci 
    to the state passed to Stratego
    """
    duration = traci.trafficlight.getPhaseDuration(tls_id)
    state[target] = float(duration)
    return state

def add_queue(state, target, lane):
    """
    Extracts and inserts accumulated number of vehicles
    to the state passed Stratego
    """
    value = traci.lane.getLastStepVehicleNumber(lane)
    if isinstance(target, list):
        key, idx = target
        state[key][idx] += value
    else:
        state[target] += value
    return state

class ExtractionPipeline:
    """
    Populates state with data about tls and lanes depending on
    the config requirements
    """
    def __init__(self, tls_ext, lane_ext, state_template):
        self.tls_ext = tls_ext
        self.lane_ext = lane_ext
        self.state_template = copy.deepcopy(state_template)
        self.state = {}

    def reset_state(self):
        self.state = copy.deepcopy(self.state_template)

    def extract_tls(self):
        if "phase_var" in self.tls_ext:            
            self.state = add_phase(self.state, 
                target=self.tls_ext["phase_var"],
                tls_id=self.tls_ext.id,
                phase_map=self.tls_ext.phase_map)

        if self.tls_ext.get("duration_var") is not None:
            self.state = add_duration(self.state,
                target=self.tls_ext["duration_var"],
                tls_id=self.tls_ext.id)
    
    def extract_lanes(self):
        for ext in self.lane_ext:
            for lane, target in ext["lanes"].items():
                if ext["feature"] == "queue":
                    self.state = add_queue(self.state, target, lane)

    def extract(self):
        self.reset_state()
        self.extract_tls()
        self.extract_lanes()
        return self.state





