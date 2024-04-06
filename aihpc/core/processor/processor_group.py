'''
Author       : Thinksky5124
Date         : 2024-03-29 19:48:23
LastEditors  : Thinksky5124
LastEditTime : 2024-04-06 19:49:02
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/processor/processor_group.py
'''
from typing import List, Dict

from .base_processor import BaseProcessor
from ..utils import ObjectRegister

@ObjectRegister.register('processor')
class ProcessorGroup(BaseProcessor):
    processors: List[BaseProcessor]

    def __init__(self,
                 processors: List[Dict[str, any]],
                 execute_seq: str = 'seq') -> None:
        super().__init__()
        assert execute_seq in ['seq', 'random'], f"Unsupported execute sequence: {execute_seq}!"
        
        self.execute_seq = execute_seq
        self.processors = [ObjectRegister.create_factory('processor').build(**processor)
                                for processor in processors]

    def run(self, save_path=''):
        if self.execute_seq =='seq':
            for processor in self.processors:
                processor.run(save_path=save_path)
        else:
            for processor in self.processors:
                processor.run(save_path=save_path)