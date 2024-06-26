'''
Author       : Thinksky5124
Date         : 2024-04-06 22:39:57
LastEditors  : Thinksky5124
LastEditTime : 2024-04-21 22:59:56
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/data_provider/tensor_generator.py
'''
import abc
import torch
from typing import List, Dict, Any, Tuple

from ..utils import ObjectRegister

class BaseTensorGenerator(metaclass=abc.ABCMeta):
    def __init__(self,
                 seed_generator: torch.Generator = None) -> None:
        self.seed_generator = seed_generator

    @abc.abstractmethod
    def generate(self, *args, **kwargs):
        pass
    
    def reset_generator(self, seed_generator: torch.Generator):
        self.seed_generator = seed_generator

@ObjectRegister.register('tensor_generator')
class RandomTensorGenerator(BaseTensorGenerator):
    def __init__(self,
                 seed_generator: torch.Generator,
                 dtype: torch.dtype,
                 device: Any = None) -> None:
        super().__init__(seed_generator)
        self.dtype = dtype
        self.device = device
    
    def generate(self, size: int, *args, map_device: Any = None, **kwargs) -> torch.Tensor:
        if map_device is None:
            map_device = self.device
        return torch.rand(size, generator=self.seed_generator,
                          dtype=self.dtype, device=map_device)
    
    