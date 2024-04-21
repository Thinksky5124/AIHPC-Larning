'''
Author       : Thinksky5124
Date         : 2024-04-08 15:01:32
LastEditors  : Thinksky5124
LastEditTime : 2024-04-21 20:23:53
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/kernel/py_api/add.py
'''
import torch

from aihpc.core import Dispatcher, BackendType, LaunchKernel

from aihpc.kernel.triton import add as triton_add
from aihpc.kernel.torch import add as torch_add

from aihpc import CXX_EXTENSION_ENABLED

CUDA_KERNEL_ENABLED = False
OPENMP_KERNEL_ENABLED = False
if CXX_EXTENSION_ENABLED:
    try:
        import aihpc._C.kernel.cuda as kernel_cuda
        CUDA_KERNEL_ENABLED = True
    except:
        pass

    try:
        import aihpc._C.kernel.openmp as kernel_openmp
        OPENMP_KERNEL_ENABLED = True
    except:
        pass

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
        return kernel_cuda.add(*args, **kwargs)

@Dispatcher.register(BackendType.OpenMP, "add")
class LaunchOpenMPAddKernel(LaunchKernel):
    def __call__(self, *args: torch.Any, **kwargs: torch.Any) -> torch.Any:
        return kernel_openmp.add(*args, **kwargs)