project(cuda_kernel LANGUAGES CXX CUDA)

enable_language(CUDA)

include_directories(${TORCH_INCLUDE_DIRS} ${CMAKE_CUDA_TOOLKIT_INCLUDE_DIRECTORIES})

file(GLOB_RECURSE CPP_SOURCES "*.cpp" "*.h")
file(GLOB_RECURSE CUDA_SOURCES "*.cu" "*.cuh")

cuda_add_library(cuda_kernel
                 SHARED
                 ${CUDA_SOURCES}
                 ${CPP_SOURCES})

target_link_libraries(cuda_kernel ${TORCH_LIBRARIES} ${CUDA_LIBRARIES})
target_include_directories(cuda_kernel PRIVATE ${TORCH_INCLUDE_DIRS} ${CMAKE_CUDA_TOOLKIT_INCLUDE_DIRECTORIES})

set_target_properties(cuda_kernel PROPERTIES CUDA_SEPARABLE_COMPILATION ON)