import pytest
from app.presenters.service_order_presenter import ServiceOrderPresenter
from app.schemas import ServiceOrderCreate, ServiceOrderUpdate
from sqlalchemy.exc import NoResultFound

def test_create_service_order(db):
    presenter = ServiceOrderPresenter(db)
    service_order_create = ServiceOrderCreate(description="Test", date="2024-05-21T00:00:00", cost=100.0, vehicle_id=None)
    service_order = presenter.create_service_order(service_order_create)
    assert service_order.id is not None
    assert service_order.description == "Test"

def test_get_service_order(db):
    presenter = ServiceOrderPresenter(db)
    service_order = presenter.get_service_order(1)
    assert service_order.id == 1

def test_update_service_order(db):
    presenter = ServiceOrderPresenter(db)
    service_order_update = ServiceOrderUpdate(description="Updated", date="2024-05-21T00:00:00", cost=150.0, vehicle_id=None)
    service_order = presenter.update_service_order(1, service_order_update)
    assert service_order.description == "Updated"

def test_delete_service_order(db):
    presenter = ServiceOrderPresenter(db)
    response = presenter.delete_service_order(1)
    assert response["message"] == "Service order deleted successfully"
    with pytest.raises(NoResultFound):
        presenter.get_service_order(1)
