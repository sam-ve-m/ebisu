# This is a sample Python script.
import uvicorn

from fastapi import FastAPI

from api.routers.routers import router as client_orders


app = FastAPI()

app.include_router(client_orders)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port="9000",
        log_level="info"

    )