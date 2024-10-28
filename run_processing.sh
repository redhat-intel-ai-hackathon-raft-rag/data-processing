workers=20
for i in $(seq 1 $workers)
do
    python -m processing &
done
