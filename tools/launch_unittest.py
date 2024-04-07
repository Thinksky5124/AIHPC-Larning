'''
Author       : Thinksky5124
Date         : 2024-03-27 20:11:45
LastEditors  : Thinksky5124
LastEditTime : 2024-04-07 14:41:45
Description  : file content
FilePath     : /AIHPC-Larning/tools/launch_unittest.py
'''
import os
import sys
path = os.path.join(os.getcwd())
sys.path.append(path)
import argparse
import subprocess
from tests.utils import logger_setting
from logging import config, getLogger

def mkdir(dir):
    if not os.path.exists(dir):
        # avoid error when train with multiple gpus
        try:
            os.makedirs(dir)
        except:
            pass

def parse_args():
    parser = argparse.ArgumentParser("AIHPC unit test case script")
    parser.add_argument('-p',
                        '--path_report',
                        type=str,
                        default='./output/test_report',
                        help='test report file path')
    parser.add_argument(
        '-v',
        action='store_true',
        help='whether to detail param during testing case')
    parser.add_argument(
        '-s',
        action='store_true',
        help='whether to print execute information during testing case')
    args = parser.parse_args()
    return args

def run_tests():
    build_dir = "build"
    test_command = ["cmake", "-DBUILD_TESTS=ON"]

    try:
        subprocess.run(test_command, cwd=build_dir, check=True)
        print("Unittest Run Successful!")
    except subprocess.CalledProcessError as e:
        print("Unittest Run Error:", e)
        
if __name__ == '__main__':
    args = parse_args()
    mkdir(args.path_report)
    config.dictConfig(logger_setting.LOGGING_DIC)
    logger = getLogger('test')
    add_args = ''
    if args.v:
        add_args = add_args + '-v '
    if args.s:
        add_args = add_args + '-s '
    os.system(f'pytest tests {add_args}')

    run_tests()
    
    logger.info("All Test Case Finish!")