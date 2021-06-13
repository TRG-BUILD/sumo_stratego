# Demand generation

Examples of generating demands of different modes and types, based on [randomTrips.py](https://sumo.dlr.de/docs/Tools/Trip.html).


Generates an `*.xml` file that defines vehicles:

```xml
<routes>
    <!-- road user type definition-->
    <vType id="sporty_car" vClass="passenger" maxSpeed="60" speedFactor="1.3" speedDev="0.1" sigma="0.1" />

    <!-- [COMPLETE DEMAND SPECIFCATION] demand consisting of a routes definitons [sequence of edges] and one or more vehicles of a given type following a route-->
    <route id="route0" color="1,1,0" edges="beg middle end rend"/>
    <vehicle id="0" type="sporty_car" route="route0" depart="0" color="1,0,0"/>
    <vehicle id="1" type="sporty_car" route="route0" depart="5" color="1,0,0"/>

    <!-- [COMPLETE DEMAND SPECIFICATION]
    Simulation performs fastest-path routing based on traffic condtion at departure time 
    FLOW - demand defined as steady state flow/generation of vehicles of a given type between origin and desintaion edges-->
    <flow id="sporty" type="sporty_car" begin="0" end="5000" number="500" from="WC" to="CE" departPos="base" departLane="best" />

    <!--
    TRIP - single trip between origin and destination-->
    <trip id="0" depart="0" from="WC" to="CE"/>
    <trip id="1" depart="5" from="WC" to="CE"/>
</routes>
```

_NOTE 1_: Vehicle type parameter `type` of `route`, `trip` or `flow` is not specified, [the simulation will apply `DEFAULT_VEHICLE` type.](https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html#default_vehicle_type).  Also `randomTrips.py -h` says  `--vehicle-class=VEHICLE_CLASS`
                        The vehicle class assigned to the generated trips
                        (adds a standard vType definition to the output file).

_NOTE 2_: The script does not check whether the chosen destination may be reached from the source. This task is performed by the router. If the network is not fully connected some of the trips may be discarded adding `--validate` flag. 

For all simulations we can remove intermediate edges from origins and destinations using `--weights-prefix` to not produce short trips. See example [here](https://sumo.dlr.de/docs/Tools/Trip.html#usage_example). Valid for bikes and vehicles, maybe not for pedestrians though.

## Vehicle demand generation

The most basic form, generates a trip every second, up to default 3600 seconds, with random origin and destination. `--seed` flag ensures repeatable randomization.

```sh
python $SUMO_HOME/tools/randomTrips.py \
    -n cross.net.xml \
    -o demands/vehicles.rou.xml \
    --seed 42 \
    --weights-prefix edge_weights
```

Generation of 100 veicles between the beginning time `-b` or `--begin` 100 s and end time `-e` or `--end` 1000. The period `-p` or `--period` controlls the arrival rate of `1 / period`. Arrival rate can be also drawn from binomial distribution `--binomial N` where N is maximum number of simultaneous arrivals.

```sh
python $SUMO_HOME/tools/randomTrips.py \
    -n cross4.net.xml \
    -o demands/vehicles.rou.xml \
    -b 100 \
    --end 1000 \
    --period 9 \
    --weights-prefix edge_weights \
    --seed 42
```


Limited to 1 type of specific vehicle

```sh
python $SUMO_HOME/tools/randomTrips.py \
    -n cross.net.xml \
    -o demands/vehicles.rou.xml \
    --vehicle-class bus \
    --seed 42
```

## Bicycle flow generation

Modelling bicycles as slow vehicles. Assumptions:

- no bi-directional movement on bike lanes
- no sharing lanes with pedestrians

Probably requires setting an `additional` file to define a bicycle `vType` as follows:

```xml
<!--in cyclist.type.xml-->
<additional>
  <vType id="cyclist" vClass="bicycle"/>
</additional>
```

And then running `randomTrips.py` with this definition:

```sh
python $SUMO_HOME/tools/randomTrips.py \
    -n networks/cross5_LFR_exits.net.xml \
    -o demands/cyclists.rou.xml \
    --trip-attributes='type="cyclist"' \
    --additional-file demands/cyclist.type.xml \
    --edge-permission bicycle \
    --period 5 \
    --binomial 25 \
    --prefix "c" \
    --seed 42 \
    --weights-prefix edge_weights \
    --validate
```

```sh
python $SUMO_HOME/tools/randomTrips.py \
    -n cross4.net.xml \
    --weights-prefix edge_weights \
    -o demands/cyclists.rou.xml \
    --vehicle-class bicycle \
    --edge-permission bicycle \
    --seed 42 \
    --validate
```

_NOTE_: `--validate` is used because i decided not to model bike left turns.

## Pedestrian flow generation

 Specifying option `--pedestrians` create a person file with pedestrian trips instead of vehicle trips. The difference with `--persontrips` is more broad specification that not only allows pedestrian traffic but also to specify modes of transport for intermodal routing (fx trips, walking -> bus -> walking -> car). Some options regarding pedestrian model are available [here](https://sumo.dlr.de/docs/Simulation/Pedestrians.html#pedestrian_models). By default pedestrians are using fastest/shortest path routing if routes are not specified.

```sh
python $SUMO_HOME/tools/randomTrips.py \
    -n cross4.net.xml \
    -o demands/pedestrians.rou.xml \
    --pedestrians \
    --max-distance 100 \
    --period 5
```

## Experiments with 4 way model
`four_phase_1` too fast?
```
python $SUMO_HOME/tools/randomTrips.py -n sumo/networks/cross5_LFR_exits.net.xml -o sumo/demands/vehicles.rou.xml --weights-prefix sumo/demands/edge_weights -b 0 -e 500 --binomial 5
```

`four_phase_2` more conservative period
```
python $SUMO_HOME/tools/randomTrips.py -n sumo/networks/cross5_LFR_exits.net.xml -o sumo/demands/vehicles.rou.xml --weights-prefix sumo/demands/edge_weights -b 0 -e 500 -p 3 --binomial 5
```



