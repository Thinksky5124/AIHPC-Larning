'''
Author       : Thinksky5124
Date         : 2024-04-06 20:30:18
LastEditors  : Thinksky5124
LastEditTime : 2024-04-08 15:03:03
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/kernel/torch/vector_add.py
'''
import torch

from aihpc.core import Dispatcher, BackendType, LaunchKernel

def add(x: torch.Tensor, y: torch.Tensor):
    return x + y

