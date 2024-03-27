'''
Author       : Thinksky5124
Date         : 2024-03-27 20:45:21
LastEditors  : Thinksky5124
LastEditTime : 2024-03-27 21:20:06
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/dispatcher.py
'''
from enum import Enum, auto
from threading import RLock
from typing import Callable, List, Tuple, Union, Dict, Any

class BackendType(Enum):
    OpenMP = auto()
    CUDA = auto()
    Tritron = auto()

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

        def do_register(obj: Callable):
            if op_name is None:
                op_name = obj.__name__
            if op_name not in Dispatcher.DISPATCH_TABLE:
                Dispatcher.DISPATCH_TABLE[op_name] = dict()
            Dispatcher.DISPATCH_TABLE[op_name][backend] = obj
            return obj
        
        return do_register
    
    @staticmethod
    def dispatch(op_name: str, backend: BackendType) -> Callable:
        return Dispatcher.DISPATCH_TABLE[op_name][backend]
