'''
Author       : Thinksky5124
Date         : 2024-04-08 15:01:32
LastEditors  : Thinksky5124
LastEditTime : 2024-04-08 15:06:07
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/kernel/py_api/vector_add.py
'''
import torch

from aihpc.core import Dispatcher, BackendType, LaunchKernel

from aihpc.kernel.triton import add as triton_add
from aihpc.kernel.torch import add as torch_add

@Dispatcher.register(BackendType.Triton, "add")
class LaunchTritonAddKernel(LaunchKernel):
    def __call__(self, *args: torch.Any, **kwargs: torch.Any) -> torch.Any:
        return triton_add(*args, **kwargs)

@Dispatcher.register(BackendType.TorchCPU, "add")
class LaunchTorchCPUAddKernel(LaunchKernel):
    def __call__(self, *args: torch.Any, **kwargs: torch.Any) -> torch.Any:
        return torch_add(*args, **kwargs)

@Dispatcher.register(BackendType.TorchCUDA, "add")
class LaunchTorchCUDAAddKernel(LaunchKernel):
    def __call__(self, *args: torch.Any, **kwargs: torch.Any) -> torch.Any:
        return torch_add(*args, **kwargs)

@Dispatcher.register(BackendType.CUDA, "add")
class LaunchCUDAAddKernel(LaunchKernel):
    def __call__(self, *args: torch.Any, **kwargs: torch.Any) -> torch.Any:
        return add(*args, **kwargs)