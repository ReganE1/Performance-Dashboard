#%%
import pandas as pd
import pyodbc
from common.common_module import *

#%%
def runDenodo_All_Portfolio():
    
    #missing inception date and market value

    Sql = "select * from mondrian.i_client_name"


    data = run_sql("", "mondrian",command = Sql, database_type="Denodo")
    return data

all_portfolio_output = runDenodo_All_Portfolio()
