/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-20 15:21:12
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-20 16:00:31
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/openmp/vector_add/vector_add.h
 */
#pragma once
#include <torch/extension.h>
#include <pybind11/pybind11.h>
#include "vector_add_openmp.h"

namespace kernel
{
    namespace openmp
    {
        torch::Tensor add(torch::Tensor a, torch::Tensor b);
    } // namespace cuda
} // namespace kernel