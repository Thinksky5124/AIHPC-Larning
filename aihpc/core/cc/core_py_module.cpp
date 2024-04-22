/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-19 14:49:48
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-22 16:22:20
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/core/cc/core_py_module.cpp
 */
#include "core_py_module.h"
#include <torch/extension.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace core
{
    void define_core_module(pybind11::module &m)
    {
        py::module core = m.def_submodule("core", "CC Core module");
        
        add_CCLogger_to_module(core);
    }

    void add_CCLogger_to_module(pybind11::module &m)
    {
        py::module spdlog = m.def_submodule("spdlog", "A Python wrapper spdlog module");

        py::enum_<Logger::CCLogger::OutPosition>(spdlog, "OutPosition")
            .value("CONSOLE", Logger::CCLogger::OutPosition::CONSOLE)
            .value("FILE", Logger::CCLogger::OutPosition::FILE)
            .value("CONSOLE_AND_FILE", Logger::CCLogger::OutPosition::CONSOLE_AND_FILE)
            .export_values();
        
        py::enum_<Logger::CCLogger::OutMode>(spdlog, "OutMode")
            .value("SYNC", Logger::CCLogger::OutMode::SYNC)
            .value("ASYNC", Logger::CCLogger::OutMode::ASYNC)
            .export_values();
        
        py::enum_<Logger::CCLogger::OutLevel>(spdlog, "OutLevel")
            .value("LEVEL_TRACE", Logger::CCLogger::OutLevel::LEVEL_TRACE)
            .value("LEVEL_DEBUG", Logger::CCLogger::OutLevel::LEVEL_DEBUG)
            .value("LEVEL_INFO", Logger::CCLogger::OutLevel::LEVEL_INFO)
            .value("LEVEL_WARN", Logger::CCLogger::OutLevel::LEVEL_WARN)
            .value("LEVEL_ERROR", Logger::CCLogger::OutLevel::LEVEL_ERROR)
            .value("LEVEL_CRITICAL", Logger::CCLogger::OutLevel::LEVEL_CRITICAL)
            .value("LEVEL_OFF", Logger::CCLogger::OutLevel::LEVEL_OFF)
            .export_values();

        py::class_<Logger::CCLogger>(spdlog, "CCLogger")
            .def(py::init<const std::string &, const std::string &, Logger::CCLogger::OutLevel, Logger::CCLogger::OutPosition,
                Logger::CCLogger::OutMode>(),
                py::arg("name"), py::arg("root_path"), py::arg("eOutLevel")=Logger::CCLogger::OutLevel::LEVEL_TRACE,
                py::arg("eOutPosition")=Logger::CCLogger::OutPosition::CONSOLE_AND_FILE,
                py::arg("eOutMode")=Logger::CCLogger::OutMode::SYNC)
            .def("init_logger", &Logger::CCLogger::init_logger,
                py::arg("name"), py::arg("root_path"), py::arg("eOutLevel")=Logger::CCLogger::OutLevel::LEVEL_TRACE,
                py::arg("eOutPosition")=Logger::CCLogger::OutPosition::CONSOLE_AND_FILE,
                py::arg("eOutMode")=Logger::CCLogger::OutMode::SYNC)
            .def("uninit_logger", &Logger::CCLogger::uninit_logger)
            .def("set_logger_level", &Logger::CCLogger::set_logger_level, py::arg("eOutLevel"))
            .def("log_trace", &Logger::CCLogger::log_trace, py::arg("msg"))
            .def("log_debug", &Logger::CCLogger::log_debug, py::arg("msg"))
            .def("log_info", &Logger::CCLogger::log_info, py::arg("msg"))
            .def("log_warn", &Logger::CCLogger::log_warn, py::arg("msg"))
            .def("log_error", &Logger::CCLogger::log_error, py::arg("msg"))
            .def("log_critical", &Logger::CCLogger::log_critical, py::arg("msg"))
            .def_readonly("name", &Logger::CCLogger::name);
    }
} // namespace kernel