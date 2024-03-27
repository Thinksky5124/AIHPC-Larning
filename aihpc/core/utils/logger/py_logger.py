'''
Author       : Thinksky5124
Date         : 2024-03-26 20:47:55
LastEditors  : Thinksky5124
LastEditTime : 2024-03-27 20:05:27
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/utils/logger/py_logger.py
'''
import os
import sys
import datetime
import logging
import functools
from .base_logger import BaseLogger, LoggerLevel
from aihpc.core.utils.registry_build import AbstractBuildFactory

def time_zone(sec, fmt):
    real_time = datetime.datetime.now()
    return real_time.timetuple()

@AbstractBuildFactory.register('logger')
class PythonLoggingLogger(BaseLogger):
    logger: logging.Logger
    level_map = {
        LoggerLevel.DEBUG: logging.DEBUG,
        LoggerLevel.INFO: logging.INFO,
        LoggerLevel.WARNING: logging.WARNING,
        LoggerLevel.ERROR: logging.ERROR,
        LoggerLevel.CRITICAL: logging.CRITICAL}

    def __init__(self, name: str = "AIHPC", root_path: str = None, level=LoggerLevel.INFO) -> None:
        super().__init__(name, root_path, level)
        logging.Formatter.converter = time_zone
        self.logger = logging.getLogger(name)
        self.set_level = level
        self.logger.propagate = False
        self.logger.level = self.level

        if level == "DEBUG":
            plain_formatter = logging.Formatter(
                "[%(asctime)s] %(name)s %(levelname)s: %(message)s",
                datefmt="%m/%d %H:%M:%S")
        else:
            plain_formatter = logging.Formatter(
                "[%(asctime)s] %(message)s",
                datefmt="%m/%d %H:%M:%S")

        # stdout logging: master only
        ch = logging.StreamHandler(stream=sys.stdout)
        ch.setLevel(self.level)
        formatter = plain_formatter
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # file logging: all workers
        if self.path is not None:
            if self.path.endswith(".txt") or self.path.endswith(".log"):
                filename = self.path
            else:
                # aviod cover
                filename = os.path.join(self.path, name + "_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") +".log")
                if(os.path.exists(filename)):
                    filename = os.path.join(self.path, name + "_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") +".log")

            # PathManager.mkdirs(os.path.dirname(filename))
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            # fh = logging.StreamHandler(_cached_log_stream(filename)
            fh = logging.FileHandler(filename, mode='a')
            fh.setLevel(self.level)
            fh.setFormatter(plain_formatter)
            self.logger.addHandler(fh)

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
        self.logger.setLevel(self.level_map[level])
    
    def log(self,
        msg: object,
        *args: object,
        level = None,
        exc_info = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra = None):
        assert level in LoggerLevel, f"Unsupport logging Level: {level}!"
        if level is None:
            level = self.level

        log_func = functools.partial(self.logger.log, level=level)
        log_func(msg, *args, extra=extra, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel)
    
    def info(self,
             msg: object,
             *args: object,
             exc_info = None,
             stack_info: bool = False,
             stacklevel: int = 1,
             extra = None):
        log_func = functools.partial(self.logger.log, level=logging.INFO)
        log_func(*args, msg=msg, extra=extra, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel)

    def debug(self,
             msg: object,
             *args: object,
             exc_info = None,
             stack_info: bool = False,
             stacklevel: int = 1,
             extra = None):
        log_func = functools.partial(self.logger.log, level=logging.DEBUG)
        log_func(*args, msg=msg, extra=extra, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel)
    
    def warn(self,
             msg: object,
             *args: object,
             exc_info = None,
             stack_info: bool = False,
             stacklevel: int = 1,
             extra = None):
        log_func = functools.partial(self.logger.log, level=logging.WARN)
        log_func(*args, msg=msg, extra=extra, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel)
    
    def error(self,
             msg: object,
             *args: object,
             exc_info = None,
             stack_info: bool = False,
             stacklevel: int = 1,
             extra = None):
        log_func = functools.partial(self.logger.log, level=logging.ERROR)
        log_func(*args, msg=msg, extra=extra, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel)
    
    def critical(self,
             msg: object,
             *args: object,
             exc_info = None,
             stack_info: bool = False,
             stacklevel: int = 1,
             extra = None):
        log_func = functools.partial(self.logger.log, level=logging.CRITICAL)
        log_func(*args, msg=msg, extra=extra, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel)