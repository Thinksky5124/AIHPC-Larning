'''
Author       : Thinksky5124
Date         : 2024-04-21 22:30:58
LastEditors  : Thinksky5124
LastEditTime : 2024-04-21 22:38:40
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/kernel/py_api/openmp.py
'''
import torch

from aihpc.core import Dispatcher, BackendType, LaunchKernel

from aihpc import CXX_EXTENSION_ENABLED

OPENMP_KERNEL_ENABLED = False
if CXX_EXTENSION_ENABLED:
    try:
        import aihpc._C.kernel.openmp as kernel_openmp
        OPENMP_KERNEL_ENABLED = True
    except:
        pass

if OPENMP_KERNEL_ENABLED:
    @Dispatcher.register(BackendType.OpenMP, "add")
    class LaunchOpenMPAddKernel(LaunchKernel):
        def __call__(self, *args: torch.Any, **kwargs: torch.Any) -> torch.Any:
            return kernel_openmp.add(*args, **kwargs)
    