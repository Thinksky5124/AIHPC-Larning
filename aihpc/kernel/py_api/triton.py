'''
Author       : Thinksky5124
Date         : 2024-04-21 22:31:04
LastEditors  : Thinksky5124
LastEditTime : 2024-04-21 22:33:50
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/kernel/py_api/triton.py
'''
import torch

from aihpc.core import Dispatcher, BackendType, LaunchKernel

from aihpc.kernel.triton import add as triton_add

@Dispatcher.register(BackendType.Triton, "add")
class LaunchTritonAddKernel(LaunchKernel):
    def __call__(self, *args: torch.Any, **kwargs: torch.Any) -> torch.Any:
        return triton_add(*args, **kwargs)