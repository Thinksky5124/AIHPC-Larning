'''
Author       : Thinksky5124
Date         : 2024-03-26 20:05:40
LastEditors  : Thinksky5124
LastEditTime : 2024-03-27 19:55:21
Description  : file content
FilePath     : /AIHPC-Larning/tools/launch.py
'''
import argparse
import os
import sys
path = os.path.join(os.getcwd())
sys.path.append(path)
import random

import numpy as np
import torch
from aihpc.core.utils.logger import get_logger
from aihpc.core.utils.config import get_config


def parse_args():
    parser = argparse.ArgumentParser("AIHPC launch script")
    parser.add_argument('-c',
                        '--config',
                        type=str,
                        default='configs/example.yaml',
                        help='config file path')
    parser.add_argument('-o',
                        '--override',
                        action='append',
                        default=[],
                        help='config options to be overridden')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    cfg = get_config(args.config, overrides=args.override)

if __name__ == '__main__':
    main()
