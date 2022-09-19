# This is a sample Python script.

# Standard Libs
import uvicorn

# Internal Libs
from etria_logger import GLADSHEIM_LOGGING_CONFIG
from src.routers.base_router import BaseRouter

app = BaseRouter.register_routers()

from unittest.mock import patch
from persephone_client import Persephone, PersephoneClientStatus
with patch.object(Persephone, "send_to_persephone", return_value=(True, PersephoneClientStatus.success)):
    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000, log_config=GLADSHEIM_LOGGING_CONFIG)
