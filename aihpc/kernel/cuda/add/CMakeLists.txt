file(GLOB_RECURSE CUDA_SOURCES "*.cu")
file(GLOB_RECURSE CUDA_HEADERS "*.cuh")
file(GLOB_RECURSE CPP_SOURCES "*.cpp" "*.cc")
file(GLOB_RECURSE CPP_HEADERS "*.h" "*.hpp")

set(KERNEL_GPU_SRCS ${KERNEL_GPU_SRCS} ${CUDA_SOURCES})
set(KERNEL_INCLUDE_DIR ${KERNEL_INCLUDE_DIR} ${CMAKE_CURRENT_LIST_DIR})
set(KERNEL_SRCS ${KERNEL_SRCS} ${CPP_SOURCES})
set(KERNEL_GPU_INCLUDE_DIR ${KERNEL_GPU_INCLUDE_DIR} ${CMAKE_CURRENT_LIST_DIR})

set(KERNEL_SRCS ${KERNEL_SRCS} PARENT_SCOPE)
set(KERNEL_INCLUDE_DIR ${KERNEL_INCLUDE_DIR} PARENT_SCOPE)

set(KERNEL_GPU_SRCS ${KERNEL_GPU_SRCS} PARENT_SCOPE)
set(KERNEL_GPU_INCLUDE_DIR ${KERNEL_GPU_INCLUDE_DIR} PARENT_SCOPE)