# This is a sample Python script.
import uvicorn

from etria_logger import GLADSHEIM_LOGGING_CONFIG

from api.routers.base_router import BaseRouter

app = BaseRouter.register_router_exchange()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=GLADSHEIM_LOGGING_CONFIG)
