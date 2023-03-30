#%%
import pandas as pd
from common.common_module import *


def runSQLScript_ACTIVESHARE():
    
    Sql = "SELECT ActiveShare" + \
        " FROM Interface.performance.vwhs_cbk_PortfolioActiveShare" + \
        " WHERE PortiaID = " + "3784" + " AND ValuationDate = " + "'2022-12-31'"

    #run_sql("Interface",Sql)

    data = run_sql("DC1SQL01C", "Interface",command = Sql)
    return data
    #df = pd.DataFrame(data, columns=["ActiveShare"])
    #df.to_excel("ACTIVE SHARE.xlsx", index=False)

    #cursor.close()
    #conn.close()

active_share_output = runSQLScript_ACTIVESHARE()
# %%
