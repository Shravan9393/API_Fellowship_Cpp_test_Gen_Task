#!/bin/bash
mkdir -p build
cd build
cmake ..
make
ctest --output-on-failure
lcov --capture --directory . --output-file coverage.info
genhtml coverage.info --output-directory ../coverage/report
echo "✅ Coverage report generated at coverage/report/index.html"
