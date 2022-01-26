# This is a sample Python script.
import uvicorn

from api.routers.routers import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
