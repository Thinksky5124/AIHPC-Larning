/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-19 14:49:48
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-20 17:05:02
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/core/cc/core_py_module.cpp
 */
#include "core_py_module.h"
#include <torch/extension.h>
#include <pybind11/pybind11.h>

namespace core
{
    void define_core_module(pybind11::module &m)
    {
        py::module core = m.def_submodule("core", "CUDA Kernel module");

    }
} // namespace kernel