#%%
from common.common_module import *
composite_code = "INT_EQ"
valuation_date = "2023-02-28"
reporting_currency = "USD"

#%%
def runDenodo_Composite_Disclosure(composite_code,reporting_currency,valuation_date):
    
    Sql = "select * from mondrian.i_cor_composite_disclosure where composite_code = '" + composite_code + "' and valuation_date = '" + valuation_date + "' and expressed_currency = '" + reporting_currency + "'"

    data = run_sql("", "mondrian",command = Sql, database_type="Denodo")
    return data

#composite_disclosure = runDenodo_Composite_Disclosure()
