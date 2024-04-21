/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-19 14:57:44
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-19 14:58:39
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/common/kernel_pybind11_module.h
 */
#pragma once
#include <torch/all.h>
#include <pybind11/pybind11.h>

namespace kernel
{
    void define_kernel_module(pybind11::module &m);
    
} // namespace kernel
