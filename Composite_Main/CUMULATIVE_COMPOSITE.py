#%%
from common.common_module import *

composite_code = "'INT_EQ'"
valuation_date = "'2023-02-28'"
reporting_currency = "'USD'"

#%%
def runDenodo_Cumulative_Composite_Performance():
    
    #missing inception date and market value

    Sql = "select * from mondrian.i_cor_composite_performance where period_length = 'MONTH' and expressed_currency_iso = " + reporting_currency + " and composite_code =" + composite_code + " and valuation_date =" + valuation_date


    data = run_sql("", "mondrian",command = Sql, database_type="Denodo")
    return data

cumulative_comp_perf_output = runDenodo_Cumulative_Composite_Performance()

