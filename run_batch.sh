for i in {1..10}
do
   python run.py -c configs/low_demand.yml
done

for i in {1..10}
do
    python run.py -c configs/high_demand.yml
done
