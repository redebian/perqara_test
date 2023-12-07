from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_item():
    item_data = {"item_name": "TestItem", "price": 1500}
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    assert response.json()["item_name"] == item_data["item_name"]
    assert response.json()["price"] == item_data["price"]


def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_read_item():
    item_data = {"item_name": "TestItem", "price": 1500}
    create_response = client.post("/items/", json=item_data)
    created_item = create_response.json()

    item_id = created_item["id"]
    response = client.get(f"/items/{item_id}")

    assert response.status_code == 200
    assert response.json()["item_name"] == created_item["item_name"]
    assert response.json()["price"] == created_item["price"]


def test_update_item():
    item_data = {"item_name": "TestItem", "price": 1500}
    create_response = client.post("/items/", json=item_data)
    created_item = create_response.json()

    updated_data = {"item_name": "UpdatedItem", "price": 2000}
    response = client.put(f"/items/{created_item['id']}", json=updated_data)

    assert response.status_code == 200
    assert response.json()["item_name"] == updated_data["item_name"]
    assert response.json()["price"] == updated_data["price"]


def test_delete_item():
    item_data = {"item_name": "TestItem", "price": 1500}
    create_response = client.post("/items/", json=item_data)
    created_item = create_response.json()

    response = client.delete(f"/items/{created_item['id']}")

    assert response.status_code == 200
    assert response.json()["item_name"] == created_item["item_name"]


def test_item_not_found():
    response = client.get(f"/items/100")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

