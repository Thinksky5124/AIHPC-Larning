'''
Author       : Thinksky5124
Date         : 2024-03-27 20:29:15
LastEditors  : Thinksky5124
LastEditTime : 2024-03-27 21:20:48
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/api.py
'''
from .dispatcher import BackendType, Dispatcher
from typing import Callable

def run_kernel(func_name: str, backend:BackendType, *args, **kwargs):
    return Dispatcher.dispatch(func_name, backend)(*args, **kwargs)