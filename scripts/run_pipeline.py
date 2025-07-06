import os
import requests
import yaml
import subprocess

MODEL = "codellama:7b"
SRC_DIR = "orgChartApi-master"
TESTS_DIR = "tests"
PROMPTS = {
    "refactor": "prompts/phase1_refactor.yaml",
    "generate": "prompts/phase2_generate_tests.yaml",
    "debug": "prompts/phase3_debug.yaml"
}

def call_llm(src_code, prompt_path):
    with open(prompt_path, "r") as f:
        data = yaml.safe_load(f)

    prompt_text = data.get("instruction", "") + "\n\n" + src_code

    print(f"📡 Sending request to Ollama with prompt {prompt_path}...")
    res = requests.post("http://localhost:11434/api/generate", json={
        "model": MODEL,
        "prompt": prompt_text,
        "stream": False
    }, timeout=300)

    if res.status_code != 200:
        print("❌ Failed to get response from Ollama")
        print(res.text)
        exit(1)

    print("✅ Response received from Ollama")
    return res.json()["response"]

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

def get_cpp_files(src_dir):
    cpp_files = []
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".cc") or file.endswith(".cpp") or file.endswith(".h") or file.endswith(".hh"):
                cpp_files.append(os.path.join(root, file))
    return cpp_files

def build_and_test():
    print("🔨 Building and testing the project...")
    result = subprocess.run(["bash", "scripts/build_and_test.sh"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("❌ Build or tests failed")
        return False, result.stdout + result.stderr
    print("✅ Build and tests succeeded")
    return True, result.stdout

def main():
    cpp_files = get_cpp_files(SRC_DIR)
    print(f"Found {len(cpp_files)} C++ source files.")

    # Limit to first 3 files for testing to avoid timeout
    cpp_files = cpp_files[:3]

    # Batch source files content for initial test generation
    batch_size = 2
    for i in range(0, len(cpp_files), batch_size):
        batch_files = cpp_files[i:i+batch_size]
        combined_code = ""
        for f in batch_files:
            combined_code += f"// File: {f}\n"
            combined_code += read_file(f) + "\n\n"
        print(f"Generating tests for batch files: {', '.join(batch_files)}")
        test_code = call_llm(combined_code, PROMPTS["generate"])
        # Save combined test output to separate files by splitting on file markers
        # Assuming LLM outputs tests separated by file markers like "// Tests for file: filename"
        # If not, save all to one file named batch_{i}.cpp
        test_file_path = os.path.join(TESTS_DIR, f"batch_{i}_test.cpp")
        write_file(test_file_path, test_code)
        print(f"Tests written to {test_file_path}")

    # Refine tests iteratively (simplified: one pass)
    for test_file in os.listdir(TESTS_DIR):
        if test_file.endswith(".cpp"):
            test_path = os.path.join(TESTS_DIR, test_file)
            test_code = read_file(test_path)
            refined_code = call_llm(test_code, PROMPTS["refactor"])
            write_file(test_path, refined_code)
            print(f"Refined tests written to {test_path}")

    # Build and test
    success, output = build_and_test()

    # If build fails, debug and fix
    if not success:
        debug_code = call_llm(output, PROMPTS["debug"])
        # For simplicity, overwrite all tests with debug_code (could be improved)
        for test_file in os.listdir(TESTS_DIR):
            if test_file.endswith(".cpp"):
                test_path = os.path.join(TESTS_DIR, test_file)
                write_file(test_path, debug_code)
                print(f"Debugged tests written to {test_path}")

        # Rebuild after debug
        success, output = build_and_test()

    # Coverage improvements could be added here (not implemented)

    if success:
        print("🎉 All tests built and passed successfully.")
    else:
        print("⚠️ Build failed after debug attempts.")

if __name__ == "__main__":
    main()
