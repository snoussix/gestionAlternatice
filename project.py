import numpy as np
import pandas as pd

from time import time
from operator import itemgetter

from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import RandomForestClassifier


exc = pd.ExcelFile("./data_final_facteurs_fusionne_2.xlsx")
df = exc.parse(0)
df = df.convert_objects(convert_numeric=True)

del df['pin']
del df['fsrv']

df1 = df.loc[df['stock_number'] != 292]
df1 = df1.loc[df['stock_number'] != 280]
df1 = df1.loc[df['stock_number'] != 308]


'''
On peut aussi virer ce qui est en dessous de 1989 par exemple
'''
l = []
for i in range(1,1088) :
    if (len(df1.loc[df1.stock_number == i])> 190) :
        l.append(i)

data = df1.loc[df['stock_number'].isin(l)]
df2 = data.loc[(data['stock_number'] != data['stock_number'].shift(-1)) & (data['year'] == 2005)]
data = df1.loc[df['stock_number'].isin(df2.stock_number)]
data = data.loc[data['stock_number'] != 1]
data = data.loc[data['year'] > 1990]

df2 = data
# df2 = df2.loc[~df2['illiq_amihud'].apply(np.isnan)]
# df2 = df2.loc[~df2['return_rf'].apply(np.isnan)]
# df2 = df2.loc[~df2['AIM_t1'].apply(np.isnan)]
# df2 = df2.loc[~df2['AIM'].apply(np.isnan)]
# df2 = df2.loc[~df2['RiskFreeReturn'].apply(np.isnan)]

l = []

for i in list(set(df2['stock_number'])) :
    if (len(df2.loc[df2.stock_number == i])> 179) :
        l.append(i)

df2 = df2.loc[df2['stock_number'].isin(l)]
#      517,520,524,532,1057,547,,559,117,82,511,497,357
tmp = [517,520,524,532,1057,547,559,117,82,511,497]
df2 = df2.loc[~df2['stock_number'].isin(tmp)]

cleanDf = df2[['stock_number','year','month','return_rf','RiskFreeReturn','betaHML']]

cleaner=['return_rf','RiskFreeReturn','betaHML']

cleanDf.is_copy = False
#cleanDf['return_rf'][804]=5.555
#cleanDf['return_rf'][805]=5.555
for name in cleaner:
    # we don't use list comprehension to preserve mean
    mean2=0.0
    prec1=0.0
    prec2=0.0
    for index,x in enumerate(cleanDf[name]) :
        mean2=(prec1+prec2)/2.0
        prec2=prec1
        if np.isnan(x):
            cleanDf[name][802+index] = mean2
            prec1=mean2
        else:
            prec1= x
#cleanDf['return_rf'][806]=5.555
writer = pd.ExcelWriter("./cleanedData.xlsx")
cleanDf.to_excel(writer, 'Sheet1')
writer.save()