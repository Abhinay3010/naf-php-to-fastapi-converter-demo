import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from converter.parser import extract_sql_queries, extract_variables
from converter.transformer import normalize_query
from converter.generator import generate_fastapi_code


def process_file(file_path, output_dir):
    file_name = os.path.basename(file_path)
    print(f"\n📄 Processing: {file_name}")

    with open(file_path, "r") as f:
        php_code = f.read()

    queries = extract_sql_queries(php_code)
    variables = extract_variables(php_code)

    if not queries:
        print("⚠️ No SQL queries found. Skipping.")
        return

    for i, raw_query in enumerate(queries):
        print(f"\n🔍 Query {i+1}:")
        print(raw_query)

        normalized_query = normalize_query(raw_query)

        print("\n🔄 Normalized Query:")
        print(normalized_query)

        generated_code = generate_fastapi_code(normalized_query, variables)

        output_file = os.path.join(
            output_dir,
            f"{file_name.replace('.php','')}_query{i+1}.py"
        )

        with open(output_file, "w") as f:
            f.write(generated_code)

        print("\n🚀 Generated FastAPI Code:")
        print("=" * 60)
        print(generated_code)
        print("=" * 60)

        print(f"✅ Saved to: {output_file}")


def run_conversion():
    print("🚀 Starting bulk PHP → FastAPI conversion...")

    samples_dir = os.path.join(BASE_DIR, "samples")
    output_dir = os.path.join(BASE_DIR, "output")

    os.makedirs(output_dir, exist_ok=True)

    php_files = [f for f in os.listdir(samples_dir) if f.endswith(".php")]

    print(f"📁 Found {len(php_files)} PHP files")

    for file in php_files:
        process_file(os.path.join(samples_dir, file), output_dir)

    print("\n🎉 Conversion completed!")


if __name__ == "__main__":
    run_conversion()
