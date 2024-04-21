/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-20 15:21:12
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-21 22:46:53
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/openmp/add/vector_add.h
 */
#pragma once
#include <torch/extension.h>
#include <pybind11/pybind11.h>
#include "vector_add_openmp.h"

namespace kernel
{
    namespace openmp
    {
        torch::Tensor add(const torch::Tensor &a, const torch::Tensor &b, bool in_place=false);
    } // namespace cuda
} // namespace kernel