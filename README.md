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
```
git clone https://github.com/TRG-BUILD/sumo_stratego.git
cd sumo_stratego
pip install -r requirements.txt

# install config parser as their pip is broken
pip install git+https://github.com/beetbox/confuse.git

python run.py -c tutorial.yaml
```

## TODO
- add info on what stratego interface is used 
- TDD feature extraction pipeline definitions
- running batches
- extend loggers to couple with matplotlib and writting states to DB