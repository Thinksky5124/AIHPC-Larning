/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-18 15:29:12
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-20 16:12:29
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/cuda/vector_add/vector_add.cpp
 */
#include <torch/all.h>
#include <pybind11/pybind11.h>
#include "vector_add_cuda.cuh"
#include "vector_add.h"

namespace kernel
{
    namespace cuda
    {
        void vector_add()
        {
            launch_vector_add_kernel();
        }
    } // namespace cuda
    
} // namespace kernel