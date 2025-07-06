# Unit Test Generator for C++ Application Using AI Models

## Overview

This project implements a unit test generator tool for a C++ application using large language models (LLMs), specifically the Ollama CodeLlama 7B model. The tool automatically generates, refines, builds, and debugs unit tests for the provided C++ codebase.

## Assignment Summary

The assignment involved creating a workflow to:

- Generate initial unit tests for the C++ project using AI models and YAML prompt instructions.
- Refine the generated tests iteratively to remove duplicates, add relevant libraries, and improve test quality.
- Build the project with the generated tests and handle build issues by debugging and fixing tests using AI assistance.
- Calculate test coverage and improve tests based on coverage data (coverage generation attempted).
- Deliver a final test folder with well-formatted, non-duplicate unit tests and a report on test coverage.

## Project Structure

- `orgChartApi-master/`: The C++ application source code.
- `tests/`: Contains generated and refined unit test files.
- `prompts/`: YAML files with strict instructions for the LLM for each phase:
  - `phase1_refactor.yaml`: Test refinement instructions.
  - `phase2_generate_tests.yaml`: Initial test generation instructions.
  - `phase3_debug.yaml`: Debugging and fixing build issues.
- `scripts/`:
  - `run_pipeline.py`: Orchestrates the workflow of generating, refining, building, and debugging tests using the LLM.
  - `build_and_test.sh`: Builds the project and runs tests, collects coverage data.
- `models/ollama_api.py`: Interface to interact with the Ollama LLM.
- `CMakeLists.txt`: Build configuration using CMake and Google Test.
- `README.md`: This report file.

## Implementation Details

1. **Environment Setup**
   - Used Ollama CodeLlama 7B model running locally.
   - Installed Google Test framework and JSONCPP library for the C++ project.
   - Created a basic `tests/test_main.cpp` to enable test executable build.

2. **Test Generation**
   - The pipeline reads C++ source files in batches.
   - Sends combined source code with YAML prompt instructions to the LLM to generate initial unit tests.
   - Saves generated tests in the `tests/` directory.

3. **Test Refinement**
   - Each generated test file is sent back to the LLM with refinement instructions.
   - The LLM removes duplicates, adds necessary includes, and improves test quality.

4. **Build and Debug**
   - The project is built using CMake and tests are run.
   - If build fails, the build logs are sent to the LLM with debug instructions.
   - The LLM generates fixed test code which is saved and rebuilt.

5. **Coverage Reporting**
   - Coverage data collection was attempted using GNU coverage tools.
   - Coverage report generation failed due to missing coverage data files.
   - The main cause was the test executable failing to run due to a GLIBCXX runtime version mismatch.

## Current Status and Issues

- The test executable builds successfully after fixing missing dependencies and excluding conflicting source files.
- The test run fails due to a GLIBCXX version mismatch error caused by the runtime environment.
- Coverage data could not be collected because tests did not run successfully.
- Further environment configuration is needed to resolve the GLIBCXX runtime issue.

## Next Steps

- Resolve the GLIBCXX runtime version mismatch by updating the runtime environment or adjusting the build environment.
- Run the tests successfully and collect coverage data.
- Optionally, extend testing to cover all source files beyond the initial batches.
- Review and improve generated tests based on coverage and test results.

## Conclusion

This project demonstrates the use of AI models to automate unit test generation, refinement, and debugging for a C++ application. Despite runtime environment challenges, the pipeline successfully generates and builds tests, showcasing the potential of integrating LLMs into software testing workflows.


---

