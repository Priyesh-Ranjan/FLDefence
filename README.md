# FL_defence
Defence against targeted attacks in Federated Learning

```
!python main.py --num_clients 20 --scale 10 --dataset mnist --loader_type dirichlet --AR fedavg --type 'LF' --PDR 1 --scaling 1 --magnitude 1 --start 0 --attack "8->3" --label_flipping 'uni' --experiment_name "trial" --device cpu --inner_epochs 10 --batch_size 64 --test_batch_size 64 --epochs 10 --optimizer SGD --lr 0.01 --momentum 0.5 --seed 1
```
