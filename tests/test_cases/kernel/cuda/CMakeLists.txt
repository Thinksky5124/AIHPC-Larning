file(GLOB_RECURSE TEST_CPPS "./test_*.cpp")

foreach (test_source ${TEST_CPPS})
    # Create a human readable name.
    get_filename_component(test_filename ${test_source} NAME)
    string(REPLACE ".cpp" "" mySTL_test_name ${test_filename})

    # Add the test target separately and as part of "make check-tests".
    add_executable(${mySTL_test_name}  ${test_source})
    target_link_libraries(${mySTL_test_name} GTest::gtest_main)


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
            COMMAND ${mySTL_test_name}
            )
endforeach ()