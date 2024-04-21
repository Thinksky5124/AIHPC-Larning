r"""
High performance computing knowledge learning warehouse in artificial intelligence
"""
CXX_EXTENSION_ENABLED = False
try:
    from . import _C
    CXX_EXTENSION_ENABLED = True
except:
    pass

from .core import *
from .kernel import *