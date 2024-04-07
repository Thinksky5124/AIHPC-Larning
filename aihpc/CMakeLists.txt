project(aihpc_cpp LANGUAGES CXX)

find_package (Python COMPONENTS Interpreter Development)

set(Torch_DIR "${Python_STDLIB}/site-packages/torch/share/cmake/Torch")
find_package(Torch REQUIRED)
find_package(CUDA REQUIRED)

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
message("  CUDA toolkit inc   : ${CMAKE_CUDA_TOOLKIT_INCLUDE_DIRECTORIES}")
message("")
message("  Python_found       : ${Python_FOUND}")
message("  Python version     : ${Python_VERSION}")
message("  Python interpreter : ${Python_EXECUTABLE}")
message("  Python interp. Id  : ${Python_INTERPRETER_ID}")
message("  Python_INCLUDE_DIRS: ${Python_INCLUDE_DIRS}")
message("  Python_LIBRARY_DIRS: ${Python_LIBRARY_DIRS}")
message("  Python_STDLIB: ${Python_STDLIB}")

add_subdirectory(kernel)