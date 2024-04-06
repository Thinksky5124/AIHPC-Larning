'''
Author       : Thinksky5124
Date         : 2024-04-06 20:30:18
LastEditors  : Thinksky5124
LastEditTime : 2024-04-06 21:01:48
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/kernel/torch/vector_add.py
'''
import torch

from aihpc.core import Dispatcher, BackendType, LaunchKernel

def add(x: torch.Tensor, y: torch.Tensor):
    return x + y

@Dispatcher.register(BackendType.TorchCPU, "add")
class LaunchTorchCPUAddKernel(LaunchKernel):
    def __call__(self, *args: torch.Any, **kwargs: torch.Any) -> torch.Any:
        return add(*args, **kwargs)

@Dispatcher.register(BackendType.TorchGPU, "add")
class LaunchTorchGPUAddKernel(LaunchKernel):
    def __call__(self, *args: torch.Any, **kwargs: torch.Any) -> torch.Any:
        return add(*args, **kwargs)