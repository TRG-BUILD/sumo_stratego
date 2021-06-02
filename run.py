
from sumolib import checkBinary
import traci

from stratego.four_phase_interface import Controller
import sumo.feature_extraction as fe
from resultlogger import get_logger
import config_parser as cp

def decide_next_phase(durations, phase_seq, MIN_TIME=4):
    """
    If controller stays in the current phase longer than MIN_TIME
    it has decided to extend it, otherwise if it stays
    exactly MIN_TIME it is eager to switch it
    """
    next_phase = phase_seq[0]
    next_duration = durations[0]
    if next_duration == MIN_TIME and len(phase_seq) > 1:
        next_phase = phase_seq[1]
        next_duration = durations[1]
    return next_duration, next_phase

def run():
    logger = get_logger(
        directory=config.RESULT_PATH, 
        run_name=config.RUN_NAME)

    # Initialize stratego model
    ctrl = Controller(
        config.MODELFILE,
        model_cfg_dict=config.CTRL_STATE)

    traci.trafficlight.setPhase(
        config.TLS_ID,
        config.CTRL_TO_SIM_PHASE.get(0)) # start NW

    cost = 0
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        phase = traci.trafficlight.getPhase(config.TLS_ID)

        # read and preprocess state
        veh_counts = fe.get_vehicle_count(config.OBSERVED_LANES)
        state = fe.build_state(config, veh_counts, 0, phase)

        if step >= config.WARMUP and step % config.KAPPA == 0:
            # insert and calculate
            ctrl.init_simfile()
            ctrl.update_state(state)
            ctrl.insert_state()
            ctrl.debug_copy(config.DEBUG_NAME + f"_{step}.xml")

            durations, phase_seq  = ctrl.run(config.QUERY)

            phase_seq = [config.CTRL_TO_SIM_PHASE.get(p) for p in phase_seq]
            duration, next_phase = decide_next_phase(durations, phase_seq)
            print(
                step, " -> ", f"STATE -> {state} ",f"CONTROLS -> {next_phase} for {duration} s")

            traci.trafficlight.setPhase(config.TLS_ID, next_phase)

        # objective
        cost += fe.get_state_objective(state)
        logger.info('%d,%d', step, cost)
        step += 1
    
    traci.close()



if __name__ == "__main__":
    cfg = cp.get_valid_config()
    sumo_bin_name = 'sumo-gui' 
    if cfg.sumo.nogui:
        sumo_bin_name = 'sumo'

    sumo_bin = checkBinary(sumo_bin_name)
    traci.start([sumo_bin, "-c", cfg.sumo.model])

    #run(cfg)