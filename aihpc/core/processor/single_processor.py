'''
Author       : Thinksky5124
Date         : 2024-03-28 20:11:08
LastEditors  : Thinksky5124
LastEditTime : 2024-04-06 23:23:00
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/processor/single_processor.py
'''
import os
from typing import List, Dict

from ..utils import ObjectRegister
from ..dispatcher import BackendType
from ..benchmark import BaseBenchmark, OpKernelBenchmark
from ..reporter import BaseReporter
from .base_processor import BaseProcessor

@ObjectRegister.register('processor')
class SingleProcessor(BaseProcessor):
    backend: BackendType
    benchmarks: List[OpKernelBenchmark]
    reporters: List[BaseReporter]
    
    def __init__(self,
                 benchmarks: List[Dict[str, str]],
                 reporters: List[Dict[str, str]]):
        super().__init__()
        self.benchmarks = []
        for benchmark_cfg in benchmarks:
            self.benchmarks.append(ObjectRegister.create_factory('benchmark').build(benchmark_cfg))
        self.reporters = []
        for reporter_cfg in reporters:
            self.reporters.append(ObjectRegister.create_factory('reporter').build(reporter_cfg))

    def run(self, save_path = None):
        for reporter in self.reporters:
            for benchmark in self.benchmarks:
                benchmark.register_callback_after_backend(reporter)
        
        for benchmark in self.benchmarks:
            benchmark.run()
        
        for reporter in self.reporters:
            reporter.save(save_path=save_path)
        
        for reporter in self.reporters:
            reporter.clear()
