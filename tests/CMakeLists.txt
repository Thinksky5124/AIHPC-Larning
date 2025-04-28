project(test_aihpc_C LANGUAGES CXX CUDA)

# Get all test files
include_directories(./common)
include_directories(./conf)

set(TEST_CPPS)

add_subdirectory(test_cases)

mark_as_advanced(
  BUILD_GMOCK BUILD_GTEST BUILD_SHARED_LIBS
  gmock_build_tests gtest_build_samples gtest_build_tests
  gtest_disable_pthreads gtest_force_shared_crt gtest_hide_internal_symbols
)

set_target_properties(gtest PROPERTIES FOLDER extern)
set_target_properties(gtest_main PROPERTIES FOLDER extern)
set_target_properties(gmock PROPERTIES FOLDER extern)
set_target_properties(gmock_main PROPERTIES FOLDER extern)

message(STATUS "TEST CPP sources: ")
foreach(tmp ${TEST_CPPS})
        message(STATUS "  " ${tmp})
endforeach()

## build test target
foreach (test_source ${TEST_CPPS})
  # Create a human readable name.
  get_filename_component(test_filename ${test_source} NAME)
  string(REPLACE ".cpp" "" mySTL_test_name ${test_filename})
  
  # Add the test target separately and as part of "make check-tests".
  add_executable(${mySTL_test_name} ${test_source})
  
  if(BUILD_CUDA_KERNEL)
    target_link_libraries(${mySTL_test_name}
                          _C_cuda
                          Python::Python
                          ${PYTHON_NVIDIA_LIBRARIES}
                          ${TORCH_LIBRARIES}
                          ${TORCH_PYTHON_LIBRARY}
                          ${TORCH_CUDA_LIBRARIES}
                          ${CUDAToolkit_LIBRARIES})
  endif()
  
  if(BUILD_OPENMP_KERNEL)
    target_link_libraries(${mySTL_test_name}
                          _C_openmp
                          Python::Python
                          ${TORCH_PYTHON_LIBRARY}
                          ${TORCH_LIBRARIES})
  endif()
  
  target_link_libraries(${mySTL_test_name}
                        _C_Lib
                        gmock
                        gtest
                        gtest_main
                        spdlog::spdlog_header_only
                        ${Python_LIBRARIES})
  
  gtest_discover_tests(${mySTL_test_name}
          EXTRA_ARGS
          --gtest_color=auto
          --gtest_output=xml:${CMAKE_BINARY_DIR}/test/${mySTL_test_name}.xml
          --gtest_catch_exceptions=0
          DISCOVERY_TIMEOUT 120
          PROPERTIES
          TIMEOUT 120
          )
  
  # Set test target properties and dependencies.
  set_target_properties(${mySTL_test_name}
          PROPERTIES
          RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/test"
          COMMAND ${mySTL_test_name})
endforeach ()
