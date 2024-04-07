# dist_defence
Defence against distributed backdoor attacks in Federated Learning

```
!python main.py --num_clients 50 --optimizer Adam --dataset mnist --AR fedavg --attacks {"Type": "Backdoor", "scale": 6, "strat": ("prob",0.5), "strength": (2,"*,+ -> 8")} --loader_type dirichlet --experiment_name "Non-Persistant" --device cuda --epochs 10 --inner_epochs 10
```
