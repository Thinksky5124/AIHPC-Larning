add_subdirectory(add)

file(GLOB_RECURSE CPP_SOURCES "include/*.cpp" "include/*.cc")

set(KERNEL_SRCS ${KERNEL_SRCS} ${CPP_SOURCES})
set(KERNEL_INCLUDE_DIR ${KERNEL_INCLUDE_DIR} ${CMAKE_CURRENT_LIST_DIR}/include)

set(KERNEL_SRCS ${KERNEL_SRCS} PARENT_SCOPE)
set(KERNEL_INCLUDE_DIR ${KERNEL_INCLUDE_DIR} PARENT_SCOPE)

set(KERNEL_GPU_SRCS ${KERNEL_GPU_SRCS} PARENT_SCOPE)
set(KERNEL_GPU_INCLUDE_DIR ${KERNEL_GPU_INCLUDE_DIR} PARENT_SCOPE)