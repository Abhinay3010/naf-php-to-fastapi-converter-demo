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
