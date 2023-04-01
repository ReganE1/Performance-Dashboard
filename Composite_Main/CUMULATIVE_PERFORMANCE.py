#%%
from common.common_module import *

#%%
def runDenodo_Cumulative_Composite_Performance(composite_code,reporting_currency,valuation_date):
    
    #missing inception date and market value

    Sql = "select * from mondrian.i_cor_composite_performance where period_length = 'MONTH' and expressed_currency_iso = '" + reporting_currency + "' and composite_code ='" + composite_code + "' and valuation_date ='" + valuation_date + "'"


    data = run_sql("", "mondrian",command = Sql, database_type="Denodo")
    return data

#cumulative_comp_perf_output = runDenodo_Cumulative_Composite_Performance()


#%%
def runDenodo_Composite_Performance(composite_code,reporting_currency,valuation_date):
    
    #missing quarter

    Sql = "select period_length, period_start, composite_gross_performance, composite_net_performance, benchmark_performance, relative_performance from mondrian.i_cor_composite_performance where valuation_date = period_ending and period_length in ('MONTH','QUARTER','YTD', 'SINCE INCEPTION', 'SINCE INCEPTION ANNUALISED', '1 YEAR ROLLING', '3 YEAR ANNUALISED', '5 YEAR ANNUALISED', '7 YEAR ANNUALISED', '10 YEAR ANNUALISED') and expressed_currency_iso = '" + reporting_currency + "' and composite_code ='" + composite_code + "' and valuation_date ='" + valuation_date + "'"

    data = run_sql("", "mondrian",command = Sql, database_type="Denodo")
    output = data.sort_values(by='period_start', ascending=False)
    df = output.drop(['period_start'], axis=1)
    data_out = df.rename(columns={'period_length':'Period', 'composite_gross_performance':'Gross Perfomance', 'composite_net_performance':'Net Performance','benchmark_performance':'Index Performance','relative_performance':'Relative Performance'})
    return data_out

#output = runDenodo_Composite_Performance(composite_code=composite_code, reporting_currency=reporting_currency, valuation_date=valuation_date)