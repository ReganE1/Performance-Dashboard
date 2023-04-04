#%%
from common.common_module import *

#%%
def runDenodo_All_Portfolio():
    
    Sql = "select * from pd.i_pd_client_name"


    data = run_sql("", "mondrian",command = Sql, database_type="Denodo")
    return data