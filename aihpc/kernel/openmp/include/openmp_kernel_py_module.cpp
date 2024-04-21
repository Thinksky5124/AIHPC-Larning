/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-20 15:21:33
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-20 16:02:33
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/openmp/include/openmp_kernel_py_module.cpp
 */
#include <torch/all.h>
#include <pybind11/pybind11.h>
#include "openmp_kernel_py_module.h"
#include "../vector_add/vector_add.h"
namespace py = pybind11;

namespace kernel
{
    namespace openmp
    {   
        void add_vector_add_to_module(pybind11::module &m)
        {
            m.def("vector_add", &vector_add, "Vector Add");
        }

        void define_openmp_kernel_module(pybind11::module &m){
            py::module openmp = m.def_submodule("openmp", "OpenMP Kernel module");

            // add kernel to module
            add_vector_add_to_module(openmp);
        }
    } // namespace cuda
} // namespace kernel