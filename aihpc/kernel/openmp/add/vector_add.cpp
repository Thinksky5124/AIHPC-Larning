/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-20 15:14:00
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-21 22:47:04
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/openmp/add/vector_add.cpp
 */
#include "vector_add.h"

namespace kernel
{
namespace openmp
{
    torch::Tensor add(const torch::Tensor &a, const torch::Tensor &b, bool in_place){
        torch::Tensor c = torch::empty_like(a);
        launch_vector_add_kernel(a, b, c, in_place);
        return c;
    }
} // namespace cuda
    
} // namespace kernel