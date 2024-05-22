# def test_create_service_order(client):
#     response = client.post(
#         "/api/v1/service_orders/",
#         json={
#             "description": "Test",
#             "date": "2024-05-21T00:00:00",
#             "cost": 100.0,
#             "vehicle_id": 1,
#         },
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["id"] is not None
#     assert data["description"] == "Test"


def test_get_service_orders(client):
    response = client.get("/api/v1/service_orders/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


# def test_get_service_order(client):
#     response = client.get("/api/v1/service_orders/1")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["id"] == 1


# def test_update_service_order(client):
#     response = client.put(
#         "/api/v1/service_orders/1",
#         json={
#             "description": "Updated",
#             "date": "2024-05-21T00:00:00",
#             "cost": 150.0,
#             "vehicle_id": None,
#         },
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["description"] == "Updated"


# def test_delete_service_order(client):
#     response = client.delete("/api/v1/service_orders/1")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["message"] == "Service order deleted successfully"

#     response = client.get("/api/v1/service_orders/1")
#     assert response.status_code == 404
