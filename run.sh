workers=80
for i in $(seq 1 $workers)
do
    python -m temp &
done
