/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-18 15:29:18
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-20 16:12:23
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/cuda/vector_add/vector_add.h
 */
#pragma once
#include <torch/all.h>
#include <pybind11/pybind11.h>
#include "vector_add_cuda.cuh"

namespace kernel
{
    namespace cuda
    {
        void vector_add();
    } // namespace cuda
} // namespace kernel
