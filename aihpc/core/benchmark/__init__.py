'''
Author       : Thinksky5124
Date         : 2024-03-29 20:17:39
LastEditors  : Thinksky5124
LastEditTime : 2024-04-06 16:18:45
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/benchmark/__init__.py
'''
from .base_benchmark import BaseBenchmark
from .op_kernel_benchmark import OpKernelBenchmark

__all__ = [
    "BaseBenchmark", "OpKernelBenchmark"
]