'''
Author       : Thinksky5124
Date         : 2024-03-27 20:45:21
LastEditors  : Thinksky5124
LastEditTime : 2024-04-21 23:08:36
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/dispatcher.py
'''
import abc
import torch
from enum import Enum, auto
from threading import RLock
from typing import Callable, List, Tuple, Union, Dict, Any

class BackendType(Enum):
    OpenMP = "openmp"
    CUDA = "cuda"
    Triton = "triton"
    TorchCPU = "torch_cpu"
    TorchCUDA = "torch_cuda"

TORCH_MAP_DEVICE = {
    BackendType.TorchCPU: "cpu",
    BackendType.TorchCUDA: "cuda",
    BackendType.Triton: "cuda",
    BackendType.CUDA: "cuda",
    BackendType.OpenMP: "cpu"
}

def get_torch_map_device(backend: BackendType) -> torch.DeviceObjType:
    return torch.device(TORCH_MAP_DEVICE[backend])

def get_backend_type(backend_str):
    for backend in BackendType:
        if backend.value == backend_str:
            return backend
    raise ValueError(f"Invalid name: {backend_str}")

def get_backend_name(backend_type):
    for backend in BackendType:
        if backend == backend_type:
            return backend.value
    raise ValueError(f"Invalid type: {backend_type}")

class Dispatcher(object):
    DISPATCH_TABLE: Dict[str, Dict[BackendType, Callable]] = dict()
    single_lock = RLock()

    def __init__(self) -> None:
        pass

    # singleton design
    def __new__(cls):
        with Dispatcher.single_lock:
            if not hasattr(Dispatcher, "_instance"):
                Dispatcher._instance = object.__new__(cls)
        
        return Dispatcher._instance
    
    @staticmethod
    @property
    def ops_name():
        return list(Dispatcher.DISPATCH_TABLE.keys())
    
    @staticmethod
    def register(backend: BackendType, op_name: str = None):
        assert backend in BackendType, "Backend: {backend} not registered in BackendType!"
        op_name_c = op_name
        def do_register(obj: Callable, op_name_r: str = None):
            if op_name_r is None:
                if op_name_c is None:
                    op_name_r = obj.__name__
                else:
                    op_name_r = op_name_c
            if op_name_r not in Dispatcher.DISPATCH_TABLE:
                Dispatcher.DISPATCH_TABLE[op_name_r] = dict()
            Dispatcher.DISPATCH_TABLE[op_name_r][backend] = obj
            return obj
        
        return do_register
    
    @staticmethod
    def dispatch(op_name: str, backend: BackendType) -> Callable:
        return Dispatcher.DISPATCH_TABLE[op_name][backend]()


class LaunchKernel(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        pass