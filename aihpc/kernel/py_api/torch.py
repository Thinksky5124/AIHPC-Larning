'''
Author       : Thinksky5124
Date         : 2024-04-21 22:31:10
LastEditors  : Thinksky5124
LastEditTime : 2024-04-21 22:33:25
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/kernel/py_api/torch.py
'''
import torch

from aihpc.core import Dispatcher, BackendType, LaunchKernel

from aihpc.kernel.torch import add as torch_add

@Dispatcher.register(BackendType.TorchCPU, "add")
class LaunchTorchCPUAddKernel(LaunchKernel):
    def __call__(self, *args: torch.Any, **kwargs: torch.Any) -> torch.Any:
        return torch_add(*args, **kwargs)

@Dispatcher.register(BackendType.TorchCUDA, "add")
class LaunchTorchCUDAAddKernel(LaunchKernel):
    def __call__(self, *args: torch.Any, **kwargs: torch.Any) -> torch.Any:
        return torch_add(*args, **kwargs)