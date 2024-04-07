'''
Author       : Thinksky5124
Date         : 2024-04-07 23:31:04
LastEditors  : Thinksky5124
LastEditTime : 2024-04-07 23:32:08
Description  : ref: https://github.com/pytorch/pytorch/blob/main/tools/generate_torch_version.py
FilePath     : /AIHPC-Larning/tools/generate_version.py
'''
import argparse
import os
import re
import subprocess
from pathlib import Path
from typing import Optional, Union

from setuptools import distutils  # type: ignore[import]


UNKNOWN = "Unknown"
RELEASE_PATTERN = re.compile(r"/v[0-9]+(\.[0-9]+)*(-rc[0-9]+)?/")

def get_sha(package_root: Union[str, Path]) -> str:
    try:
        rev = None
        if os.path.exists(os.path.join(package_root, ".git")):
            rev = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=package_root
            )
        elif os.path.exists(os.path.join(package_root, ".hg")):
            rev = subprocess.check_output(
                ["hg", "identify", "-r", "."], cwd=package_root
            )
        if rev:
            return rev.decode("ascii").strip()
    except Exception:
        pass
    return UNKNOWN

def get_version(sha: Optional[str] = None) -> str:
    package_root = Path(__file__).parent.parent
    version = open(package_root / "version.txt").read().strip()

    if os.getenv("AIHPC_BUILD_VERSION"):
        assert os.getenv("AIHPC_BUILD_NUMBER") is not None
        build_number = int(os.getenv("AIHPC_BUILD_NUMBER", ""))
        version = os.getenv("AIHPC_BUILD_VERSION", "")
        if build_number > 1:
            version += ".post" + str(build_number)
    elif sha != UNKNOWN:
        if sha is None:
            sha = get_sha(package_root)
        version += "+git" + sha[:7]
    return version