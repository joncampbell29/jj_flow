from .config import get_alpaca_keys
from datetime import datetime, timedelta
from alpaca.data import StockHistoricalDataClient, StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from ..utils.date_utils import check_date, safe_convert_date


def retrieve_historical_prices(
    stocks: list,
    start_date,
    end_date,
    alpaca_api_key=None,
    alpaca_secret_key=None,
    **kwargs
):
    pass
    # start_date = safe_convert_date(start_date)
    # end_date = safe_convert_date(end_date)
    
    # if not isinstance(stocks, list):
    #     raise ValueError("stocks must be a list of stock symbols")
    # if not all([isinstance(stock, str) for stock in stocks]):
    #     raise ValueError("stocks must be a list of stock symbols")
    
    # client = StockHistoricalDataClient(get_alpaca_keys())
    
    
    