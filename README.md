Welcome to SUMO-Stratego

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/mihsamusev/strategoutil)
<!---when tests are ready
[![badge](https://github.com/mihsamusev/strategoutil/workflows/build/badge.svg)](https://github.com/mihsamusev/strategoutil/actions)
--->

The purpose of the project is to provide infrastructure that lets use [UPPAAL Stratego](https://people.cs.aau.dk/~marius/stratego/) for traffic light optimization in [SUMO - Simulation of Urban Mobility](https://www.eclipse.org/sumo/).



<p align="center">
    <img src="docs/components.png">
</p>

## Associated projects
SUMO-Stratego shares ideas of MPC control using UPPAAL Stratego with the following projects:

- [`strategoutil`](https://github.com/mihsamusev/strategoutil) - Python library for Model Predictive Control using UPPAAL Stratego
- [`stratego_mpc_example`](https://github.com/mihsamusev/stratego_mpc_example) - example zoo for `strategoutil`


## Getting started
### Install
```
git clone https://github.com/TRG-BUILD/sumo_stratego.git
cd sumo_stratego
pip install -r requirements.txt

# install config parser as their pip is broken
pip install git+https://github.com/beetbox/confuse.git

python run.py -c tutorial.yaml
```

## Project structure
```
run.py
utils
- feature_extraction.py
configs
- job_1.yml
- job_2.yml
jobs
- job_1
    - stratego
        - __init__.py
        - model_template.xml
        - interface.py
        - query.q
    - sumo
        - __init__.py
        - demand
        - network
        - simulation.sumocfg
    - output
    - debug
- job_2
    ...
```


## TODO
- add info on what stratego interface is used 
- TDD feature extraction pipeline definitions
- running batches
- extend loggers to couple with matplotlib and writting states to DB


## FIX BUG!
```
20  ->  STATE -> {'A': [0, 0, 2], 'B': [0, 0, 0], 'x': 0.0, 'is_active': [1, 0, 1, 0]}  CONTROLS -> 0 for 5 s  OBJECTIVE -> 5
25  ->  STATE -> {'A': [2, 0, 2], 'B': [0, 1, 0], 'x': 0.0, 'is_active': [1, 0, 1, 0]}  CONTROLS -> 1 for 6 s  OBJECTIVE -> 14
30  ->  STATE -> {'A': [3, 0, 2], 'B': [0, 2, 0], 'x': 0.0, 'is_active': [1, 1, 1, 0]}  CONTROLS -> 1 for 1 s  OBJECTIVE -> 31
35  ->  STATE -> {'A': [3, 0, 2], 'B': [1, 4, 0], 'x': 0.0, 'is_active': [1, 1, 1, 0]}  CONTROLS -> 2 for 2 s  OBJECTIVE -> 61
40  ->  STATE -> {'A': [4, 0, 2], 'B': [2, 4, 0], 'x': 0.0, 'is_active': [1, 1, 1, 0]}  CONTROLS -> 0 for 5 s  OBJECTIVE -> 101
```