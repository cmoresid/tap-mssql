#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-mssql",
    version="0.0.1",
    description="Singer.io tap for extracting data from MS SQL Server",
    author="Connor Moreside",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_mssql"],
    install_requires=[
        "singer-python==5.1.1",
        "backoff==1.3.2",
        "pendulum==1.2.0",
        "pymssql==2.1.4"
    ],
    entry_points="""
    [console_scripts]
    tap-mssql=tap_mssql:main
    """,
    packages=["tap_mssql"],
    package_data = {
        "schemas": ["tap_mssql/schemas/*.json"]
    },
    include_package_data=True,
)
