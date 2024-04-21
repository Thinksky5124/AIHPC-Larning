/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-19 14:56:41
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-21 19:38:10
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/cc/aihpc_py_module.cpp
 */
#include "aihpc_py_module.h"
#include "../kernel/include/kernel_py_module.h"
#include "../core/cc/core_py_module.h"

PYBIND11_MODULE(_C, m) {
    m.doc() = "AIHPC CC Functions Module";
    kernel::define_kernel_module(m);
    core::define_core_module(m);
}