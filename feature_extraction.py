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
    to the state passed to Stratego
    """
    number = traci.lane.getLastStepVehicleNumber(lane)
    if isinstance(target, list):
        key, idx = target
        state[key][idx] += number
    else:
        state[target] += number
    return state

def add_to_state(state, target, value):
    """
    Adds a value to state dictionary
    """
    if isinstance(target, list):
        key, idx = target
        state[key][idx] += value
    else:
        state[target] += value
    return state

def add_typed_lane_count(state, lane, target, user_type="DEFAULT_VEHTYPE"):
    """
    Extracts accumulated number of users from a lane and inserts
    to the state passed to Stratego
    """
    ids = traci.lane.getLastStepVehicleIDs(lane)
    number = sum([1 for i in ids if traci.vehicle.getTypeID(i) == user_type])
    state = add_to_state(state, target, number)
    return state

def add_typed_phase_count(state, tls_id, phase_id, target, user_type="DEFAULT_VEHTYPE"):
    """
    Extracts accumulated number of users served by tls phase and inserts
    to the state passed to Stratego
    """

    # if pedestrian requested just use tls function to get served count at phase_id,
    # otherwise, extract lanes enabled for the phase_id and reuse lane count fcn
    ctrl_links = traci.trafficlight.getControlledLinks(tls_id)
    phase_lights = traci.trafficlight.getAllProgramLogics(
        tls_id)[1].getPhases()[phase_id].state

    phase_links = set(
        [lane[0] for lane, col in zip(ctrl_links, phase_lights) if col.lower() == 'g'])

    # RREALLY REALLY HACKY!
    ped_edges = [link[0][0].rsplit("_", 1)[0] for link in ctrl_links if link[0][0][0] == ":"]
    phase_cross_edges = [link[1].rsplit("_", 1)[0] for link in phase_links if link[0][0]==":"]

    if user_type == "pedestrian":
        
        number = 0
        for edge in ped_edges:
            peds = traci.edge.getLastStepPersonIDs(edge)
            # what?
            for ped in peds:
                if (traci.person.getWaitingTime(ped) >= 1 and 
                    traci.person.getNextEdge(ped) in phase_cross_edges):
                    number += 1
        state = add_to_state(state, target, number)
    else:
        lanes = set([lanes[0] for lanes in phase_links])
        for lane in lanes:
            state = add_typed_lane_count(state, lane, target, user_type)

    return state


class ExtractionPipeline:
    """
    Populates state with data about tls and lanes depending on
    the config requirements
    """
    def __init__(self, tls_ext, user_ext, state_template, tls_program_id=1):
        self.tls_program_id = tls_program_id
        self.tls_ext = tls_ext
        self.user_ext = user_ext
        self.state_template = copy.deepcopy(state_template)
        self.state = {}
        self.validate_targets()

    def validate_targets(self):
        """
        Check whether UPPAAL variables area available for writting 
        extracted simulation data
        """
        lane_ids = traci.lane.getIDList()
        phase_count = len(traci.trafficlight.getAllProgramLogics(
            self.tls_ext.id)[self.tls_program_id].getPhases())

        for ext in self.user_ext:
            origin = ext["from"]
            for sumo_var, stratego_var in ext["mapping"].items():
                # validate origin
                if origin == "lane":
                    assert sumo_var in lane_ids, \
                        f"{sumo_var} is not a SUMO link"
                elif origin == "phase":
                    assert str(sumo_var).isdigit(), \
                        f"{sumo_var} is not correct to be TLS phase"
                    assert int(sumo_var) < phase_count, \
                        f"{sumo_var} is not a TLS phases"

                # validate stratego_var
                if isinstance(stratego_var, list):
                    assert stratego_var[0] in self.state_template.keys(), \
                    f"{stratego_var[0]} is not in UPPAAL variables"
                    assert stratego_var[1] <= len(self.state_template[stratego_var[0]]), \
                        f"{stratego_var[0]} at {stratego_var[1]} is out of bounds of UPPAAL variable"
                else:
                    assert stratego_var in self.state_template.keys(), \
                    f"{stratego_var} is not in UPPAAL variables"

                
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
    
    def extract_counts(self, origin, mapping, user_type="DEFAULT_VEHTYPE"):
        """
        Extracts and adds queue length of given vtype
        """
        if origin == "lane": 
            for lane, stratego_var in mapping.items():
                add_typed_lane_count(self.state, lane, stratego_var, user_type)
        elif origin == "detector":
            #for detector, stratego_var in mapping.items():
            NotImplementedError
        elif origin == "phase":
            for phase, stratego_var in mapping.items():
                add_typed_phase_count(
                    self.state, self.tls_ext.id, phase, stratego_var, user_type)

    def extract(self):
        self.reset_state()
        self.extract_tls()

        for ext in self.user_ext:
            if ext["feature"] == "count":
                self.extract_counts(
                    origin=ext["from"],
                    mapping=ext["mapping"],
                    user_type=ext["user_type"])

        return self.state







