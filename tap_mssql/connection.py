#!/usr/bin/env python3

import backoff
import _mssql

import singer
import ssl

LOGGER = singer.get_logger()

DEFAULT_PORT = 1433

@backoff.on_exception(backoff.expo,
                      (_mssql.MssqlDatabaseException),
                      max_tries=5,
                      factor=2)
def connect_with_backoff(connection):
    conn = connection()
    conn.execute_scalar("SELECT 1 + 1")

    return conn

def make_connection_wrapper(config):
    args = {
        "server": config["server"],
        "user": config["user"],
        "password": config["password"],
        "database": config["database"],
        "port": config.get("port", DEFAULT_PORT),
        "tds_version": "7.0",
        "charset": "utf8",
    }

    return connect_with_backoff(_mssql.connect(**args))
