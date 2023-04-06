#%%
from common.common_module import *
#portfolio_id = 3774
rebased_cash = '0'
#%%
def runDenodo_Portfolio_Holdings(portfolio_id,valuation_date):
    

    Sql = "select * from pd.i_pd_top_holding where rebased_cash = '" + rebased_cash + "' and account_id_invest_accounting = '" + portfolio_id + "' and valuation_date ='" + valuation_date + "'"

    data = run_sql("", "mondrian",command = Sql, database_type="Denodo")
    return data
