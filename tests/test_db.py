import yaml
import os
import psycopg2
import pytest

@pytest.fixture(scope='module')
def db_config():
    root_dir = os.path.dirname(os.path.dirname(__file__))
    db_yaml = os.path.join(root_dir, 'config', 'db_settings.yaml')
    with open(db_yaml, 'r') as file:
        DB_CONFIG = yaml.safe_load(file)['postgres']
    yield DB_CONFIG

@pytest.fixture(scope="module")
def db_connection(db_config):
    con = psycopg2.connect(**db_config)
    yield con
    con.close()

def test_connection(db_connection):
    assert db_connection is not None
    
def test_create_table(db_connection):
    cursor = db_connection.cursor()
    query = ''' 
    CREATE TABLE IF NOT EXISTS test_table (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        value INTEGER
        );
    '''
    cursor.execute(query)
    db_connection.commit()
    cursor.close()
    
    query = '''
    SELECT table_name
    FROM information_schema.tables
    WHERE table_name = 'test_table';
    '''
    cursor = db_connection.cursor()
    cursor.execute(query)
    res = cursor.fetchone()
    assert res is not None, "Table creation failed."
    cursor.close()

def test_insert_and_query(db_connection):
    """Test inserting data into the table and querying it."""
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO test_table (name, value) VALUES ('pytest_test', 123);")
    db_connection.commit()

    cursor.execute("SELECT name, value FROM test_table WHERE name = 'pytest_test';")
    result = cursor.fetchone()

    assert result == ('pytest_test', 123), "Insert or query failed."
    cursor.close()
    
@pytest.fixture(scope="module", autouse=True)
def clean_up(db_connection):
    yield
    cursor = db_connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS test_table;")
    db_connection.commit()
    cursor.close()
