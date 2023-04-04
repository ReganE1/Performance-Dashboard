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

    Sql = "select * from mondrian.i_cor_composite_performance where valuation_date = period_ending and period_length in ('MONTH','QUARTER','YTD', 'SINCE INCEPTION', 'SINCE INCEPTION ANNUALISED', '1 YEAR ROLLING', '3 YEAR ANNUALISED', '5 YEAR ANNUALISED', '7 YEAR ANNUALISED', '10 YEAR ANNUALISED') and expressed_currency_iso = '" + reporting_currency + "' and composite_code ='" + composite_code + "' and valuation_date ='" + valuation_date + "'"

    data = run_sql("", "mondrian",command = Sql, database_type="Denodo")
    output = data.sort_values(by='period_start', ascending=False)
    df = output.drop(['period_start'], axis=1)
    return df

#output = runDenodo_Composite_Performance(composite_code=composite_code, reporting_currency=reporting_currency, valuation_date=valuation_date)

#%%
def runDenodo_Composite_Performance_Extract(composite_code,reporting_currency,valuation_date):
    
    #missing quarters past the previous year. Needs new denodo view. 

    Sql = "select * from mondrian.i_cor_composite_performance where expressed_currency_iso = '" + reporting_currency + "' and composite_code ='" + composite_code + "' and valuation_date ='" + valuation_date + "'"

    data = run_sql("", "mondrian",command = Sql, database_type="Denodo")
    output = data.sort_values(by='period_start', ascending=False)
    return output

#output = runDenodo_Composite_Performance(composite_code=composite_code, reporting_currency=reporting_currency, valuation_date=valuation_date)