# Transportista Backend

Este proyecto es un backend para una empresa transportista, diseñado para administrar los procesos asociados al mantenimiento de sus vehículos. La aplicación está construida utilizando FastAPI y SQLAlchemy, y proporciona una API para registrar vehículos y gestionar órdenes de servicio de mantenimiento.

## Características

- **Registro de vehículos:** Permite registrar nuevos vehículos en el sistema.
- **Gestión de órdenes de servicio:** Permite crear y gestionar órdenes de servicio de mantenimiento para los vehículos registrados.

## Requisitos

- Python 3.10 o superior
- FastAPI
- Uvicorn
- SQLAlchemy
- Alembic
- Pydantic

## Estructura básica del proyecto

```sh
transportista_backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── vehicles.py
│   │   ├── service_orders.py
│   ├── presenters/
│   │   ├── __init__.py
│   │   ├── vehicle_presenter.py
│   │   ├── service_order_presenter.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── vehicle_view.py
│   │   ├── service_order_view.py
├── tests/
│   ├── test_integration.py
├── requirements.txt
```

## Instalación

1. Clona el repositorio:

    ```sh
    git clone https://github.com/tu_usuario/transportista_backend.git
    cd transportista_backend
    ```

2. Crea y activa un entorno virtual:

    ```sh
    python -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    ```

3. Instala las dependencias:

    ```sh
    pip install -r requirements.txt
    ```

4. Configura la base de datos:

    - Edita `database.py` para configurar la URL de tu base de datos.
    - Realiza las migraciones iniciales:

    ```sh
    alembic upgrade head
    ```

## Ejecución

Para ejecutar el servidor de desarrollo, usa el siguiente comando:

```sh
uvicorn app.main:app --reload
