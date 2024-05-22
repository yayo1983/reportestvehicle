
async def test_create_vehicle(client):
    response = await client.post(
        "/api/v1/vehicles/",
        json={"license_plate": "ABC123", "model": "Truck", "year": 2010, "current_mileage": 100000.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["license_plate"] == "ABC123"
    assert data["model"] == "Truck"
    assert data["year"] == 2010
    assert data["current_mileage"] == 100000.0
    assert "id" in data


async def test_get_vehicles(client):
    response = await client.get("/api/v1/vehicles/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["license_plate"] == "ABC123"

