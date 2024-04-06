'''
Author       : Thinksky5124
Date         : 2024-03-28 20:16:39
LastEditors  : Thinksky5124
LastEditTime : 2024-04-01 22:45:00
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/data_provider/__init__.py
'''
from .base_data_provider import BaseDataProvider, ArgsType
from .args_data_provider import (TupleDataProvider, DictDataProvider,
                                 MixedDataProvider)
from .tensor_generator import RandomTensorGenerator, BaseTensorGenerator

__all__ = ['TupleDataProvider', 'DictDataProvider', 'MixedDataProvider',
           'BaseDataProvider', 'ArgsType', 'RandomTensorGenerator',
           'BaseTensorGenerator']