/*
 * @Author       : Thinksky5124
 * @Date         : 2024-04-20 15:14:00
 * @LastEditors  : Thinksky5124
 * @LastEditTime : 2024-04-20 17:16:41
 * @Description  : file content
 * @FilePath     : /AIHPC-Larning/aihpc/kernel/openmp/vector_add/vector_add.cpp
 */
#include "vector_add.h"

namespace kernel
{
namespace openmp
{
    void vector_add(){
        launch_vector_add_kernel();
    }
} // namespace cuda
    
} // namespace kernel