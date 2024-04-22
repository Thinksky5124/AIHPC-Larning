/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-22 10:00:48
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-22 21:15:59
 * @Description  : ref: https://blog.csdn.net/qq_41768362/article/details/127024667
 * @FilePath     : /AIHPC-Larning/aihpc/core/cc/cc_logger/cc_logger.cpp
 */
#include "cc_logger.h"
#include <fstream>
#include <iostream>
#include <string>
#include <chrono>
#include <iomanip>
#include "spdlog/sinks/stdout_color_sinks.h"
#include "spdlog/sinks/basic_file_sink.h"
#include "spdlog/async.h"

core::Logger::CCLogger::CCLogger(const std::string& name, const std::string& root_path,
                        OutLevel eOutLevel, OutPosition eOutPosition, OutMode eOutMode): m_bInit(false), name(name){
    this->init_logger(name, root_path, eOutLevel, eOutPosition, eOutMode);
}

core::Logger::CCLogger::~CCLogger(){
    if(m_bInit){
        this->uninit_logger();
    }
}

bool core::Logger::CCLogger::init_logger(const std::string& name, const std::string& root_path,
                        OutLevel eOutLevel, OutPosition eOutPosition, OutMode eOutMode){
    try
    {
        const char* pFormat = "[%Y-%m-%d %H:%M:%S.%e] <thread %t> [%l] [%@] %v";
        //sink container
        std::vector<spdlog::sink_ptr> vSinks;

        if (eOutPosition & CONSOLE)
        {
            auto console_sink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();
            console_sink->set_pattern(pFormat);
            vSinks.push_back(console_sink);
        }
        
        if (eOutPosition & FILE)
        {
            auto now = std::chrono::system_clock::now();
            std::time_t now_c = std::chrono::system_clock::to_time_t(now);
            std::ostringstream ss;
            ss << std::put_time(std::localtime(&now_c), "%Y%m%d%H%M%S");
            std::string str_time = ss.str();
            auto file_sink = std::make_shared<spdlog::sinks::basic_file_sink_mt>(root_path + "/" + name + "_CCLogger_" + str_time + ".log", true);
            file_sink->set_pattern(pFormat);
            vSinks.push_back(file_sink);
        }
        
        if (eOutMode == ASYNC)
        {
            spdlog::init_thread_pool(120400, 1);
            auto tp = spdlog::thread_pool();
            m_pLogger = std::make_shared<spdlog::async_logger>(name, vSinks.begin(), vSinks.end(), tp, spdlog::async_overflow_policy::block);
        }else{
            m_pLogger = std::make_shared<spdlog::logger>(name, vSinks.begin(), vSinks.end());
        }

        this->name = name;
        m_pLogger->set_level((spdlog::level::level_enum)eOutLevel);

        // flush the file immediately when encounter a warn level
        m_pLogger->flush_on((spdlog::level::level_enum)eOutLevel);
        // flush files periodically and flush them every seconds
        spdlog::flush_every(std::chrono::seconds(1));
        spdlog::register_logger(m_pLogger);
        m_bInit = true;
    }
    catch(const spdlog::spdlog_ex& e)
    {
        std::cerr << "Log initialization failed: " << e.what() << '\n';
        return false;
    }
    return true;
}

void core::Logger::CCLogger::uninit_logger(){
    if(m_bInit){
        m_pLogger->flush();
        spdlog::drop_all();
        spdlog::shutdown();
        m_bInit = false;
    }
}

void core::Logger::CCLogger::set_logger_level(OutLevel eOutLevel){
    if(m_bInit){
        m_pLogger->set_level((spdlog::level::level_enum)eOutLevel);
    }
}

void core::Logger::CCLogger::log (OutLevel level, const std::string& message) const {
    if(m_bInit){
        this->m_pLogger->log((spdlog::level::level_enum)level, message);
    }
}

void core::Logger::CCLogger::log_trace(const std::string& message) const{
    if(m_bInit){
        this->m_pLogger->trace(message);
    }
}

void core::Logger::CCLogger::log_critical(const std::string& message) const{
    if(m_bInit){
        this->m_pLogger->critical(message);
    }
}

void core::Logger::CCLogger::log_debug(const std::string& message) const{
    if(m_bInit){
        this->m_pLogger->debug(message);
    }
}

void core::Logger::CCLogger::log_error(const std::string& message) const{
    if(m_bInit){
        this->m_pLogger->error(message);
    }
}

void core::Logger::CCLogger::log_info(const std::string& message) const{
    if(m_bInit){
        // this->m_pLogger->info(message);
        LOG_INFO(name, message);
    }
}

void core::Logger::CCLogger::log_warn(const std::string& message) const{
    if(m_bInit){
        this->m_pLogger->warn(message);
    }
}