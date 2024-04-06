'''
Author       : Thinksky5124
Date         : 2024-04-06 16:22:41
LastEditors  : Thinksky5124
LastEditTime : 2024-04-06 18:34:42
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/reporter/base_reporter.py
'''
import abc
from typing import Dict, List, Any, Callable

class BaseReporter(object):
    def __init__(self,
                 save_path: str) -> None:
        self.save_path = save_path
    
    @abc.abstractmethod
    def __call__(self, x_name: str, x_val: Any, y_name: str,  *args, **kwargs) -> None:
        pass

    @abc.abstractmethod
    def save(self, save_path: str = None) -> None:
        pass

    @abc.abstractmethod
    def clear(self) -> None:
        pass