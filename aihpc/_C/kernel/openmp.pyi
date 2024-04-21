"""
OpenMP Kernel module
"""
from __future__ import annotations
import torch
__all__ = ['add']
def add(a: torch.Tensor, b: torch.Tensor, in_place: bool = False) -> torch.Tensor:
    """
    Add Two Tensor
    """
