for i in {1..10}
do
    python run.py -c configs/latest_wy.yml
done

for i in {1..10}
do
    python run.py -c configs/latest_wy_low.yml
done

for i in {1..10}
do
    python run.py -c configs/latest_wy_high.yml
done

for i in {1..10}
do
    python run.py -c configs/latest.yml
done
