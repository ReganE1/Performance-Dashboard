#%%
from common.common_module import *

#%%
def runDenodo_Portfolio_Detail(internal_account_id):
    
    #missing inception date and market value

    Sql = "select internal_account_id, portfolio_id, funding_date, primary_benchmark_reporting_name, primary_composite_name, reporting_currency from pd.i_pd_account where internal_account_id = '" + internal_account_id + "'"


    data = run_sql("", "mondrian",command = Sql, database_type="Denodo")
    output = data.rename(columns={'internal_account_id':'Account Code', 'portfolio_id':'Portfolio ID', 'funding_date':'Account Inception', 'primary_benchmark_reporting_name':'Primary Benchmark','primary_composite_name':'Primary Composite Name','reporting_currency':'Account Reporting Currency'})
    return output

#portfolio_detail_output = runDenodo_Portfolio_Detail()
