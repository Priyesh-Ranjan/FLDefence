import torch

# Function to find matching positions for any number of numbers
def find_ASR(tensor_1, tensor_2, flip):
    
    if flip == None :
        return 0,100

    count = 0
    tot = 0
    
    for src, tgt in flip.items():
        match_tensor1 = (tensor_1 == src)
        match_tensor2 = (tensor_2 == tgt)
        matching_positions = (match_tensor1 & match_tensor2)
        count += torch.sum(matching_positions).item()
        tot += torch.sum(match_tensor1).item()
    
    return count, tot
