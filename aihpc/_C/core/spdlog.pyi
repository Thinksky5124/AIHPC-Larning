"""
A Python wrapper spdlog module
"""
from __future__ import annotations
import typing
__all__ = ['ASYNC', 'CCLogger', 'CONSOLE', 'CONSOLE_AND_FILE', 'FILE', 'LEVEL_CRITICAL', 'LEVEL_DEBUG', 'LEVEL_ERROR', 'LEVEL_INFO', 'LEVEL_OFF', 'LEVEL_TRACE', 'LEVEL_WARN', 'OutLevel', 'OutMode', 'OutPosition', 'SYNC']
class CCLogger:
    def __init__(self, name: str, root_path: str, eOutLevel: OutLevel = OutLevel.LEVEL_TRACE, eOutPosition: OutPosition = OutPosition.CONSOLE_AND_FILE, eOutMode: OutMode = OutMode.SYNC) -> None:
        ...
    def init_logger(self, name: str, root_path: str, eOutLevel: OutLevel = OutLevel.LEVEL_TRACE, eOutPosition: OutPosition = OutPosition.CONSOLE_AND_FILE, eOutMode: OutMode = OutMode.SYNC) -> bool:
        ...
    def log_critical(self, msg: str) -> None:
        ...
    def log_debug(self, msg: str) -> None:
        ...
    def log_error(self, msg: str) -> None:
        ...
    def log_info(self, msg: str) -> None:
        ...
    def log_trace(self, msg: str) -> None:
        ...
    def log_warn(self, msg: str) -> None:
        ...
    def set_logger_level(self, eOutLevel: OutLevel) -> None:
        ...
    def uninit_logger(self) -> None:
        ...
    @property
    def name(self) -> str:
        ...
class OutLevel:
    """
    Members:
    
      LEVEL_TRACE
    
      LEVEL_DEBUG
    
      LEVEL_INFO
    
      LEVEL_WARN
    
      LEVEL_ERROR
    
      LEVEL_CRITICAL
    
      LEVEL_OFF
    """
    LEVEL_CRITICAL: typing.ClassVar[OutLevel]  # value = <OutLevel.LEVEL_CRITICAL: 5>
    LEVEL_DEBUG: typing.ClassVar[OutLevel]  # value = <OutLevel.LEVEL_DEBUG: 1>
    LEVEL_ERROR: typing.ClassVar[OutLevel]  # value = <OutLevel.LEVEL_ERROR: 4>
    LEVEL_INFO: typing.ClassVar[OutLevel]  # value = <OutLevel.LEVEL_INFO: 2>
    LEVEL_OFF: typing.ClassVar[OutLevel]  # value = <OutLevel.LEVEL_OFF: 6>
    LEVEL_TRACE: typing.ClassVar[OutLevel]  # value = <OutLevel.LEVEL_TRACE: 0>
    LEVEL_WARN: typing.ClassVar[OutLevel]  # value = <OutLevel.LEVEL_WARN: 3>
    __members__: typing.ClassVar[dict[str, OutLevel]]  # value = {'LEVEL_TRACE': <OutLevel.LEVEL_TRACE: 0>, 'LEVEL_DEBUG': <OutLevel.LEVEL_DEBUG: 1>, 'LEVEL_INFO': <OutLevel.LEVEL_INFO: 2>, 'LEVEL_WARN': <OutLevel.LEVEL_WARN: 3>, 'LEVEL_ERROR': <OutLevel.LEVEL_ERROR: 4>, 'LEVEL_CRITICAL': <OutLevel.LEVEL_CRITICAL: 5>, 'LEVEL_OFF': <OutLevel.LEVEL_OFF: 6>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OutMode:
    """
    Members:
    
      SYNC
    
      ASYNC
    """
    ASYNC: typing.ClassVar[OutMode]  # value = <OutMode.ASYNC: 2>
    SYNC: typing.ClassVar[OutMode]  # value = <OutMode.SYNC: 1>
    __members__: typing.ClassVar[dict[str, OutMode]]  # value = {'SYNC': <OutMode.SYNC: 1>, 'ASYNC': <OutMode.ASYNC: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OutPosition:
    """
    Members:
    
      CONSOLE
    
      FILE
    
      CONSOLE_AND_FILE
    """
    CONSOLE: typing.ClassVar[OutPosition]  # value = <OutPosition.CONSOLE: 1>
    CONSOLE_AND_FILE: typing.ClassVar[OutPosition]  # value = <OutPosition.CONSOLE_AND_FILE: 3>
    FILE: typing.ClassVar[OutPosition]  # value = <OutPosition.FILE: 2>
    __members__: typing.ClassVar[dict[str, OutPosition]]  # value = {'CONSOLE': <OutPosition.CONSOLE: 1>, 'FILE': <OutPosition.FILE: 2>, 'CONSOLE_AND_FILE': <OutPosition.CONSOLE_AND_FILE: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
ASYNC: OutMode  # value = <OutMode.ASYNC: 2>
CONSOLE: OutPosition  # value = <OutPosition.CONSOLE: 1>
CONSOLE_AND_FILE: OutPosition  # value = <OutPosition.CONSOLE_AND_FILE: 3>
FILE: OutPosition  # value = <OutPosition.FILE: 2>
LEVEL_CRITICAL: OutLevel  # value = <OutLevel.LEVEL_CRITICAL: 5>
LEVEL_DEBUG: OutLevel  # value = <OutLevel.LEVEL_DEBUG: 1>
LEVEL_ERROR: OutLevel  # value = <OutLevel.LEVEL_ERROR: 4>
LEVEL_INFO: OutLevel  # value = <OutLevel.LEVEL_INFO: 2>
LEVEL_OFF: OutLevel  # value = <OutLevel.LEVEL_OFF: 6>
LEVEL_TRACE: OutLevel  # value = <OutLevel.LEVEL_TRACE: 0>
LEVEL_WARN: OutLevel  # value = <OutLevel.LEVEL_WARN: 3>
SYNC: OutMode  # value = <OutMode.SYNC: 1>
