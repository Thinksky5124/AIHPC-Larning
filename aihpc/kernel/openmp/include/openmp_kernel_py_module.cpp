/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-20 15:21:33
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-21 23:19:46
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/openmp/include/openmp_kernel_py_module.cpp
 */
#include <torch/extension.h>
#include <pybind11/pybind11.h>
#include "openmp_kernel_py_module.h"
#include "../add/vector_add.h"
namespace py = pybind11;

namespace kernel
{
    namespace openmp
    {   
        void add_add_to_module(pybind11::module &m)
        {
            m.def("add", &add, "Add Two Tensor", py::arg("a"), py::arg("b"), py::arg("in_place") = false);
        }

        void define_openmp_kernel_module(pybind11::module &m){
            py::module openmp = m.def_submodule("openmp", "OpenMP Kernel module");

            // add kernel to module
            add_add_to_module(openmp);
        }
    } // namespace cuda
} // namespace kernel