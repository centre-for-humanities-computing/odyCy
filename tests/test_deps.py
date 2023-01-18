import torch

def test_cuda_available():
    assert torch.cuda.is_available()