'''
Author       : Thinksky5124
Date         : 2024-03-29 19:44:12
LastEditors  : Thinksky5124
LastEditTime : 2024-04-06 19:17:00
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/processor/base_processor.py
'''
import abc

class BaseProcessor(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def run(self, save_path=''):
        pass