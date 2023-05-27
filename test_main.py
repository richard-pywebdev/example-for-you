from fastapi.testclient import TestClient
from main import main_app

client = TestClient(main_app)


# Test health API
def test_get_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"health": "ok"}
