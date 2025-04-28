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
set(Python_ROOT_DIR "/home/users/wujun.wen/miniconda3/envs/torch260_py310")
find_package (Python COMPONENTS Interpreter Development)

set(Torch_DIR "${Python_STDLIB}/site-packages/torch/share/cmake/Torch")
find_package(Torch REQUIRED)

set(PYTHON_NVIDIA_LIBRARIES "")
set(PYTHON_NVIDIA_INCLUDE_DIR "")

if(BUILD_CUDA_KERNEL)
  enable_language(CUDA)
  find_package(CUDAToolkit REQUIRED)

    set(PYTHON_SCRIPT "
import platform
import sys
import os
import glob

def _preload_cuda_deps(lib_folder: str, lib_name: str) -> None:
    '''Preloads cuda deps if they could not be found otherwise.'''
    # Should only be called on Linux if default path resolution have failed
    assert platform.system() == 'Linux', 'Should only be called on Linux'

    lib_path = None
    include_path = None
    for path in sys.path:
        nvidia_path = os.path.join(path, 'nvidia')
        if not os.path.exists(nvidia_path):
            continue
        candidate_lib_paths = glob.glob(
            os.path.join(nvidia_path, lib_folder, 'lib', lib_name)
        )
        # if path/nvidia/lib_folder/ is not found look in path/lib_folder/
        if not candidate_lib_paths:
            candidate_lib_paths = glob.glob(
                os.path.join(path, lib_folder, 'lib', lib_name)
            )

        if candidate_lib_paths and not lib_path:
            lib_path = candidate_lib_paths[0]
        if lib_path:
            include_path = os.path.join('/'.join(candidate_lib_paths[0].split('/')[:-2]), 'include')
            break
    if not lib_path:
        raise ValueError(f'{lib_name} not found in the system path {sys.path}')
    return lib_path, include_path

cuda_libs = {
    'cublas': 'libcublas.so.*[0-9]',
    'cudnn': 'libcudnn.so.*[0-9]',
    'cuda_cupti': 'libcupti.so.*[0-9]',
    'cufft': 'libcufft.so.*[0-9]',
    'curand': 'libcurand.so.*[0-9]',
    'cusparse': 'libcusparse.so.*[0-9]',
    'cusolver': 'libcusolver.so.*[0-9]',
    'nccl': 'libnccl.so.*[0-9]',
}

libs = ''
include = ''

for lib_folder, lib_name in cuda_libs.items():
    lib_path, include_path = _preload_cuda_deps(lib_folder, lib_name)
    libs += f'{lib_path}|'
    include += f'{include_path}|'

libs = libs[:-1]
include = include[:-1]

print(libs + ';' + include)
")

    execute_process(
        COMMAND ${CMAKE_COMMAND} -E echo \"${PYTHON_SCRIPT}\" 
        COMMAND ${Python_EXECUTABLE} -c "${PYTHON_SCRIPT}"
        OUTPUT_VARIABLE PYTHON_OUTPUT
        ERROR_VARIABLE PYTHON_ERROR
        RESULT_VARIABLE PYTHON_RESULT
    )

    string(REPLACE ";" ";" my_list "${PYTHON_OUTPUT}")

    set(index 0)
    foreach(item IN LISTS my_list)
        string(REPLACE "|" ";" path_var "${item}")
        if(index EQUAL 0)
            set(PYTHON_NVIDIA_LIBRARIES "${path_var}")
            message(STATUS "PYTHON_NVIDIA_LIBRARIES: ${PYTHON_NVIDIA_LIBRARIES}")
        else()
            set(PYTHON_NVIDIA_INCLUDE_DIR "${path_var}")
            message(STATUS "PYTHON_NVIDIA_INCLUDE_DIR: ${PYTHON_NVIDIA_INCLUDE_DIR}")
        endif()
        math(EXPR index "${index} + 1")
    endforeach()
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
    include_directories(${CUDAToolkit_INCLUDE_DIRS} ${PYTHON_NVIDIA_INCLUDE_DIR})
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
