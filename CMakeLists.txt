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


message("//=====================FIND PACKAGES======================")
set(Python_ROOT_DIR "/home/wenwujun/miniconda3/envs/torch")
find_package (Python COMPONENTS Interpreter Development)

set(Torch_DIR "${Python_STDLIB}/site-packages/torch/share/cmake/Torch")
find_package(Torch REQUIRED)

if(BUILD_CUDA_KERNEL)
  enable_language(CUDA)
  find_package(CUDAToolkit REQUIRED)
endif()

if(BUILD_OPENMP_KERNEL)
  find_package(OpenMP REQUIRED)
endif()

message("//=====================BUILD ENVIRONMENT======================")
message("  Python_found       : ${Python_FOUND}")
message("  Python version     : ${Python_VERSION}")
message("  Python interpreter : ${Python_EXECUTABLE}")
message("  Python interp. Id  : ${Python_INTERPRETER_ID}")
message("  Python_INCLUDE_DIRS: ${Python_INCLUDE_DIRS}")
message("  Python_LIBRARY_DIRS: ${Python_LIBRARY_DIRS}")
message("  Python_STDLIB: ${Python_STDLIB}")
message("")
message("  Torch_found         : ${Torch_FOUND}")
message("  Torch dir           : ${Torch_DIR}")
message("  Torch libraries     : ${TORCH_LIBRARIES}")
message("  Torch include dirs  : ${TORCH_INCLUDE_DIRS}")
message("  Torch_cuda_libraries: ${TORCH_CUDA_LIBRARIES}")
message("  Torch_cxx_flags     : ${TORCH_CXX_FLAGS}")
message("")

if(BUILD_CUDA_KERNEL)
    message("  CUDA compiler ID      : ${CMAKE_CUDA_COMPILER_ID}")
    message("  CUDA compiler Version : ${CMAKE_CUDA_COMPILER_VERSION}")
    message("  C++ Compiler : ${CMAKE_CXX_COMPILER_ID} "
      "${CMAKE_CXX_COMPILER_VERSION} "
      "${CMAKE_CXX_COMPILER_WRAPPER}")
    message("    ${CMAKE_CXX_COMPILER}")
    message("  CUDA Compiler      : ${CMAKE_CUDA_COMPILER}")
    message("  CUDA Compiler exec : ${CUDA_NVCC_EXECUTABLE}")
    message("  CUDA Compile flags : ${CMAKE_CUDA_FLAGS}")
    message("  CUDA toolkit inc   : ${CUDAToolkit_INCLUDE_DIRS}")
    message("  CUDA library dir   : ${CUDAToolkit_LIBRARY_DIR}")
    message("")
endif()

if(BUILD_OPENMP_KERNEL)
    message("  OpenMP_CXX_VERSION      : ${OpenMP_CXX_VERSION}")
    message("  OpenMP_CXX_FLAGS        : ${OpenMP_CXX_FLAGS}")
    message("  OpenMP_CXX_LIBRARIES     : ${OpenMP_CXX_LIBRARIES}")
    message("  OpenMP_CXX_INCLUDE_DIRS : ${OpenMP_CXX_INCLUDE_DIRS}")
    message("")
endif()

message("//=====================BUILD STATUS======================")
message(STATUS "build CUDA kernel  : ${BUILD_CUDA_KERNEL}")
message(STATUS "build OpenMP kernel: ${BUILD_OPENMP_KERNEL}")
message(STATUS "build tests        : ${BUILD_TESTS}")
message(STATUS "build stub files   : ${BUILD_STUB_FILES}")

include_directories(${Python_INCLUDE_DIRS} ${pybind11_INCLUDE_DIRS}
                    ${TORCH_INCLUDE_DIRS})

if(BUILD_CUDA_KERNEL)
    include_directories(${CUDAToolkit_INCLUDE_DIRS})
endif()

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${TORCH_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
find_library(TORCH_PYTHON_LIBRARY torch_python PATH "${TORCH_INSTALL_PREFIX}/lib")

message("//=====================BUILD MESSAGE======================")

add_subdirectory(third_party)

if(NOT TARGET spdlog)
    # Stand-alone build
    find_package(spdlog REQUIRED)
endif()

add_subdirectory(aihpc)

# CTest related
if(BUILD_TESTS)
    enable_testing()
    include(GoogleTest)
    add_subdirectory(third_party/googletest)
    add_subdirectory(tests)
endif()