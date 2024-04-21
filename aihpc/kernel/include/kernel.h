/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-20 17:08:35
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-20 22:36:09
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/include/kernel.h
 */
#pragma once
#ifdef BUILD_CUDA_KERNEL
#include "../cuda/include/cuda_kernel.h"
#endif
#ifdef BUILD_OPENMP_KERNEL
#include "../openmp/include/openmp_kernel.h"
#endif