import psycopg2
from .connection import DatabaseManager

def check_stocks_table(
    conn,
    stock_list,
    start_date,
    end_date,
    tablename='daily_prices'
):
    # query = f'''
    #     SELECT symbol, COUNT(symbol) AS count
    #     FROM {tablename}
    #     WHERE symbol IN ({','.join([f"'{stock}'" for stock in stock_list])})
    #     AND date >= '{start_date}'
    #     AND date <= '{end_date}'
    #     GROUP BY symbol;
    # '''
    # with conn.cursor() as cur:
    #     cur.execute(query)
    #     data = cur.fetchall()
    # return data
    pass