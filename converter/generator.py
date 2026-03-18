import os

def generate_fastapi_code(variables: list[str], query: str, output_file: str):
    """
    Generates a FastAPI endpoint file with SQLAlchemy query.
    variables: list of parameter names, e.g., ['id', 'name']
    query: SQL query string with named parameters (:id, :name)
    output_file: path to write the generated Python file
    """
    # Build parameter signature for FastAPI function
    params_signature = ", ".join([f"{v}: str" for v in variables]) if variables else ""

    # Build params dictionary from variables
    params_dict = ", ".join([f'"{v}": {v}' for v in variables]) if variables else ""

    endpoint_code = f"""from fastapi import FastAPI
from sqlalchemy import text, create_engine

app = FastAPI()

# Engine will be patched in tests if needed
engine = create_engine("sqlite:///./test.db")

@app.get("/auto-endpoint")
def auto_endpoint({params_signature}):
    query = text(\"\"\"{query}\"\"\")
    params = {{{params_dict}}}
    with engine.connect() as conn:
        result = conn.execute(query, params or {{}})
        conn.commit()
        return [dict(row._mapping) for row in result]
"""

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        f.write(endpoint_code)

    print(f"Generated FastAPI code in {output_file}")
