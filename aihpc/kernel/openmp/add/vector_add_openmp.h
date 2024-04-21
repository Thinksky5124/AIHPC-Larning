/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-20 15:47:20
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-21 22:47:50
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/openmp/add/vector_add_openmp.h
 */
#pragma once
#include <torch/extension.h>
#include <pybind11/pybind11.h>
#include <omp.h>
namespace kernel
{
namespace openmp
{
    void vector_add_kernel(float *a, float *b, float *c, int n);
    void vector_add_kernel_AVX2(float *a, float *b, float *c, int n);
    void launch_vector_add_kernel(const torch::Tensor &a, const torch::Tensor &b, torch::Tensor &c, bool in_place);
} // namespace openmp
    
} // namespace kernel
