# This is a sample Python script.
from etria_logger import GLADSHEIM_LOGGING_CONFIG
import uvicorn
from api.routers.routers import app


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=GLADSHEIM_LOGGING_CONFIG)
