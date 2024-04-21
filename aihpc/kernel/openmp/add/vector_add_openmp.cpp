/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-20 15:47:11
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-21 23:18:09
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/openmp/add/vector_add_openmp.cpp
 */
#include <iostream>
#include <vector>
#include <chrono>
#include <omp.h>
#include <immintrin.h>
#include "vector_add_openmp.h"

void kernel::openmp::vector_add_kernel(float *a, float *b, float *c, int n)
{   
#pragma omp parallel for
    for (int i = 0; i < n; ++i)
    {
        c[i] = a[i] + b[i];
    }
}

void kernel::openmp::vector_add_kernel_AVX2(float *a, float *b, float *c, int n)
{   
    // int loop = n / 8;
    // for (int tid = 0; tid < loop; tid++)
    // {
    //     __m256i aavx2 = _mm256_loadu_si256((__m256i*)(&a[tid * 8]));
    //     __m256i bavx2 = _mm256_loadu_si256((__m256i*)(&b[tid * 8]));
    //     __m256i cavx2 = _mm256_add_epi32(aavx2, bavx2);
    //     _mm256_storeu_si256((__m256i*)(&c[tid * 8]), cavx2);
    // }
    // #pragma omp parallel for
    // for (int i = loop * 8; i < n; i++)
    // {
    //     c[i] = a[i] + b[i];
    // }
}

void kernel::openmp::launch_vector_add_kernel(const torch::Tensor &a, const torch::Tensor &b, torch::Tensor &c, bool in_place){
    if (a.is_cpu() && b.is_cpu())
    {
        if (a.numel() != b.numel())
        {
            std::cerr << "The input tensor must have the same size" << std::endl;
            return;
        }
        {
            vector_add_kernel(a.data_ptr<float>(), b.data_ptr<float>(), c.data_ptr<float>(), a.numel());
        }
    }else{
        std::cerr << "The input tensor must be on CPU" << std::endl;
        return;
    }
}