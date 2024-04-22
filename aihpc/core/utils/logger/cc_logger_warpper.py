'''
Author       : Thinksky5124
Date         : 2024-04-22 16:05:59
LastEditors  : Thinksky5124
LastEditTime : 2024-04-22 21:11:26
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/utils/logger/cc_logger_warpper.py
'''
import os
from aihpc import CXX_EXTENSION_ENABLED

from .base_logger import BaseLogger, LoggerLevel
from aihpc.core.utils.registry_build import ObjectRegister

if CXX_EXTENSION_ENABLED:
    from aihpc._C.core.spdlog import CCLogger, OutLevel

    @ObjectRegister.register('logger')
    class CCLoggerWrapper(BaseLogger):
        logger: CCLogger
        level_map = {
            LoggerLevel.TRACE: OutLevel.LEVEL_TRACE,
            LoggerLevel.DEBUG: OutLevel.LEVEL_DEBUG,
            LoggerLevel.INFO: OutLevel.LEVEL_INFO,
            LoggerLevel.WARNING: OutLevel.LEVEL_WARN,
            LoggerLevel.ERROR: OutLevel.LEVEL_ERROR,
            LoggerLevel.CRITICAL: OutLevel.LEVEL_CRITICAL}
        def __init__(self, name: str = "AIHPC", root_path: str = None, level=LoggerLevel.INFO) -> None:
            super().__init__(name, root_path, level)
            self.set_level = level
            self.logger = CCLogger(name, self.path, self.level_map[level])

        @property
        def level(self):
            """
            Return logger's current log level
            """
            return self.level_map[self._level]
    
        @level.setter
        def level(self, level: LoggerLevel):
            assert level in LoggerLevel, f"Unsupport logging Level: {self._level}!"
            self._level = level
            self.logger.set_logger_level(self.level_map[level])
        
        def log(self, level: LoggerLevel, msg: str):
            self.logger.log(self.level_map[level], msg)
        
        def trace(self, msg: str):
            self.logger.log_trace(msg)
        
        def info(self, msg: str):
            self.logger.log_info(msg)
        
        def debug(self, msg: str):
            self.logger.log_debug(msg)
        
        def warn(self, msg: str):
            self.logger.log_warn(msg)
        
        def error(self, msg: str):
            self.logger.log_error(msg)
        
        def critical(self, msg: str):
            self.logger.log_critical(msg)
else:
    class CCLoggerWrapper(BaseLogger):
        pass