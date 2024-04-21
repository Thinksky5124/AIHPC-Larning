/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-20 15:14:00
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-21 20:28:32
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/openmp/add/vector_add.cpp
 */
#include "vector_add.h"

namespace kernel
{
namespace openmp
{
    torch::Tensor add(torch::Tensor a, torch::Tensor b){
        launch_vector_add_kernel();
    }
} // namespace cuda
    
} // namespace kernel