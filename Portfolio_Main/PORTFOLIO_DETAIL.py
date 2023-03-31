#%%
import pandas as pd
import pyodbc
from common.common_module import *

#%%
def runDenodo_Portfolio_Detail():
    
    #missing inception date and market value

    Sql = "select internal_account_id, funding_date, primary_benchmark_reporting_name, primary_composite_name from mondrian.i_cor_salesforce where portfolio_id = 3784"


    data = run_sql("", "mondrian",command = Sql, database_type="Denodo")
    return data

portfolio_detail_output = runDenodo_Portfolio_Detail()
