#!/usr/bin/env python3

import backoff
import _mssql

import singer
import ssl

LOGGER = singer.get_logger()

DEFAULT_PORT = 1433
DEFAULT_TDS_VERSION = "7.0"
DEFAULT_CHARSET = "utf8"

@backoff.on_exception(backoff.expo,
                      (_mssql.MSSQLDatabaseException),
                      max_tries=5,
                      factor=2)
def connect_with_backoff(connection, config):
    conn = connection(config)
    conn.execute_scalar("SELECT 1 + 1")

    return conn

class MSSQLConnection(_mssql.MSSQLConnection):
    def __init__(self, config):
        args = {
            "server": config["server"],
            "user": config["user"],
            "password": config["password"],
            "database": config["database"],
            "port": config.get("port", DEFAULT_PORT),
            "tds_version": config.get("tds_version", DEFAULT_TDS_VERSION),
            "charset": config.get("charset", DEFAULT_CHARSET),
        }

        super().__init__(**args)
    
    def __enter__(self):
        return self
    
    def __exit__(self, *exc_info):
        del exc_info
        self.close()

def make_connection_wrapper(config):
    return connect_with_backoff(MSSQLConnection, config)
