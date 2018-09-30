import os
import _mssql
from tap_mssql.connection import MSSQLConnection, connect_with_backoff

DB_NAME = 'tap_mssql_test'

def get_db_config():
    config = {}
    config['server'] = os.environ.get('TAP_MSSQL_SERVER')
    config['port'] = os.environ.get('TAP_MSSQL_PORT')
    config['user'] = os.environ.get('TAP_MSSQL_USER')
    config['password'] = os.environ.get('TAP_MSSQL_PASSWORD')

    if not config['password']:
        del config['password']

    return config

def get_test_connection():
    db_config = get_db_config()

    connection = _mssql.connect(**db_config)

    try:
        connection.execute_non_query('DROP DATABASE {}'.format(DB_NAME))
    except:
        pass

    try:
        connection.execute_non_query('CREATE DATABASE {}'.format(DB_NAME))
    except:
        pass
    finally:
        connection.close()

    db_config['database'] = DB_NAME

    return connect_with_backoff(MSSQLConnection, db_config)
