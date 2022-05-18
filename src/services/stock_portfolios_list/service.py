# STANDARD LIBS
from datetime import datetime
from typing import List
import pytz

#INTERNAL LIBS
from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository


class StockPortfoliosList:
    mongo_stock_portfolios_repository_instance = MongoDbBaseRepository


