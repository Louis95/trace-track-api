import os
import sys

import uvicorn as uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from modules.routers import shipments
from modules.utilities.responses import base_responses

ENVIRONMENT = os.getenv("RUN_ENV", "local")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
API_TITLE = "Shipment API"

app = FastAPI(
    responses={**base_responses},
    title=API_TITLE,
    description="API Endpoint that exposes shipment and article information along with corresponding weather "
    "information.",
    docs_url=None,
    openapi_url="/api/v1/openapi.json",
    redoc_url="/docs",
    version="1.0",
)


app.include_router(shipments.router)

if __name__ == "__main__":
    load_dotenv()
    if "DATABASE_URL" in os.environ:
        # noinspection PyTypeChecker
        api_host = os.getenv(
            "API_HOST",
            "0.0.0.0",
        )  # noqa: S104 - binding to all interfaces on purpose
        api_port = int(os.getenv("API_PORT", "8000"))
        if ENVIRONMENT == "local":
            uvicorn.run(
                "main:app",
                host=api_host,
                port=api_port,
                reload=True,
            )
        else:
            uvicorn.run(app, host=api_host, port=api_port)
    else:
        sys.stderr.write(
            "Variable DATABASE_URL cannot be found in environment. Put it in .env or in "
            "the DATABASE_URL environment variable\n",
        )
