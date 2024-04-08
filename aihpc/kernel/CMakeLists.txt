cmake_minimum_required(VERSION 3.22)

project(kernel LANGUAGES CXX)

add_subdirectory(cuda)
add_subdirectory(openmp)

file(GLOB_RECURSE TOP_CPP_SOURCES "common/*.cpp" "common/*.h")

add_library(kernel SHARED ${TOP_CPP_SOURCES})

target_link_libraries(kernel cuda_kernel)
