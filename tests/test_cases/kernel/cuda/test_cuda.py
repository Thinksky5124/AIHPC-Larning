'''
Author       : Thinksky5124
Date         : 2024-04-19 10:42:16
LastEditors  : Thinksky5124
LastEditTime : 2024-04-21 20:52:17
Description  : file content
FilePath     : /AIHPC-Larning/tests/test_cases/kernel/cuda/test_cuda.py
'''
import aihpc
import torch

class TestCUDA:
    def test_add(self):
        a = torch.randn(3, 3)
        b = torch.randn(3, 3)
        c_c = a + b
        c = aihpc._C.kernel.cuda.add(a, b, False)
        assert torch.allclose(c, c_c)