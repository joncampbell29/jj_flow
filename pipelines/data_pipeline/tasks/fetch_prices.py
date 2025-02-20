from utils.env_utils import load_root_env
from database.config import get_db_config
from database.connection import DatabaseManager

load_root_env()
DB_CONFIG = get_db_config()

db_manager = DatabaseManager(DB_CONFIG)
db_manager.initiate_pool()
conn = db_manager.connect_to_db()
print(DB_CONFIG)
print(db_manager.get_tables(conn))
start_date = "2022-05-13"
end_date = "2022-05-13"

# query = f'''
#     SELECT symbol, COUNT(symbol) AS count
#     FROM {tablename}
#     WHERE symbol IN ({','.join([f"'{stock}'" for stock in stock_list])})
#     AND date >= '{start_date}'
#     AND date <= '{end_date}'
#     GROUP BY symbol;
#     '''
# with conn.cursor() as cur:
#     cur.execute(query)
#     data = cur.fetchall()

db_manager.release_connection(conn)
db_manager.close_pool()


