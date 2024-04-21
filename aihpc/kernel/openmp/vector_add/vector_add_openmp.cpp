/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-20 15:47:11
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-20 15:59:40
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/openmp/vector_add/vector_add_openmp.cpp
 */
#include <iostream>
#include <vector>
#include <chrono>
#include <omp.h>
#include "vector_add_openmp.h"

void kernel::openmp::vector_add_kernel()
{   
    std::vector<int> data(10000000, 1);
    // #pragma omp parallel
    {
        std::vector<int> result(data.size());
#pragma omp parallel for
        for (int i = 0; i < data.size(); ++i)
        {
            if (i >= 0 && i <= 1000000)
            {
                // 使用 OpenMP 并行计算
                result[i] = data[i] * 2;
            }
        }
    }
}

void kernel::openmp::launch_vector_add_kernel(){
    vector_add_kernel();
}