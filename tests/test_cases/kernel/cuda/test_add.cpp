/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-07 13:57:12
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-07 15:54:42
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/tests/test_cases/kernel/cuda/test_add.cpp
 */
#include "gtest/gtest.h"

TEST(TestAddInt, test_add_int_1) {
  int res = 10 + 34;
  EXPECT_EQ(res, 44);
}