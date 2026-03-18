import os
from fastapi import FastAPI
from sqlalchemy import text, create_engine

def generate_fastapi_code(params_signature: str, query: str, output_file: str):
    """
    Generates a FastAPI endpoint file with a working SQLAlchemy query.

    params_signature: str like "id: int, name: str"
    query: SQL query string with named parameters, e.g., "UPDATE users SET name = :name WHERE id = :id"
    output_file: path to write the generated .py file
    """
    # Generate Python code for the endpoint
    endpoint_code = f"""from fastapi import FastAPI
from sqlalchemy import text, create_engine

app = FastAPI()

# Engine will be patched in tests if needed
engine = create_engine("sqlite:///./test.db")

@app.get("/auto-endpoint")
def auto_endpoint({params_signature}):
    query = text(\"\"\"{query}\"\"\")
    # Build params dictionary from function arguments
    params = {{{', '.join([f'"{p.split(":")[0].strip()}": {p.split(":")[0].strip()}' for p in params_signature.split(",")])}}}
    with engine.connect() as conn:
        result = conn.execute(query, params)
        conn.commit()
        return [dict(row._mapping) for row in result]
"""

    # Make sure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write to file
    with open(output_file, "w") as f:
        f.write(endpoint_code)

    print(f"Generated FastAPI code in {output_file}")
