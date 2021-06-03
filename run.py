
from sumolib import checkBinary
import traci

import importlib.util
import feature_extraction as fe
from resultlogger import get_logger
import config_parser as cp

def import_uppaal_interface(path):
    """
    Import UPPAAL strategoutil interface as module from file path
    """
    spec = importlib.util.spec_from_file_location(
        "stratego.interface", path)
    interface = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(interface)
    return interface

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

def run(cfg, ctrl):
    '''
    logger = get_logger(
        directory=config.RESULT_PATH, 
        run_name=config.RUN_NAME)
    '''

    feature_pipeline = fe.ExtractionPipeline(
        cfg.sumo.tls,
        cfg.sumo.extract)

    traci.trafficlight.setPhase(
        cfg.sumo.tls.id,
        0) # start NW

    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        phase = traci.trafficlight.getPhase(cfg.sumo.tls.id)

        # read and preprocess state
        state = feature_pipeline.apply(cfg.uppaal.variables)

        if step >= cfg.mpc.warmup and step % cfg.mpc.step == 0:
            # insert and calculate
            ctrl.init_simfile()
            ctrl.update_state(state)
            ctrl.insert_state()
            #ctrl.debug_copy(config.DEBUG_NAME + f"_{step}.xml")

            durations, phase_seq  = ctrl.run(
                queryfile=cfg.uppaal.query,
                verifyta_path=cfg.uppaal.verifyta)

            #phase_seq = [config.CTRL_TO_SIM_PHASE.get(p) for p in phase_seq]
            
            duration, next_phase = decide_next_phase(durations, phase_seq)
            print(
                step, " -> ",
                f"STATE -> {state} ",
                f"CONTROLS -> {next_phase} for {duration} s ",
                f"OBJECTIVE -> {ctrl.get_objective()}")

            traci.trafficlight.setPhase(cfg.sumo.tls.id, next_phase)

        # objective
        #ctrl.get_objective()
        #logger.info('%d,%d', step, cost)
        step += 1
    
    traci.close()

def main():
    cfg = cp.get_valid_config()
    sumo_bin_name = 'sumo-gui' 
    if cfg.sumo.nogui:
        sumo_bin_name = 'sumo'

    # Initialize UPPAAL model
    sumo_bin = checkBinary(sumo_bin_name)
    traci.start([sumo_bin, "-c", cfg.sumo.model])

    # Initialize stratego model
    interface = import_uppaal_interface(cfg.uppaal.interface)
    ctrl = interface.Controller(
        templatefile=cfg.uppaal.model,
        model_cfg_dict=cfg.uppaal.variables)

    run(cfg, ctrl)

if __name__ == "__main__":
    main()