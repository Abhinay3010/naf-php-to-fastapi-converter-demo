from converter.parser import extract_sql_queries, extract_variables
from converter.transformer import normalize_query
from converter.generator import generate_fastapi_code

def run_conversion():
    with open("samples/sample1.php", "r") as f:
        php_code = f.read()

    queries = extract_sql_queries(php_code)
    variables = extract_variables(php_code)

    if not queries:
        print("No SQL found")
        return

    query = normalize_query(queries[0])
    code = generate_fastapi_code(query, variables)

    with open("output/generated_api.py", "w") as f:
        f.write(code)

    print("✅ Conversion complete. Check output/generated_api.py")

if __name__ == "__main__":
    run_conversion()
