cmake_minimum_required(VERSION 3.22)

project(aihpc_C LANGUAGES CXX)

option(BUILD_CUDA_KERNEL "weather to build CUDA kernel" ON)
option(BUILD_OPENMP_KERNEL "weather to build OpenMP kernel" ON)
option(BUILD_STUB_FILES "weather to generate *.pyi file" OFF)
option(BUILD_TESTS "weather to run unitest" OFF)

# set compile option
#! can use macro to reduce code
if(BUILD_CUDA_KERNEL)
    set(BUILD_CUDA_KERNEL ON CACHE INTERNAL "build CUDA kernel")
    add_compile_definitions(BUILD_CUDA_KERNEL)
else()
    set(BUILD_CUDA_KERNEL OFF CACHE INTERNAL "NOT build CUDA kernel")
endif()

if(BUILD_OPENMP_KERNEL)
    set(BUILD_OPENMP_KERNEL ON CACHE INTERNAL "build OpenMP kernel")
    add_compile_definitions(BUILD_OPENMP_KERNEL)
else()
    set(BUILD_OPENMP_KERNEL OFF CACHE INTERNAL "NOT build OpenMP kernel")
endif()

add_subdirectory(third_party)
add_subdirectory(aihpc)

# CTest related
if(BUILD_TESTS)
    enable_testing()
    include(GoogleTest)
    add_subdirectory(third_party/googletest)
    add_subdirectory(tests)
endif()