#%%
from common.common_module import *

#%%
def runDenodo_Portfolio_Detail(internal_account_id):
    
    #missing inception date and market value

    Sql = "select internal_account_id, funding_date, primary_benchmark_reporting_name, primary_composite_name from pd.i_pd_salesforce where internal_account_id = '" + internal_account_id + "'"


    data = run_sql("", "mondrian",command = Sql, database_type="Denodo")
    return data

#portfolio_detail_output = runDenodo_Portfolio_Detail()
