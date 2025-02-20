import psycopg2
from psycopg2.pool import SimpleConnectionPool

class DatabaseManager:
    """
    A class to manage database connections and operations using a connection pool.

    Simplifies interactions with a PostgreSQL database by providing
    methods to initialize a connection pool, connect to the database, and perform
    common database operations such as querying table dimensions, column names, 
    and table structures.

    Attributes
    ----------
    db_config : dict
        The configuration parameters for the database connection.
    pool : psycopg2.pool.SimpleConnectionPool
        The connection pool used to manage database connections.

    Methods
    -------
    initiate_pool(minconn=1, maxconn=10)
        Initializes a connection pool with the given minimum and maximum connections.
    
    connect_to_db()
        Retrieves a database connection from the connection pool.
    
    release_connection(conn)
        Releases a database connection back to the connection pool.
    
    close_pool()
        Closes all connections in the connection pool.
    
    test_connection()
        Tests if a connection to the database can be established.
    
    get_table_dim(conn, tablename)
        Retrieves the number of rows and columns in a table.
    
    get_colnames(conn, tablename)
        Retrieves the column names of a specified table.
    
    get_tables(conn)
        Retrieves a list of all tables in the public schema of the database.
    
    get_table_structure(conn, tablename)
        Retrieves the structure of a specified table, including column names, 
        data types, and maximum character lengths.
    """
    
    def __init__(self, db_config: dict):
        self.pool = None
        self.db_config = db_config
        
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
