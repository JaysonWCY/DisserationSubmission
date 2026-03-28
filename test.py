import torch
print(torch.version.cuda)      # Should show a CUDA version, e.g., '12.1'
print(torch.cuda.is_available())  # Should be True