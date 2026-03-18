import os
from fastapi import FastAPI
from sqlalchemy import text, create_engine

def generate_fastapi_code(params_signature, query: str, output_file: str):
    """
    Generates a FastAPI endpoint file with a working SQLAlchemy query.

    params_signature: list of parameter names OR string like "id: int, name: str"
    query: SQL query string with named parameters, e.g., "UPDATE users SET name = :name WHERE id = :id"
    output_file: path to write the generated .py file
    """

    # If params_signature is a string, convert to list of names
    if isinstance(params_signature, str):
        param_names = [p.split(":")[0].strip() for p in params_signature.split(",")]
    elif isinstance(params_signature, list):
        param_names = [p.strip() for p in params_signature]
    else:
        raise ValueError("params_signature must be a string or list of parameter names")

    # Build params dictionary from function arguments
    params_dict_code = ", ".join([f'"{name}": {name}' for name in param_names])

    # Reconstruct params_signature for function definition
    if isinstance(params_signature, list):
        params_signature_code = ", ".join([f"{name}: str" for name in param_names])  # default type str
    else:
        params_signature_code = params_signature

    # Generate Python code for the endpoint
    endpoint_code = f"""from fastapi import FastAPI
from sqlalchemy import text, create_engine

app = FastAPI()

# Engine will be patched in tests if needed
engine = create_engine("sqlite:///./test.db")

@app.get("/auto-endpoint")
def auto_endpoint({params_signature_code}):
    query = text(\"\"\"{query}\"\"\")
    params = {{{params_dict_code}}}
    with engine.connect() as conn:
        result = conn.execute(query, params)
        conn.commit()
        return [dict(row._mapping) for row in result]
"""

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write to file
    with open(output_file, "w") as f:
        f.write(endpoint_code)

    print(f"Generated FastAPI code in {output_file}")
