/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-19 14:58:10
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-22 11:02:36
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/core/cc/core_py_module.h
 */
#pragma once
#include <torch/extension.h>
#include <pybind11/pybind11.h>
#include "core.h"

namespace core
{
    void define_core_module(pybind11::module &m);

    void add_CCLogger_to_module(pybind11::module &m);
} // namespace kernel