/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-07 13:57:12
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-21 21:20:34
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/tests/test_cases/kernel/cuda/test_cuda.cpp
 */
#include "gtest/gtest.h"
#include "../../../aihpc/include/aihpc.h"
#include <torch/torch.h>

TEST(TestAddTensor, test_add_1) {
  torch::Tensor a = torch::ones({2, 2}, torch::kFloat32);
  torch::Tensor b = torch::ones({2, 2}, torch::kFloat32);
  torch::Tensor c_c = a + b;
  torch::Tensor c = kernel::cuda::add(a, b, false);
  EXPECT_EQ(torch::allclose(c, c_c), true);
}