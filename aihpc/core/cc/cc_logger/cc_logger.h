/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-22 10:00:54
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-22 21:06:01
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/core/cc/cc_logger/cc_logger.h
 */
#pragma once
#include  <memory>
#include "spdlog/spdlog.h"

// define LOG_NAME
#define LOG_NAME "AIHPC"
// Encapsulate a macro, without which information such as file name and line number cannot be output
#define LOG_TRACE(name, ...) SPDLOG_LOGGER_CALL(spdlog::get((name)), spdlog::level::trace, __VA_ARGS__)
#define LOG_DEBUG(name,...) SPDLOG_LOGGER_CALL(spdlog::get((name)), spdlog::level::debug, __VA_ARGS__)
#define LOG_INFO(name,...) SPDLOG_LOGGER_CALL(spdlog::get((name)), spdlog::level::info, __VA_ARGS__)
#define LOG_WARN(name,...) SPDLOG_LOGGER_CALL(spdlog::get((name)), spdlog::level::warn, __VA_ARGS__)
#define LOG_ERROR(name,...) SPDLOG_LOGGER_CALL(spdlog::get((name)), spdlog::level::err, __VA_ARGS__)
#define LOG_CRITI(name,...) SPDLOG_LOGGER_CALL(spdlog::get((name)), spdlog::level::critical, __VA_ARGS__)

namespace core
{
namespace Logger {
    class CCLogger
    {
    private:
        bool m_bInit;
    public:
        enum OutPosition{
            CONSOLE             = 0x01,
            FILE                = 0x02,
            CONSOLE_AND_FILE    = 0x03,
        };

        enum OutMode{
            SYNC                = 0x01,
            ASYNC               = 0x02,
        };

        enum OutLevel{
            LEVEL_TRACE               = 0x00,
            LEVEL_DEBUG               = 0x01,
            LEVEL_INFO                = 0x02,
            LEVEL_WARN                = 0x03,
            LEVEL_ERROR               = 0x04,
            LEVEL_CRITICAL            = 0x05,
            LEVEL_OFF                 = 0x06,
        };

        CCLogger(const std::string& name, const std::string& root_path,
                OutLevel eOutLevel=LEVEL_TRACE, OutPosition eOutPosition=CONSOLE_AND_FILE,
                OutMode eOutMode=SYNC);
        ~CCLogger();

        std::shared_ptr<spdlog::logger> m_pLogger;
        std::string name;

        bool init_logger(const std::string& name, const std::string& root_path,
                        OutLevel eOutLevel=LEVEL_TRACE, OutPosition eOutPosition=CONSOLE_AND_FILE,
                        OutMode eOutMode=SYNC);
        void uninit_logger();

        void set_logger_level(OutLevel eOutLevel);
        void log (OutLevel level, const std::string& message) const;
        void log_trace(const std::string& message) const;
        void log_debug(const std::string& message) const;
        void log_info(const std::string& message) const;
        void log_warn(const std::string& message) const;
        void log_error(const std::string& message) const;
        void log_critical(const std::string& message) const;
    
        CCLogger(const CCLogger&) = delete;
        CCLogger& operator=(const CCLogger&) = delete;
    };
}
} // namespace core

