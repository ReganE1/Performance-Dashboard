#%%
from common.common_module import *


#%%
def runDenodo_Composite_List():
    
    #missing inception date and market value

    Sql = "select composite_code, composite_name from mondrian.e_composite"


    data = run_sql("", "mondrian",command = Sql, database_type="Denodo")
    return data

composite_list = runDenodo_Composite_List()

