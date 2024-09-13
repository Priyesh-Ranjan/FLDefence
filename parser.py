import argparse
import json

import numpy as np
#from utils.decide_attack import attack

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--test_batch_size", type=int, default=64)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--optimizer", type=str, default='SGD')
    parser.add_argument("--lr", type=float, default=0.01, help="Learning rate of models")
    parser.add_argument("--momentum", type=float, default=0.5)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--num_clients", type=int, default=10)
    parser.add_argument("--scale",type=int, default=10)
    parser.add_argument("--dataset", type=str, choices=["mnist", "cifar", "cifar100", "fmnist"], default="mnist")
    parser.add_argument("--loader_type", type=str, choices=["iid", "byLabel", "dirichlet"], default="iid")
    parser.add_argument("--AR", type=str, default="fedavg")
    parser.add_argument("--type", type=str, choices=["LF","BD"])
    parser.add_argument("--PDR",type=float,default=0.2)
    parser.add_argument("--scaling",type=float,default=1)
    parser.add_argument("--magnitude", nargs='?', type=float, default=1)
    parser.add_argument("--start", nargs='?', type=int, default=0)
    parser.add_argument("--end", nargs='?', type=int, default=None)
    parser.add_argument("--attack", type=str)
    parser.add_argument("--backdoor",nargs='?',type=str,choices=["central","intra","inter"], default="central")
    parser.add_argument("--label_flipping",nargs='?',type=str,choices=["uni","bi"], default="bi")
    parser.add_argument("--pattern",nargs='?',type=str,default=None)
    parser.add_argument("--experiment_name", type=str)
    parser.add_argument("--device", type=str, choices=["cuda", "cpu"], default='cuda')
    parser.add_argument("--inner_epochs", type=int, default=1)

    args = parser.parse_args()
    
    """if "DISTRIBUTED" in args.attacks.upper() :
        N = args.n_attacker
        args.attacker_list_distributed = np.array([i for i in range(N)])
    elif "BACKDOOR" in args.attacks.upper() :
        N = args.n_attacker
        args.attacker_list_backdoor = np.array([i for i in range(N)])
    elif "LABEL_FLIPPING" in args.attacks.upper() :
        N = args.n_attacker

    m_s = args.n_attacker_labelFlipping
    #args.attacker_list_labelFlipping = np.random.permutation(list(range(n)))[:m]
    args.attacker_list_labelFlipping = np.array([i for i in range(m_b,m_s+m_b)])

    m = args.n_attacker_labelFlippingDirectional
    args.attacker_list_labelFlippingDirectional = np.random.permutation(list(range(n)))[:m]
    
    m_m = args.n_attacker_multilabelFlipping
    args.attacker_list_multilabelFlipping = np.array([i for i in range(m_s+m_b,m_s+m_b+m_m)])

    if args.experiment_name == None:
        args.experiment_name = f"{args.loader_type}/{args.attacks}/{args.AR}"""
            
    return args


if __name__ == "__main__":

    import _main

    args = parse_args()
    print("#" * 64)
    for i in vars(args):
        print(f"#{i:>40}: {str(getattr(args, i)):<20}#")
    print("#" * 64)
    _main.main(args)
