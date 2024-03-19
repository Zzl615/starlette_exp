

from fastapi import FastAPI
from webapp.middleware.api_record import ApiRecordMiddleware

APP_NAME = "explore-fastapi"

SERVICE_DESCRIPTION = "Explore FastAPI with a simple web service."

def create_app() -> FastAPI:
    app = FastAPI(
        title=APP_NAME,
        description=SERVICE_DESCRIPTION,
        version="0.0.1",
        generate_unique_id_function=lambda route: f"{route.name}",
        openapi_url=f"/{APP_NAME}/open-api-json",
        docs_url=f"/{APP_NAME}/swagger",
        redoc_url=f"/{APP_NAME}/redoc",
    )
    app.add_middleware(ApiRecordMiddleware)
    return app