cmake_minimum_required(VERSION 3.10)
project(orgChartTests CXX)

enable_testing()
find_package(GTest REQUIRED)
find_package(jsoncpp REQUIRED)

add_executable(runTests tests/test_main.cpp)
target_include_directories(runTests PRIVATE orgChartApi-master ${JSONCPP_INCLUDE_DIRS})
target_link_libraries(runTests GTest::GTest GTest::Main pthread jsoncpp_lib)

add_test(NAME OrgChartTests COMMAND runTests)
