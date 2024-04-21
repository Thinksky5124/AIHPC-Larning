/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-18 15:29:18
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-21 21:15:49
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/cuda/add/vector_add.h
 */
#pragma once
#include <torch/extension.h>
#include <pybind11/pybind11.h>
#include "vector_add_cuda.cuh"

namespace kernel
{
    namespace cuda
    {
        torch::Tensor add(const torch::Tensor &a, const torch::Tensor &b, bool in_place=false);
    } // namespace cuda
} // namespace kernel
