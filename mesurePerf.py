import numpy as np
import pandas as pd
import datetime as dt


class Momentum:

    def __init__(self, nbStock):
        exc = pd.ExcelFile("./cleanedData.xlsx")
        self.data = exc.parse(0)
        self.stockPrices = {}
        for stock_nb in self.data.stock_number.unique():
            self.stockPrices[stock_nb] = 100
        self.lastYear = 2005
        self.lastMonth = 12
        self.nbStock = nbStock
        self.trans_cost = 0


    def isEnough(self, month, year, nbMonth):
        tmpYear = year
        tmpMonth = month
        if tmpMonth == 12:
            tmpYear += 1
            tmpMonth = 1
        else:
            tmpMonth += 1
        tmpNbMonth = 1
        while (tmpYear < self.lastYear or (tmpYear == self.lastYear and tmpMonth < self.lastMonth)):
            if (tmpNbMonth >= nbMonth) :
                return 'true'
            tmpNbMonth += 1;
            if tmpMonth == 12:
                tmpYear += 1
                tmpMonth = 1
            else:
                tmpMonth = 1
        return 'false'



    def incrMonth(self):
        if self.month == 12:
            self.year += 1
            self.month = 1
        else:
            self.month = 1

    def computeRenta(self, beginYear, beginMonth, endYear, endMonth):
        tmpMonth = 0
        while (tmpMonth < addMonth):
            tmpMonth+=1
            self.incrMonth()
            df = self.data.loc[(self.data['year']==self.year) & (self.data['month']>self.month)]
            for index, row in df.iterrows():
                self.stockPrices[row['stock_number']] *= (1 + row['return_rf'] + row['RiskFreeReturn'])

    def computeReturn(self, oldPrice):
        returns = {}
        for stock_nb in self.stockPrices:
            returns[stock_nb] = (self.stockPrices[stock_nb] - oldPrice[stock_nb])
        return returns

    def modifPfs(self):


    def execute(self,  estimMonth, holdMonth):
        while (self.year < 2006):
            oldPrice = self.stockPrices.copy()
            self.simulate(estimMonth)
            returns = self.computeReturn(oldPrice)
            '''Construction du portefeuille initiale'''
            sortRet = sorted(returns, key=returns.get)
            self.portfolios = {}
            for index, value in enumerate(sortRet):
                portId = int(index / self.nbStock) + 1
                if not portId in self.portfolios.keys():
                    self.portfolios[portId] = {'stocks' : [], 'price' : 100}
                self.portfolios[portId]['stocks'].append(value)
            print(self.portfolios)
            self.trans_cost = 0.2




mom = Momentum(10)
mom.execute(6,12)






def splitData()



#
# def computeTotalReturns(data):
#     totalReturns = {}
#     for index, row in data.iterrows():
#         if row['stock_number'] in totalReturns.keys():
#             totalReturns[int(row['stock_number'])] *= (1 + row['return_rf'] + row['RiskFreeReturn'])
#         else:
#             totalReturns[int(row['stock_number'])] = (1 + row['return_rf'] + row['RiskFreeReturn'])
#     return totalReturns
#
# def constructPortfolios(data, nbStock):
#     totalReturns = computeTotalReturns(data)
#     portfolios = {}
#     sortTotRet = sorted(totalReturns, key=totalReturns.get)
#     for index, value in enumerate(sortTotRet):
#         portName = (index % nbStock) + 1
#         if portName in portfolios.keys():
#             portfolios[portName]['stocks'].append({'stock_number' : value})
#         else:
#             portfolios[portName] = {'stocks': [{'stock_number' : value}]}
#     return portfolios
#
# def modifyPortfolio(data, nbStock):
#
#
# def computePortRent(data, portfolios, nbStock):
#     totalReturns = computeTotalReturns(data)
#     for name in portfolios:
#         portfolios[name]['rent'] = 0
#         for stock in portfolios[name]['stocks']:
#             portfolios[name]['rent'] += ((totalReturns[stock['stock_number']] - 1) / nbStock)
#             stock['rent'] = totalReturns[stock['stock_number']] - 1
#
#     portfolios['Momentum'] = { 'rent' : portfolios[int(100/nbStock)]['rent'] - portfolios[1]['rent'] }
#     return portfolios
#
# def execute(data, nbStock):
#     portRentas = {}
#     marketPortfolioPrices = {1995: '100'}
#     for year in range(1996,2006):
#         df = data.loc[(data['year']==year-1) & (data['month']>6)]
#         portfolios = constructPortfolios(df, nbStock)
#         df2 = data.loc[(data['year']==year)]
#         portfolios = computePortRent(df2, portfolios, nbStock)
#         for name in portfolios:
#             if name in portRentas.keys():
#                 portRentas[name][year] = int(portfolios[name]['rent'] * 10000) / 100
#             else:
#                 portRentas[name] = { year : int(portfolios[name]['rent'] * 10000) / 100 }
#
#     return portRentas
#
# exc = pd.ExcelFile("./cleanedData.xlsx")
# df = exc.parse(0)
# result = execute(df,10)
# print(result['Momentum'])
# for year in result['Momentum']:
#     print( result['Momentum'][year], ' \%' , end=' & ')
# print(' ')
# print(result)