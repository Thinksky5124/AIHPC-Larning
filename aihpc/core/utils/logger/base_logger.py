'''
Author       : Thinksky5124
Date         : 2024-03-27 19:19:15
LastEditors  : Thinksky5124
LastEditTime : 2024-04-22 16:51:16
Description  : file content
FilePath     : /AIHPC-Larning/aihpc/core/utils/logger/base_logger.py
'''
import os
import abc
from enum import Enum, auto
from aihpc.core.utils.registry_build import ObjectRegister

class LoggerLevel(Enum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()
    TRACE = auto()

def get_log_root_path() -> str:
    return os.environ['AIHPC_LOG_DIR']

class BaseLogger(metaclass=abc.ABCMeta):
    LOGGER_DICT = dict()
    def __init__(self,
                 name: str,
                 root_path: str = None,
                 level = LoggerLevel.INFO) -> None:
        self._name = name
        if root_path is None:
            self._path = get_log_root_path()
        else:
            self._path = root_path
        self._level = level
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def level(self) -> LoggerLevel:
        return self._level
    
    @property
    def path(self) -> str:
        return self._path
    
    def __new__(cls, name: str, root_path: str = None, level=LoggerLevel.INFO):
        if name in BaseLogger.LOGGER_DICT.keys():
            raise NameError(f"You can't build two logger with the same name: {name}!")
        else:
            logger_instance = super().__new__(cls)
            BaseLogger.LOGGER_DICT[name] = logger_instance
            return logger_instance
    
    @abc.abstractmethod
    def log(self, msg, *args, **kwargs):
        pass
    
    @abc.abstractmethod
    def trace(self,
             msg: object,
             *args: object,
             **kwargs):
        pass

    @abc.abstractmethod
    def info(self,
             msg: object,
             *args: object,
             **kwargs):
        pass

    @abc.abstractmethod
    def debug(self,
             msg: object,
             *args: object,
             **kwargs):
        pass
    
    @abc.abstractmethod
    def warn(self,
             msg: object,
             *args: object,
             **kwargs):
        pass
    
    @abc.abstractmethod
    def error(self,
             msg: object,
             *args: object,
             **kwargs):
        pass
    
    @abc.abstractmethod
    def critical(self,
             msg: object,
             *args: object,
             **kwargs):
        pass

def get_logger(name: str) -> BaseLogger:
    assert name in BaseLogger.LOGGER_DICT.keys(), f"The log with the name of {name} was not initialized!"
    return BaseLogger.LOGGER_DICT[name]

def setup_logger(cfg):
    for logger_class, logger_cfg in cfg.items():
        logger_cfg['type'] = logger_class
        ObjectRegister.create_factory('logger').build(logger_cfg)

def get_root_logger_instance(default_name='AIHPC'):
    return BaseLogger.LOGGER_DICT[default_name]