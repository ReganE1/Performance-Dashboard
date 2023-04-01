#%%
from common.common_module import *

#composite_code = "INT_EQ"

#%%
def runDenodo_Composite_Details(composite_code):
    
    #missing inception date and market value

    Sql = "select composite_name, composite_currency, initial_date, benchmark_name from mondrian.e_composite where composite_code = '" + composite_code + "'"


    data = run_sql("", "mondrian",command = Sql, database_type="Denodo")
    output = data.rename(columns={'composite_name':'Composite Name', 'composite_currency':'Composite Currency', 'initial_date':'Inception Date','benchmark_name':'Index Name'})
    #data_out = data.set_index('composite_name')['composite_currency','initial_date','benchmark_name'].to_dict()
    #data_out = data.to_dict('records')
    #output = data.transpose()
    #data_out = output.rename(columns = {:'Composite Label}{0:'Composite Details'})
    return output
