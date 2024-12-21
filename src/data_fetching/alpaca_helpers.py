from .config import get_alpaca_keys
from datetime import datetime, timedelta
from alpaca.data import StockHistoricalDataClient, StockBarsRequest
from alpaca.data.timeframe import TimeFrame


def retrieve_historical_prices(
    stocks: list,
    start_date,
    end_date,
):
    pass