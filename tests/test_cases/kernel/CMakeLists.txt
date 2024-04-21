if(BUILD_CUDA_KERNEL)
    add_subdirectory(cuda)
endif()

if(BUILD_OPENMP_KERNEL)
    add_subdirectory(openmp)
endif()

set(TEST_CPPS ${TEST_CPPS} PARENT_SCOPE)