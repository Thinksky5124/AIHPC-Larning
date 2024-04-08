/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-07 15:59:12
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-08 20:09:37
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/cuda/vector_add/vector_add_cuda.cuh
 */
#pragma once
#include <torch/all.h>
#include "stdio.h"
#include <cuda_runtime_api.h>
#include <cuda.h>

#define CHECK_CUDA(x) TORCH_CHECK(x.device().is_cuda(), #x " must be a CUDA tensor")
#define CHECK_CONTIGUOUS(x) TORCH_CHECK(x.is_contiguous(), #x " must be contiguous")
#define CHECK_INPUT(x) CHECK_CUDA(x); CHECK_CONTIGUOUS(x)

namespace cuda_kernel
{
__global__ void vector_add_kernel(double *a, double *b, double *c);
void launch_vector_add_kernel();
} // namespace cuda_kernel
