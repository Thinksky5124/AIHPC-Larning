'''
Author       : Thinksky5124
Date         : 2024-04-19 10:42:16
LastEditors  : Thinksky5124
LastEditTime : 2024-04-20 22:42:56
Description  : file content
FilePath     : /AIHPC-Larning/tests/test_cases/kernel/cuda/test_cuda.py
'''
import aihpc
import torch

class TestCUDA:
    def test_add(self):
        aihpc._C.kernel.cuda.vector_add(torch.randn(3, 3), torch.randn(3, 3), torch.randn(3, 3))
        assert True