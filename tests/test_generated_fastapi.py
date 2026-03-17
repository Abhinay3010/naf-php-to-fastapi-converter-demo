import os
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure repo root is in path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Collect all generated FastAPI files
generated_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".py")]

@pytest.mark.parametrize("file_name", generated_files)
def test_fastapi_file_import(file_name):
    """
    Test that the generated FastAPI file can be imported
    and has a valid 'app' object.
    """
    module_path = os.path.join(OUTPUT_DIR, file_name)
    module_name = file_name.replace(".py", "")
    
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Check app object exists
    assert hasattr(module, "app"), f"'app' not found in {file_name}"

    # Optional: test GET /auto-endpoint
    client = TestClient(module.app)
    response = client.get("/auto-endpoint")
    assert response.status_code == 200, f"{file_name} endpoint /auto-endpoint failed"
