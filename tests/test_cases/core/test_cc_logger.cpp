/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-22 20:35:10
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-22 20:45:47
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/tests/test_cases/core/test_cc_logger.cpp
 */
#include "gtest/gtest.h"
#include "../../../aihpc/include/aihpc.h"

TEST(TestCCLogger, test_cc_logger_1) {
  core::Logger::CCLogger logger("AIHPC", "./output");
  logger.set_logger_level(core::Logger::CCLogger::OutLevel::LEVEL_TRACE);
  logger.log_trace("test trace");
  logger.log_debug("test debug");
  logger.log_info("test info");
  logger.log_warn("test warn");
  logger.log_error("test error");
  logger.log_critical("test critical");
  logger.uninit_logger();
  EXPECT_EQ(1, 1);
}