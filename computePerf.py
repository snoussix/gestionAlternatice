'''
    Format du Dictionaire { date : { id_stock_1 :  return_rf , id_stock_2 : return_rf } , ... }
'''
import pandas as pd

exc = pd.ExcelFile("./data_final_facteurs_fusionne_2.xlsx")
df = exc.parse(0)
