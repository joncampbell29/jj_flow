import psycopg2
from psycopg2.pool import SimpleConnectionPool
from .config import get_db_config

class DatabaseManager:
    def __init__(self, db_config_yaml_path: str=None, db_config: dict=None):
        self.pool = None
        if db_config:
            self.db_config = db_config
        else:
            self.db_config = get_db_config(db_config_yaml_path)
        
    def initiate_pool(self, minconn=1, maxconn=10):
        if not self.pool:
            try:
                self.pool = psycopg2.pool.SimpleConnectionPool(minconn, maxconn, **self.db_config)
            except psycopg2.Error as e:
                RuntimeError(f"Could not initialize the connection pool: {e}")
        
    def connect_to_db(self):
        if not self.pool:
            raise RuntimeError("Connection pool is not initialized. Call initialize_pool() first.")
        try:
            conn = self.pool.getconn()
            return conn
        except psycopg2.Error as e:
            raise RuntimeError(f"Could not get a connection from pool: {e}")
    
    def release_connection(self, conn):
        if not self.pool:
            raise RuntimeError("Connection pool is not initialized.")
        if conn:
            self.pool.putconn(conn)
            
    def close_pool(self):
        if self.pool:
            self.pool.closeall()
            self.pool = None
    
    def test_connection(self):
        try:
            conn = self.connect_to_db()
            self.release_connection(conn)
            return True
        except Exception as e:
            return False
        
    def get_table_dim(self, conn, tablename):
        query = f'''
            SELECT 
            (SELECT COUNT(*) FROM {tablename}) AS row_count,
            (SELECT COUNT(column_name) 
            FROM information_schema.columns 
            WHERE table_name = '{tablename}') AS column_count;
        '''
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()
        return data
        
    def get_colnames(self, conn, tablename):
        query = f'''
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = '{tablename}';
        '''
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()
        return data
        
    def get_tables(self, conn):
        query = '''
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        '''
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()
        return data
    
    def get_table_structure(self, conn, tablename):
        query = f'''
            SELECT column_name, data_type, character_maximum_length
            FROM information_schema.columns
            WHERE table_name = '{tablename}';
        '''
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()
        return data
