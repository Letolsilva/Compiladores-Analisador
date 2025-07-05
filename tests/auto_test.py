import sys
import os
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import executar_codigo

def test_run(pas_file, input_file):
    try:
        with open(input_file, 'r') as input_data:
            input_content = input_data.read()
        
        process = subprocess.Popen(
            ['python3', 'main.py', pas_file], 
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        )
        if input_content:
            output, error = process.communicate(input=input_content.encode())
        else:
            output, error = process.communicate()

        if error:
            print(f"Erro durante a execução: {error.decode()}")

        return output.decode()
    except Exception as e:
        print(f"Erro durante o teste: {e}")

def run_test(pas_file, input_path, expected_output_path):
    output = test_run(pas_file,input_path)

    with open(expected_output_path, 'r') as expected_file:
        expected_output = expected_file.read()

    if output == expected_output:
        print("PASSED!")
    else:
        print("FAILED!")
        print("Expected:")
        print(expected_output)
        print("Got:")
        print(output)
    print()

def run_all_tests(program_path, input_dir, output_dir):
    for output_file in os.listdir(output_dir):
        if output_file.endswith('.out'):
            pas_file = os.path.join(program_path, output_file.replace('.out', '.pas'))
            input_file = os.path.join(input_dir, output_file.replace('.out', '.input'))
            expected_output_file = os.path.join(output_dir, output_file)
            print(f"Running test for {output_file}...")
            run_test(pas_file, input_file, expected_output_file)

run_all_tests('lista1', 'input/lista1', 'out/lista1')