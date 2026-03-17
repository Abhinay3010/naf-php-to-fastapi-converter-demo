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

        queries = extract_sql_queries(php_code)
        variables = extract_variables(php_code)

        if not queries:
            print(f"No SQL found in {sample_file}")
            continue

        query = normalize_query(queries[0])
        code = generate_fastapi_code(query, variables)

        output_file = f"output/{sample_file.replace('.php','_query1.py')}"
        with open(output_file, "w") as f:
            f.write(code)

        print(f"✅ Converted {sample_file} → {output_file}")

if __name__ == "__main__":
    run_conversion()
