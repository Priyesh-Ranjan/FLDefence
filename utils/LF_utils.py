import torch

# Function to find matching positions for any number of numbers
def find_ASR(tensor_1, tensor_2, numbers):
    
    if numbers == None :
        return 0,100

    match_tensor1 = torch.zeros_like(tensor_1, dtype=torch.bool)
    match_tensor2 = torch.zeros_like(tensor_2, dtype=torch.bool)
    
    for num in numbers:
        match_tensor1 |= (tensor_1 == num)
        match_tensor2 |= (tensor_2 == num)
    
    matching_positions = (match_tensor1 & match_tensor2)
    
    count = torch.sum(matching_positions).item()
    
    return count, torch.sum(match_tensor1).item()
