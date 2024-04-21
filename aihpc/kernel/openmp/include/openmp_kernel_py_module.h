/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-20 15:21:43
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-20 15:21:59
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/openmp/include/openmp_kernel_py_module.h
 */
#pragma once
#include <torch/all.h>
#include <pybind11/pybind11.h>

namespace kernel
{
    namespace openmp
    {
        void add_vector_add_to_module(pybind11::module &m);
        void define_openmp_kernel_module(pybind11::module &m);
    } // namespace opemmp
} // namespace kernel