#%%
from common.common_module import run_sql, db_connection, create_db_engine
import pandas as pd
import pyodbc


def denodo(context):
    conn = db_connection(db='mondrian',server='',database_type = 'denodo')
    assert type(conn) == pyodbc.Connection

def interface(context):
    conn = db_connection(db='interface',server='',database_type = 'denodo')
    assert type(conn) == pyodbc.Connection