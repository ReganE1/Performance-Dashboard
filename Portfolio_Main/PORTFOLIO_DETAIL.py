#%%
import pandas as pd
import pyodbc
from common.common_module import *

#%%
def test_db_connection_denodo():   
    conn = db_connection(db = 'mondrian', database_type = 'denodo')
    conn.execute('select * from mondrian.bv_ad_computer').fetchall()

#%%
def denodo_connect():
    denodo_driver = "DenodoODBC Unicode(x64)"
    denodo_server = "dc1den01c.mondrian.mipl.com"
    denodo_port = "9996"
    db = "Mondrian"
    password = "Password1"
    conn_string_dict = f"DRIVER={denodo_driver};SERVER={denodo_server};PORT={denodo_port};DATABASE={db};krbsrvname=HTTP;password={password};Integrated Security=true;"
    conn = conn_string_dict   
    con = pyodbc.connect(conn_string_dict, ansi=True,autocommit=True, encoding='ISO-8859-1')
    #con.setdecoding(pyodbc.SQL_CHAR,encoding='iso-8859-1')
    #con.setdecoding(pyodbc.SQL_WCHAR,encoding='iso-8859-1')
    #con.setencoding(encoding='iso-8859-1')
    command = 'select * from mondrian.i_cor_salesforce where portfolio_id = 3784'
    df = pd.read_sql(command, con)
    return df

output = denodo_connect()
#%%
def runDenodo_Portfolio_Detail():
    
    

    Sql = "Select * from mondrian.i_cor_salesforce where portfolio_id = 3784"


    data = run_sql("", "Mondrian",command = Sql, database_type="Denodo", )
    return data

output = runDenodo_Portfolio_Detail()
# %%
