import numpy as np
import random
from clients_attackers import *

["sqr","hash","cros","plus","eql","prl"]

def label_flipping_params(args) :
    sources = [int(i.strip()) for i in args.attacks.split("->")[0].split(",")]
    targets = [int(i.strip()) for i in args.attacks.split("->")[1].split(",")]
    
    

def adversary_setup(args, model, trainData, optimizer, criterion, device):    

    if args.type == 'LF':
        params = label_flipping_params(args)
    elif args.type == 'BD' :
        params = backdoor_params(args)
    else :
        print("Invalid attack")
        return None
    
    for i in range(args.num_clients):
        if i < args.scale :
            print()
        else :    
            client = Client(i, model, trainData[i], optimizer, criterion, device, args.inner_epochs)

    
    return client_list, labels    