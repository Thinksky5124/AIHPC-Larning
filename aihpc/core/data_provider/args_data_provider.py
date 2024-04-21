'''
Author       : Thinksky5124
Date         : 2024-03-28 20:31:00
LastEditors  : Thinksky5124
LastEditTime : 2024-04-21 22:39:46
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/data_provider/args_data_provider.py
'''
import torch
import copy

from typing import Dict, Any, Optional, Tuple, List, Callable
from aihpc.core.utils import ObjectRegister
from .base_data_provider import BaseDataProvider
from .tensor_generator import BaseTensorGenerator

@ObjectRegister.register('data_provider')
class TupleDataProvider(BaseDataProvider):
    def __init__(self,
                 args_list: List[Dict[str, Any]],
                 seed: int = None,
                 gbps: Callable = None,) -> None:
        super(TupleDataProvider, self).__init__(seed, gbps, "tuple")
        self.args_list = []
        for cfg in args_list:
            cfg_copy = copy.deepcopy(cfg)
            cfg_copy['seed_generator'] = self.seed_generator
            self.args_list.append(ObjectRegister.create_factory('tensor_generator').build(cfg_copy))

    def generate_data(self, *args, **kwargs) -> Tuple[Any]:
        data = [gen.generate(*args, **kwargs) for gen in self.args_list]
        return tuple(data)

@ObjectRegister.register('data_provider')
class DictDataProvider(BaseDataProvider):
    def __init__(self,
                 args_dict: Dict[str, Any],
                 seed: int = None,
                 gbps: Callable = None,) -> None:
        super(DictDataProvider, self).__init__(seed, gbps, "dict")
        self.args_dict = {}
        for key, cfg in args_dict.items():
            cfg_copy = copy.deepcopy(cfg)
            cfg_copy['seed_generator'] = self.seed_generator
            self.args_dict[key] = ObjectRegister.create_factory('tensor_generator').build(cfg_copy)
    
    def generate_data(self, *args, **kwargs) -> Dict[str, Any]:
        res_dict = {}
        for key, gen in self.args_dict.items():
            res_dict[key] = gen.generate(*args, **kwargs)
        return res_dict

@ObjectRegister.register('data_provider')
class MixedDataProvider(BaseDataProvider):
    def __init__(self,
                 args_list: List[Dict[str, Any]],
                 args_dict: Dict[str, Any],
                 seed: int = None,
                 gbps: Callable = None,) -> None:
        super(MixedDataProvider, self).__init__(seed, gbps, "mix")
        self.args_list = []
        for cfg in args_list:
            cfg_copy = copy.deepcopy(cfg)
            cfg_copy['seed_generator'] = self.seed_generator
            self.args_list.append(ObjectRegister.create_factory('tensor_generator').build(cfg_copy))
        self.args_dict = {}
        for key, cfg in args_dict.items():
            cfg_copy = copy.deepcopy(cfg)
            cfg_copy['seed_generator'] = self.seed_generator
            self.args_dict[key] = ObjectRegister.create_factory('tensor_generator').build(cfg_copy)

    def generate_data(self,  *args, **kwargs) -> Tuple[Tuple[Any], Dict[str, Any]]:
        data = [gen.generate(*args, **kwargs) for gen in self.args_list]
        res_dict = {}
        for key, gen in self.args_dict.items():
            res_dict[key] = gen.generate(*args, **kwargs)
        return tuple(data), res_dict