# This is a sample Python script.

# Standard Libs
import uvicorn

# Internal Libs
from etria_logger import GLADSHEIM_LOGGING_CONFIG
from api.routers.base_router import BaseRouter

app = BaseRouter.register_routers()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=GLADSHEIM_LOGGING_CONFIG)
