/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-19 14:58:10
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-19 16:32:11
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/core/csrc/core_pybind11_module.h
 */
#pragma once
#include <torch/all.h>
#include <pybind11/pybind11.h>

namespace core
{
    void define_core_module(pybind11::module &m);
} // namespace kernel