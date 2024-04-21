"""
OpenMP Kernel module
"""
from __future__ import annotations
import torch
__all__ = ['add']
def add(arg0: torch.Tensor, arg1: torch.Tensor) -> torch.Tensor:
    """
    Add Two Tensor
    """
