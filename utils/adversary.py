import numpy as np
import random
from clients_attackers import *

ref = ["sqr","hash","cros","plus","eql","prl"]

def label_flipping_params(args) :
    sources = [int(i.strip()) for i in args.attack.split("->")[0].split(",")]
    targets = [int(i.strip()) for i in args.attack.split("->")[1].split(",")]
    
    flip = {}
    
    for i, val in enumerate(sources) :
        flip[val] = targets[i]
    
    return flip    
    
def backdoor_params(args) :
    target = args.attacks.split("->")[1].strip()  
    
    if args.backdoor == "central" :
        trigger = args.attack.split("->")[0].strip()
        pattern = [trigger]*args.num_clients
    if args.backdoor == "inter" :    
        triggers = [int(i.strip()) for i in args.attack.split("->")[0].split(",")]
        pattern = [triggers[int(i%len(triggers))] for i in range(args.num_clients)]
    if args.backdoor == "intra" :
        triggers = triggers = [int(i.strip()) for i in args.attack.split("->")[0].split(",")]
        pattern = [triggers for i in range(args.num_clients)]
    label = int(target)
    return pattern, label

def adversary_setup(args, model, trainData, optimizer, criterion, device):    

    if args.type == 'LF':
        flip = label_flipping_params(args)
    elif args.type == 'BD' :
        pattern, label = backdoor_params(args)
    else :
        print("Invalid attack")
        return None
    
    interval = range(args.start, (lambda x: args.epochs if x == None else x)(args.end))
    client_list = []; labels = []
    
    for i in range(args.num_clients):
        if i < args.scale :
            if args.type == 'LF':
                client = Attacker_LF(i, args.PDR, args.scaling, interval, flip, model, trainData[i], optimizer, criterion, device, args.inner_epochs)
                labels.append('LF')
            elif args.type == 'BD':
                client = Attacker_BD(i, args.PDR, args.scaling, interval, args.magnitude, pattern[i], args.pattern, label, model, trainData[i], optimizer, criterion, device, args.inner_epochs)
                labels.append('BD')
        else :    
            client = Client(i, model, trainData[i], optimizer, criterion, device, args.inner_epochs)
            labels.append('N')
        client_list.append(client)
    
    return client_list, labels    