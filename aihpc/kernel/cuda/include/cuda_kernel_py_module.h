/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-19 11:31:01
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-20 17:15:46
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/cuda/include/cuda_kernel_py_module.h
 */
#pragma once
#include <torch/all.h>
#include <pybind11/pybind11.h>

namespace kernel
{
    namespace cuda
    {
        void define_cuda_kernel_module(pybind11::module &m);
        void add_vector_add_to_module(pybind11::module &m);
    } // namespace cuda
} // namespace kernel