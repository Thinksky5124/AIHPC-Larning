/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-20 16:07:35
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-20 16:08:20
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/tests/test_cases/kernel/openmp/test_openmp.cpp
 */
#include "gtest/gtest.h"

TEST(TestAddInt, test_add_int_1) {
  int res = 10 + 34;
  EXPECT_EQ(res, 44);
}