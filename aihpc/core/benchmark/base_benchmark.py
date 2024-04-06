'''
Author       : Thinksky5124
Date         : 2024-03-29 20:18:07
LastEditors  : Thinksky5124
LastEditTime : 2024-04-06 21:30:49
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/benchmark/base_benchmark.py
'''
import abc
from typing import Dict, List, Any, Callable

from ..utils import ObjectRegister
from ..data_provider import BaseDataProvider, ArgsType

class BaseBenchmark(metaclass=abc.ABCMeta):
    data_provider: BaseDataProvider
    callback_fn_dict: Dict[str, List[Callable]]

    def __init__(self,
                 data_provider: Dict[str, Any],
                 x_names: str,
                 x_vals: List[Any],
                 warmup: int = 25,
                 repeat_num: int = 100,
                 return_mode: str = "mean") -> None:
        assert return_mode in ["min", "max", "mean", "median"]
        self.data_provider = ObjectRegister.create_factory('data_provider').build(data_provider)
        self.x_names = x_names
        self.x_vals = x_vals
        self.warmup = warmup
        self.repeat_num = repeat_num
        self.return_mode = return_mode
        self.callback_fn_dict = {}
    
    def register_callback(self, position: str, fn: Callable) -> None:
        if position not in self.callback_fn_dict:
            self.callback_fn_dict[position] = []
        self.callback_fn_dict[position].append(fn)

    def get_function_input(self, x_kwargs: Dict[str, Any]):
        if self.data_provider.args_type == ArgsType.DictType:
            return (), self.data_provider.generate_data(**x_kwargs)
        elif self.data_provider.args_type == ArgsType.TupleType:
            return self.data_provider.generate_data(**x_kwargs), {}
        elif self.data_provider.args_type == ArgsType.MixType:
            return self.data_provider.generate_data(**x_kwargs)
        else:
            raise NotImplementedError
    
    def function(self, fn, args, kwargs):
        return fn(*args, **kwargs)
        
    @abc.abstractmethod
    def run(self, fn_kwargs: Dict[str, Any]):
        pass
