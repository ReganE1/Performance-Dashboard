#%%
from common.common_module import *

#%%
def runDenodo_Composite_BB_Period():
    
    #missing inception date and market value

    Sql = "select distinct period_length from mondrian.i_cor_defensive_characteristics"

    data = run_sql("", "mondrian",command = Sql, database_type="Denodo")
    return data
period_list = runDenodo_Composite_BB_Period()

#%%
def runDenodo_Composite_Defensive_Characteristics_Month(composite_code,reporting_currency,valuation_date,period_length):
    

    Sql = "select period_length, bull_count_month, bear_count_month, total_months, composite_performance_bull_month, benchmark_performance_bull_month, composite_performance_bear_month, benchmark_performance_bear_month, composite_net_performance_bull_monthly, composite_net_performance_bear_monthly, relative_net_performance_bull_monthly, relative_net_performance_bear_monthly from mondrian.i_cor_defensive_characteristics where period_length = '" + period_length + "' and expressed_currency = '" + reporting_currency + "' and composite_code ='" + composite_code + "' and valuation_date ='" + valuation_date + "'"


    data = run_sql("", "mondrian",command = Sql, database_type="Denodo")
    output = data.drop(['period_length'], axis=1)
    df = output.rename(columns={'bull_count_month':'Bull Count', 'bear_count_month':'Bear Count', 'total_months': 'Total Months', 'composite_performance_bull_month': 'Composite Bull Performance', 'benchmark_performance_bull_month': 'Benchmark Bull Performance', 'composite_performance_bear_month':'Composite Bear Performance', 'benchmark_performance_bear_month':'Benchmark Bear Performance', 'composite_net_performance_bull_month': 'Composite Net Bull Performance', 'composite_net_performance_bear_month': 'Composite Net Bear Performance', 'relative_net_performance_bull_month': 'Relative Net Bull Performance', 'relative_net_performance_bear_month': 'Relative Net Bear Performance'})
    transposed = df.transpose()
    indexed =transposed.reset_index()
    renamed = indexed.rename(columns={'index':'Data_Point',0:'Data_Value'})
    #final = renamed.loc[renamed['Data_Point'].isin(['Bull Count','Bear Count', 'Total Months'])]
    return renamed

#%%
def runDenodo_Composite_Defensive_Characteristics_Quarter(composite_code,reporting_currency,valuation_date,period_length):
    

    Sql = "select period_length, bull_count_quarter, bear_count_quarter, total_quarters, composite_performance_bull_quarter, benchmark_performance_bull_quarter, composite_performance_bear_quarter, benchmark_performance_bear_quarter, composite_net_performance_bull_quarter, composite_net_performance_bear_quarter, relative_net_performance_bull_quarter, relative_net_performance_bear_quarter from mondrian.i_cor_defensive_characteristics where period_length = '" + period_length + "' and expressed_currency = '" + reporting_currency + "' and composite_code ='" + composite_code + "' and valuation_date ='" + valuation_date + "'"


    data = run_sql("", "mondrian",command = Sql, database_type="Denodo")
    output = data.drop(['period_length'], axis=1)
    df = output.rename(columns={'bull_count_quarter':'Bull Count', 'bear_count_quarter':'Bear Count', 'total_quarters': 'Total Quarters', 'composite_performance_bull_quarter': 'Composite Bull Performance', 'benchmark_performance_bull_quarter': 'Benchmark Bull Performance', 'composite_performance_bear_quarter':'Composite Bear Performance', 'benchmark_performance_bear_quarter':'Benchmark Bear Performance', 'composite_net_performance_bull_quarter': 'Composite Net Bull Performance', 'composite_net_performance_bear_quarter': 'Composite Net Bear Performance', 'relative_net_performance_bull_quarter': 'Relative Net Bull Performance', 'relative_net_performance_bear_quarter': 'Relative Net Bear Performance'})
    transposed = df.transpose()
    indexed =transposed.reset_index()
    renamed = indexed.rename(columns={'index':'Data_Point',0:'Data_Value'})
    #final = renamed.loc[renamed['Data_Point'].isin(['Bull Count','Bear Count', 'Total Quarters'])]
    return renamed

#output = runDenodo_Composite_Defensive_Characteristics_Quarter("INT_EQ","USD","2022-12-31","SINCE INCEPTION")
#Column = output['Data_Point'].values.tolist()
#Data = output['Data_Value'].values.tolist()


#%%
def runDenodo_Composite_Defensive_Characteristics_All(composite_code,reporting_currency,valuation_date, period_length):
    

    Sql = "select * from mondrian.i_cor_defensive_characteristics where expressed_currency = '" + reporting_currency + "' and composite_code ='" + composite_code + "' and valuation_date ='" + valuation_date + "'"


    data = run_sql("", "mondrian",command = Sql, database_type="Denodo").set_index('period_length')
    transposed = data.transpose()
    indexed =transposed.reset_index()
    out = indexed[['index',period_length]]
    output = out.rename(columns={'index':'data'})
    return output
#%%
#out = runDenodo_Composite_Defensive_Characteristics_Quarter("INT_EQ","USD","2022-12-31","SINCE INCEPTION")