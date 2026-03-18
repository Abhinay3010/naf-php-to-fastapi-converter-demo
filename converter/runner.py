from converter.parser import extract_sql_queries, extract_variables
from converter.transformer import normalize_query
from converter.generator import generate_fastapi_code
import os

def run_conversion():
    os.makedirs("output", exist_ok=True)
    sample_files = os.listdir("samples")
    
    for sample_file in sample_files:
        if not sample_file.endswith(".php"):
            continue
        with open(f"samples/{sample_file}", "r") as f:
            php_code = f.read()

        # Extract SQL queries and variables from PHP
        queries = extract_sql_queries(php_code)
        variables_list = extract_variables(php_code)

        if not queries:
            print(f"No SQL found in {sample_file}")
            continue

        query = normalize_query(queries[0])

        # Convert variables list to comma-separated string for generator
        params_signature = ", ".join(variables_list)

        # Determine output path
        output_file = f"output/{sample_file.replace('.php','_query1.py')}"

        # Generate FastAPI code
        generate_fastapi_code(params_signature, query, output_file)

        print(f"✅ Converted {sample_file} → {output_file}")

if __name__ == "__main__":
    run_conversion()
