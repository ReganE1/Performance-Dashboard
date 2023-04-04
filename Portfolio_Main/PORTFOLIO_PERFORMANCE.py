#%%
from common.common_module import *
portfolio_id = 3774
#%%
def runDenodo_Portfolio_Performance(portfolio_id,reporting_currency,valuation_date):
    
    #missing quarters past the previous year. Needs new denodo view. 

    Sql = "select * from pd.i_pd_performance_by_type_company where valuation_date = period_end_date and account_id_invest_accounting = " + portfolio_id + " and valuation_date ='" + valuation_date + "'"

    data = run_sql("", "mondrian",command = Sql, database_type="Denodo")
    output = data.sort_values(by='sort_order', ascending=False)
    return output
