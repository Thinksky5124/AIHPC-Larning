'''
Author       : Thinksky5124
Date         : 2024-04-07 23:51:14
LastEditors  : Thinksky5124
LastEditTime : 2024-04-07 23:56:54
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/kernel/cuda/vector_add/vector_add.py
'''
import torch
from aihpc.core import Dispatcher, BackendType, LaunchKernel

def add(x: torch.Tensor, y: torch.Tensor):
    
    return x + y

@Dispatcher.register(BackendType.CUDA, "add")
class LaunchCUDAAddKernel(LaunchKernel):
    def __call__(self, *args: torch.Any, **kwargs: torch.Any) -> torch.Any:
        return add(*args, **kwargs)