
#%%
import pandas as pd
import pyodbc
from common.common_module import *
import panel as pn
pn.extension()



#%%

def f(x):
    return x * x

pn.interact(f, x=10)
