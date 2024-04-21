/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-18 16:13:35
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-20 00:02:29
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/cuda/common/cuda_kernel_py_module.cpp
 */
#include <torch/all.h>
#include <pybind11/pybind11.h>
#include "cuda_kernel_py_module.h"
#include "../vector_add/vector_add.h"
namespace py = pybind11;

namespace kernel
{
    namespace cuda
    {   
        void add_vector_add_to_module(pybind11::module &m)
        {
            m.def("vector_add", &vector_add, "Vector Add");
        }
        
        void define_cuda_kernel_module(pybind11::module &m){
            py::module cuda = m.def_submodule("cuda", "CUDA Kernel module");

            // add kernel to module
            add_vector_add_to_module(cuda);
        }
    } // namespace cuda
} // namespace kernel