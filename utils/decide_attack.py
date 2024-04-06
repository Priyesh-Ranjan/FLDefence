import numpy as np
import random

def attack(config, E):
    types = config["Type"]
    scale = config["scale"]
    duration = config["duration"]
    strength = config["strength"]
    strategy = config["strategy"]
    
    attacker_num = scale
    attack_rounds = duration
    
    if "LABEL" in types.upper() :
        attacks = 'L'
    elif "BACKDOOR" in types.upper() :
        attacks = 'B'
    
    if len(strength) == 2 :
        scaling = int(strength[0])
        nature = strength[1]
    else :
        scaling = 1
        nature = strength[0]
        
    if attacks == 'L' :
        sources = [i.strip() for i in nature.split("->")[0].split(",")]
        targets = [i.strip() for i in nature.split("->")[1].split(",")]
    elif attacks == 'B' :
        sources = [i.strip() for i in nature.split("->")[0].split(",")]
        targets = [i.strip() for i in nature.split("->")[1].split(",")]
    
    if strategy[0].upper() == "PROB" :
        prob = strategy[1]
        attack_rounds = np.array([0 if random.random() < float(prob) else 1 for i in range(E)])
    
    return attacker_num, attack_rounds, attacks, scaling, sources, targets
    
    """
    if "BACKDOOR" in name :
        n_backdoor  = name.split("BACKDOOR",1)[1].split(" ")[0]
        attacker_dictionary["backdoor"] = np.array([i for i in range(n_backdoor)])
        arr = name.split("BACKDOOR",1)[1].split(";")
        pattern = []; target = []
        for ele in arr :
            if "->" in ele :
                target.append(int(ele.split('->')[1]))
                pattern.append(ele.split('->')[0].split(','))
        attacker_dictionary["backdoor_pattern"] = pattern
        attacker_dictionary["backdoor_target"] = target        
    elif "LABEL" in name or "FLIPPING" in name :
        attacker_dictionary["label_flipping"] = np.array([i for i in range(N)])
        arr = name.split("FLIPPING",1)[1].split(";")
        source = []; destination = []
        for ele in arr :
            if "->" in ele :
                source.append(int(ele.split("->")[0]))
                destination.append(int(ele.split("->")[1]))
        attacker_dictionary["label_flipping_sources"] = source
        attacker_dictionary["label_flipping_destinations"] = destination        
    if "PROBABILISTIC" in name :
        prob = name.split("PROBABILISTIC",1)[1].split(";")[0]
        attacker_dictionary["attack_rounds"] = np.array([0 if random.random() < float(prob) else 1 for i in range(E)])
    if "DELAYED" in name :
        epoch = name.split("DELAYED",1)[1].split(";")[0]
        attacker_dictionary["attack_rounds"] = np.array([0 if i < int(epoch) else 1 for i in range(E)])
    if "ON-OFF" in name :
        attacker_dictionary["strategy"] = "ON-OFF"
    if "RAMP" in name :
        attacker_dictionary["strategy"] = "RAMP"
    print("The attack parameters are:\n")
    print(attacker_dictionary)    
    return attacker_dictionary"""