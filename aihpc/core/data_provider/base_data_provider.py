'''
Author       : Thinksky5124
Date         : 2024-03-28 20:17:17
LastEditors  : Thinksky5124
LastEditTime : 2024-04-06 23:11:19
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/data_provider/base_data_provider.py
'''
import abc
import torch
from typing import Dict, Any, Optional, Tuple, Callable
from enum import Enum

class ArgsType(Enum):
    TupleType = "tuple"
    DictType = "dict"
    MixType = "mix"
    Unknown = "unknown"

def get_args_type(args_str):
    for backend in ArgsType:
        if backend.value == args_str:
            return backend
    raise ValueError(f"Invalid name: {args_str}")

def get_args_name(args_type):
    for backend in ArgsType:
        if backend == args_type:
            return backend.value
    raise ValueError(f"Invalid type: {args_type}")

class BaseDataProvider(metaclass=abc.ABCMeta):
    SEED_RANGE = [-9999999999, 99999999999]
    args_type: ArgsType
    gbps: Callable
    def __init__(self,
                 seed: int = None,
                 gbps: Callable = None,
                 args_type: str = "unknown") -> None:
        self.seed = seed
        if gbps is None:
            self.gbps = lambda ms: 12 / ms * 1e-6
        else:
            self.gbps = gbps
        if self.seed is not None:
            self.seed_generator = torch.Generator().manual_seed(self.seed)
        else:
            self.seed_generator = None
        self.args_type_name = args_type
        self.args_type = get_args_type(args_type)
        assert self.args_type in ArgsType and self.args_type != ArgsType.Unknown, "Must specify a args type!"

    def reset_seed_generator(self, seed: int = None):
        if seed is None:
            seed = self.seed
        self.seed_generator = torch.Generator().manual_seed(seed)

    def get_random_seed_from_generator(self) -> int:
        return int(torch.randint(low=self.SEED_RANGE[0], high=self.SEED_RANGE[1], size=[1], generator=self.seed_generator).item())
    
    @abc.abstractmethod
    def generate_data(self, *args, **kwargs) -> Any:
        pass
