
from sumolib import checkBinary
import traci

import feature_extraction as fe
from resultlogger import get_logger
import config_parser as cp

def run(cfg, ctrl=None, logger=None):
    feature_pipeline = fe.ExtractionPipeline(
        cfg.sumo.tls,
        cfg.sumo.extract,
        cfg.uppaal.variables)

    traci.trafficlight.setPhase(
        cfg.sumo.tls.id,
        0) # start NW

    n_main_phases = len(cfg.sumo.tls.phase_map)

    time = 0
    phase_time = 0
    while traci.simulation.getMinExpectedNumber() > 0 and time < cfg.mpc.max_steps:
        traci.simulationStep()

        # sim step info
        time = traci.simulation.getTime()
        
        phase = traci.trafficlight.getPhase(cfg.sumo.tls.id)
        is_main_phase = phase < n_main_phases
        if is_main_phase:
            phase_time += 1
            state = feature_pipeline.extract()
            print(
                time, " -> ",
                f"ELAPSED -> {phase_time} ", 
                f"STATE -> {state} ")


    traci.close()

def main():
    cfg = cp.get_valid_config()

    # Initialize SUMO simulator
    sumo_bin_name = 'sumo-gui' 
    if cfg.sumo.nogui:
        sumo_bin_name = 'sumo'
    sumo_bin = checkBinary(sumo_bin_name)
    traci.start([sumo_bin, "-c", cfg.sumo.model])

    run(cfg)

if __name__ == "__main__":
    main()