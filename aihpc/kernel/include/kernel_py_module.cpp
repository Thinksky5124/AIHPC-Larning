/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-08 21:00:14
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-20 22:37:42
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/include/kernel_py_module.cpp
 */
#include <torch/extension.h>
#include <pybind11/pybind11.h>
#include "kernel_py_module.h"
#ifdef BUILD_CUDA_KERNEL
#include "../cuda/include/cuda_kernel_py_module.h"
#endif
#ifdef BUILD_OPENMP_KERNEL
#include "../openmp/include/openmp_kernel_py_module.h"
#endif

namespace kernel
{
    void define_kernel_module(pybind11::module &m)
    {
        py::module kernel = m.def_submodule("kernel", "AIHPC Kernel Functions Module");

        // add kernel to module
        #ifdef BUILD_CUDA_KERNEL
        cuda::define_cuda_kernel_module(kernel);
        #endif

        #ifdef BUILD_OPENMP_KERNEL
        openmp::define_openmp_kernel_module(kernel);
        #endif
    }
} // namespace kernel