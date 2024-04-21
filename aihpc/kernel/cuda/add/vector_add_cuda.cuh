/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-07 15:59:12
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-21 20:54:00
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/cuda/add/vector_add_cuda.cuh
 */
#pragma once
#include <torch/extension.h>
#include "stdio.h"
#include <cuda_runtime_api.h>
#include <cuda.h>
#include <pybind11/pybind11.h>

namespace kernel
{
namespace cuda
{
__global__ void vector_add_kernel(const float *A, const float *B,
                                    float *C, int numElements);
void launch_vector_add_kernel(const torch::Tensor &a, const torch::Tensor &b, torch::Tensor &c, bool in_place);
} // namespace cuda
} // namespace kernel


