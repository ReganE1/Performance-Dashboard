#%%
from common.common_module import *

#%%
def runDenodo_Portfolio_Characteristics(portfolio_id,valuation_date):
    

    Sql = "select * from pd.i_pd_account_characteristic_summary where account_id_invest_accounting = '" + portfolio_id + "' and end_date ='" + valuation_date + "'"

    data = run_sql("", "mondrian",command = Sql, database_type="Denodo")
    portfolio_output = data[['fund_pe','fund_yield','fund_pb','fund_pce','fund_market_cap','fund_median_market_cap','portfolio_security_count']]
    portfolio_output.loc[:,'Statistic'] ='Portfolio'
    portfolio_df = portfolio_output.rename(columns={'fund_pe':'Price to Earnings', 'fund_yield':'Dividend Yield','fund_pb':'Price to Book','fund_pce':'Price to Cash Flow', 'fund_market_cap': 'Weighted Average Market Cap (USD mil)', 'fund_median_market_cap': 'Median Market Cap (USD mil)', 'portfolio_security_count': 'Number of Securities'})
    index_output = data[['primary_benchmark_pe','primary_benchmark_dy','primary_benchmark_pb','primary_benchmark_pce','primary_benchmark_market_cap','primary_benchmark_median_market_cap','primary_benchmark_number_of_securities']]
    index_output.loc[:,'Statistic'] ='Index'
    index_df = index_output.rename(columns={'primary_benchmark_pe':'Price to Earnings', 'primary_benchmark_dy':'Dividend Yield','primary_benchmark_pb':'Price to Book','primary_benchmark_pce':'Price to Cash Flow', 'primary_benchmark_market_cap': 'Weighted Average Market Cap (USD mil)', 'primary_benchmark_median_market_cap': 'Median Market Cap (USD mil)', 'primary_benchmark_number_of_securities': 'Number of Securities'})
    df_combined = pd.concat([portfolio_df,index_df])
    transposed = df_combined.set_index('Statistic').T
    final = transposed.reset_index()
    return final
