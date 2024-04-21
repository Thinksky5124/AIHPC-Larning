/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-18 15:29:12
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-21 20:42:30
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/cuda/add/vector_add.cpp
 */
#include <torch/extension.h>
#include <pybind11/pybind11.h>
#include "vector_add_cuda.cuh"
#include "vector_add.h"

namespace kernel
{
    namespace cuda
    {
        torch::Tensor add(const torch::Tensor &a, const torch::Tensor &b, bool in_place)
        {
            torch::Tensor c = torch::empty_like(a);
            launch_vector_add_kernel(a, b, c, in_place);
            return c;
        }
    } // namespace cuda
    
} // namespace kernel