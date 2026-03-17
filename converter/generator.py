def generate_fastapi_code(query: str, params: list):
    params_signature = ", ".join([f"{p}: str" for p in params])
    params_dict = ", ".join([f'"{p}": {p}' for p in params])

    return f'''
from fastapi import FastAPI
from sqlalchemy import text, create_engine

app = FastAPI()

engine = create_engine("sqlite:///./test.db")

@app.get("/auto-endpoint")
def auto_endpoint({params_signature}):
    query = text("{query}")
    with engine.connect() as conn:
        result = conn.execute(query, {{{params_dict}}})
        return [dict(row._mapping) for row in result]
'''
