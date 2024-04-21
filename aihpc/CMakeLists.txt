cmake_minimum_required(VERSION 3.22)
project(_C LANGUAGES CXX CUDA)

# Define SRCS Variable
set(KERNEL_SRCS)
set(KERNEL_INCLUDE_DIR)
set(KERNEL_GPU_SRCS)
set(KERNEL_GPU_INCLUDE_DIR)
set(KERNEL_OpenMP_SRCS)
set(KERNEL_OpenMP_INCLUDE_DIR)
set(CORE_SRCS)
set(CORE_INCLUDE_DIR)
set(Pybind11_SRCS)

add_subdirectory(kernel)
add_subdirectory(core)

file(GLOB_RECURSE CPP_SOURCES "cc/*.cpp" "cc/*.h" "cc/*.cc" "cc/*.hpp")
set(CPP_SOURCES ${CPP_SOURCES} ${KERNEL_SRCS} ${CORE_SRCS})
file(GLOB_RECURSE Pybind11_SRCS "*_py_module.cpp" "*_py_module.h" "*_py_module.cc")

exclude(CPP_SOURCES "${CPP_SOURCES}" ${Pybind11_SRCS})
exclude(KERNEL_SRCS "${KERNEL_SRCS}" ${Pybind11_SRCS})
exclude(CORE_SRCS "${CORE_SRCS}" ${Pybind11_SRCS})

message(STATUS "Pybind11 Module CPP sources: ")
foreach(tmp ${Pybind11_SRCS})
  message(STATUS "  " ${tmp})
endforeach()

message(STATUS "Core CPP sources: ")
foreach(tmp ${CORE_SRCS})
  message(STATUS "  " ${tmp})
endforeach()

if(BUILD_CUDA_KERNEL)
  message(STATUS "KERNEL CUDA sources: ")
  foreach(tmp ${KERNEL_GPU_SRCS})
    message(STATUS "  " ${tmp})
  endforeach()
endif()

if(BUILD_OPENMP_KERNEL)
  message(STATUS "KERNEL OpenMP sources: ")
  foreach(tmp ${KERNEL_OpenMP_SRCS})
    message(STATUS "  " ${tmp})
  endforeach()
endif(BUILD_OPENMP_KERNEL)

message(STATUS "KERNEL CPP sources: ")
foreach(tmp ${KERNEL_SRCS})
  message(STATUS "  " ${tmp})
endforeach()

if(BUILD_CUDA_KERNEL)
  add_library(${PROJECT_NAME}_cuda STATIC ${KERNEL_GPU_SRCS})
  set_property(TARGET ${PROJECT_NAME}_cuda PROPERTY POSITION_INDEPENDENT_CODE ON)
  target_link_libraries(${PROJECT_NAME}_cuda
                        PUBLIC
                        Python::Python
                        ${TORCH_LIBRARIES}
                        ${TORCH_PYTHON_LIBRARY}
                        ${TORCH_CUDA_LIBRARIES}
                        ${CUDAToolkit_LIBRARIES})
endif()

if(BUILD_OPENMP_KERNEL)
  add_library(${PROJECT_NAME}_openmp STATIC ${KERNEL_OpenMP_SRCS})
  set_property(TARGET ${PROJECT_NAME}_openmp PROPERTY POSITION_INDEPENDENT_CODE ON)
  target_link_libraries(${PROJECT_NAME}_openmp
                        PUBLIC
                        Python::Python
                        ${TORCH_PYTHON_LIBRARY}
                        ${TORCH_LIBRARIES})
endif()

add_library(${PROJECT_NAME}_Lib STATIC ${CPP_SOURCES})
set_property(TARGET ${PROJECT_NAME}_Lib PROPERTY POSITION_INDEPENDENT_CODE ON)

target_link_libraries(${PROJECT_NAME}_Lib
                      PUBLIC
                      ${Python_LIBRARIES}
                      ${TORCH_PYTHON_LIBRARY}
                      ${TORCH_LIBRARIES}
                      ${TORCH_CUDA_LIBRARIES}
                      ${CUDAToolkit_LIBRARIES})

pybind11_add_module(${PROJECT_NAME} ${Pybind11_SRCS})

target_link_libraries(${PROJECT_NAME}
                      PUBLIC
                      ${PROJECT_NAME}_Lib
                      ${TORCH_PYTHON_LIBRARY}
                      ${Python_LIBRARIES}
                      ${TORCH_LIBRARIES}
                      ${TORCH_CUDA_LIBRARIES}
                      ${CUDAToolkit_LIBRARIES})

if(BUILD_CUDA_KERNEL)
  target_link_libraries(${PROJECT_NAME}
                        PUBLIC
                        ${PROJECT_NAME}_cuda)
  target_link_libraries(${PROJECT_NAME}_Lib
                        PUBLIC
                        ${PROJECT_NAME}_cuda)
endif()

if(BUILD_OPENMP_KERNEL)
  target_link_libraries(${PROJECT_NAME}
                        PUBLIC
                        ${PROJECT_NAME}_openmp)
  target_link_libraries(${PROJECT_NAME}_Lib
                        PUBLIC
                        ${PROJECT_NAME}_openmp)
endif()

target_include_directories(${PROJECT_NAME}
                           PUBLIC
                           ${CMAKE_CURRENT_LIST_DIR}/cc
                           ${KERNEL_INCLUDE_DIR}
                           ${CORE_INCLUDE_DIR}
                           ${KERNEL_GPU_INCLUDE_DIR}
                           ${KERNEL_OpenMP_INCLUDE_DIR})
                           
# VERSION_INFO is defined by setup.py and passed into the C++ code as a
# define (VERSION_INFO) here.
target_compile_definitions(${PROJECT_NAME}
                           PRIVATE VERSION_INFO=${VERSION_INFO})

# Generate *.pyi
if(BUILD_STUB_FILES)
execute_process(COMMAND ${Python_EXECUTABLE} -c "from importlib.metadata import version; print(version('pybind11-stubgen'))" OUTPUT_VARIABLE stubgen_version RESULT_VARIABLE pybind11_stubgen)
if(pybind11_stubgen AND NOT ${pybind11_stubgen} EQUAL 0)
    message(WARNING "pybind11-stubgen not found, if you want to create stub files
        for better autocompletion support install it with pip.")
else()
    if(stubgen_version LESS "1.0")
        message(WARNING "pybind11-stubgen version is too old, if you want to create stub files for better autocompletion support upgrade it with pip.")
    else()
    message("-- Found pybind11-stubgen version: ${stubgen_version}")
    add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
        COMMAND ${Python_EXECUTABLE} -m pybind11_stubgen -o ${CMAKE_CURRENT_LIST_DIR} ${PROJECT_NAME}
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        DEPENDS ${PROJECT_NAME})
    endif()
endif()
endif(BUILD_STUB_FILES)