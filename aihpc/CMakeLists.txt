project(aihpc_cpp LANGUAGES CXX)

# execute_process(
#   COMMAND conda env list
#   COMMAND grep "torch"
#   OUTPUT_VARIABLE CONDA_PREFIX_RAW
#   OUTPUT_STRIP_TRAILING_WHITESPACE
# )

# message("CONDA_PREFIX = ${CONDA_PREFIX_RAW}")

set(Python_ROOT_DIR "/home/wenwujun/miniconda3/envs/torch")
find_package (Python COMPONENTS Interpreter Development)

set(Torch_DIR "${Python_STDLIB}/site-packages/torch/share/cmake/Torch")
find_package(Torch REQUIRED)
find_package(CUDAToolkit REQUIRED)

#-------------------------------------------------------------------#
# Configuration summary
#-------------------------------------------------------------------#
message("//===================================================")
message("  ${PROJECT_NAME} build configuration:")
message("//===================================================")
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
message("  Torch_cxx_flags  : ${TORCH_CXX_FLAGS}")

add_subdirectory(kernel)

add_library(${PROJECT_NAME} ALIAS kernel)

# VERSION_INFO is defined by setup.py and passed into the C++ code as a
# define (VERSION_INFO) here.
target_compile_definitions(kernel
                           PRIVATE VERSION_INFO=${VERSION_INFO})
set_target_properties(kernel PROPERTIES PREFIX "")
set_target_properties(kernel PROPERTIES OUTPUT_NAME ${PROJECT_NAME})