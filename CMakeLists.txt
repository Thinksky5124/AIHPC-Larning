cmake_minimum_required(VERSION 3.22)

project(aihpc_learning LANGUAGES CXX)

add_subdirectory(third_party)
add_subdirectory(aihpc)

option(BUILD_TESTS "weather to run unitest" ON)

# CTest related
if(BUILD_TESTS)
    enable_testing()
    include(GoogleTest)
    add_subdirectory(tests)
endif()