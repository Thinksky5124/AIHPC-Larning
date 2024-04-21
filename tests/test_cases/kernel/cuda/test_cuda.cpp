/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-07 13:57:12
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-20 16:37:31
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/tests/test_cases/kernel/cuda/test_cuda.cpp
 */
#include "gtest/gtest.h"
#include "../../../aihpc/include/aihpc.h"

TEST(TestAddInt, test_add_int_1) {
  kernel::cuda::vector_add();
  EXPECT_EQ(1, 1);
}