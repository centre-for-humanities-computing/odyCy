import torch
import spacy

def test_cuda_available():
    assert torch.cuda.is_available()

def test_spacy_sees_gpu():
    assert spacy.require_gpu()