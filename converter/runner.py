import os
import sys

# ✅ Ensure project root is in Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from converter.parser import extract_sql_queries, extract_variables
from converter.transformer import normalize_query
from converter.generator import generate_fastapi_code


def run_conversion():
    print("🚀 Starting PHP → FastAPI conversion...")

    # ✅ Resolve file paths safely
    sample_path = os.path.join(BASE_DIR, "samples", "sample1.php")
    output_dir = os.path.join(BASE_DIR, "output")
    output_file = os.path.join(output_dir, "generated_api.py")

    # ✅ Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # ✅ Read PHP file
    try:
        with open(sample_path, "r") as f:
            php_code = f.read()
    except FileNotFoundError:
        print(f"❌ Sample file not found: {sample_path}")
        return

    print("📄 PHP file loaded")

    # ✅ Extract SQL + variables
    queries = extract_sql_queries(php_code)
    variables = extract_variables(php_code)

    print(f"🔍 Found {len(queries)} SQL query(ies)")
    print(f"🧩 Detected variables: {variables}")

    if not queries:
        print("⚠️ No SQL queries found. Exiting.")
        return

    # ✅ Normalize query
    query = normalize_query(queries[0])
    print(f"🔄 Normalized Query:\n{query}")

    # ✅ Generate FastAPI code
    code = generate_fastapi_code(query, variables)

    # ✅ Write output file
    with open(output_file, "w") as f:
        f.write(code)

    print("✅ Conversion complete!")
    print(f"📁 Output file: {output_file}")


if __name__ == "__main__":
    run_conversion()
