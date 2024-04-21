'''
Author       : Thinksky5124
Date         : 2024-04-21 22:30:52
LastEditors  : Thinksky5124
LastEditTime : 2024-04-21 22:35:34
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/kernel/py_api/cuda.py
'''
import torch

from aihpc.core import Dispatcher, BackendType, LaunchKernel

from aihpc import CXX_EXTENSION_ENABLED

CUDA_KERNEL_ENABLED = False
if CXX_EXTENSION_ENABLED:
    try:
        import aihpc._C.kernel.cuda as kernel_cuda
        CUDA_KERNEL_ENABLED = True
    except:
        pass

if CUDA_KERNEL_ENABLED:    
    @Dispatcher.register(BackendType.CUDA, "add")
    class LaunchCUDAAddKernel(LaunchKernel):
        def __call__(self, *args: torch.Any, **kwargs: torch.Any) -> torch.Any:
            return kernel_cuda.add(*args, **kwargs)