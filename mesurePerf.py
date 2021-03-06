import pandas as pd
import numpy as np
np.seterr(all='print')

def getMonthCount(y1, m1, y2, m2):
    return (y2 - y1)*12 + m2 - m1


startMonth = 7

startYear = 1991
endMonth = 12
endYear = 2001
estLength = 6
holdLength = 12
nbStock = 10
positions = {}
trans_rate = 0.001
nbPositions = int((getMonthCount(startYear, startMonth, endYear, endMonth) + 1 - estLength) / holdLength)
print(nbPositions)

def incrMonth(year, month, nbMonth):
    tmpNbMonth = 0
    tmpMonth = month
    tmpYear = year
    while (tmpNbMonth < nbMonth):
        if tmpMonth == 12:
            tmpYear += 1
            tmpMonth = 1
        else:
            tmpMonth += 1
        tmpNbMonth += 1
    return [tmpMonth,tmpYear]

def decrMonth(year, month, nbMonth):
    tmpNbMonth = 0
    tmpMonth = month
    tmpYear = year
    while (tmpNbMonth < nbMonth):
        if tmpMonth == 1:
            tmpYear -= 1
            tmpMonth = 12
        else:
            tmpMonth -= 1
        tmpNbMonth += 1
    return [tmpMonth,tmpYear]

def isBetween(date, stt, end):
    return ((date[0] + date[1]*12) >= (stt[0] + stt[1]*12)) & ((date[0] + date[1]*12) < (end[0] + end[1]*12))


def computeReturns(data):
    returns = {}
    for index, row in data.iterrows():
        if row['stock_number'] in returns.keys():
            returns[int(row['stock_number'])].append(row['return_rf']-row['RiskFreeReturn'])
        else:
            returns[int(row['stock_number'])] = [(1 + row['return_rf'] - row['RiskFreeReturn'])**(1 / 12)]
    return returns

def computeTotalBeta(data):
    totalBeta = {}
    for index, row in data.iterrows():
        if row['stock_number'] in totalBeta.keys():
            totalBeta[int(row['stock_number'])] += row['betaHML']
        else:
            totalBeta[int(row['stock_number'])] = row['betaHML']
    return totalBeta



def computeTotalReturns(data):
    totalReturns = {}
    for index, row in data.iterrows():
        if row['stock_number'] in totalReturns.keys():
            totalReturns[int(row['stock_number'])] *= ((1 + row['return_rf']-row['RiskFreeReturn'])**(1/12))
        else:
            totalReturns[int(row['stock_number'])] = ((1 + row['return_rf']-row['RiskFreeReturn'])**(1/12))
    return totalReturns

def constructPortfoliosBeta(totalReturns):
    portfolios = {}
    sortTotRet = sorted(totalReturns, key=totalReturns.get)
    for index, value in enumerate(sortTotRet):
        if 'beta' in portfolios.keys():
            portfolios['beta']['stocks'].append(value)
        else:
            portfolios['beta'] = {'stocks': [value]}
    return portfolios

def constructPortfolios(totalReturns):
    portfolios = {}
    sortTotRet = sorted(totalReturns, key=totalReturns.get)
    for index, value in enumerate(sortTotRet):
        portName = int(index / nbStock) + 1
        if portName in portfolios.keys():
            portfolios[portName]['stocks'].append(value)
        else:
            portfolios[portName] = {'stocks': [value]}
    return portfolios

def computePortRent(totalReturns, portfolios):
    for pf_id in range(1,int(100/nbStock) + 1):
        portfolios[pf_id]['rent'] = 0
        for stock in portfolios[pf_id]['stocks']:
            portfolios[pf_id]['rent'] += ((totalReturns[stock] - 1) / nbStock)
    portfolios['Momentum'] = { 'rent' : portfolios[int(100/nbStock)]['rent'] - portfolios[1]['rent'] }
    return portfolios

def computePortRentBeta(totalReturns, portfolios):
    pf_id='beta'
    portfolios[pf_id]['rent'] = 0
    for stock in portfolios[pf_id]['stocks']:
       portfolios[pf_id]['rent'] += ((totalReturns[stock] - 1) / nbStock)
    return portfolios

def computeTransacCost():
    for i in range(nbPositions):
        for pf_name in range(1, int(100 / nbStock) + 1):
            if i == 0 :
                positions[0]['portfolios'][pf_name]['trans_cost'] = trans_rate
            else:
                oldPortfolio = positions[i-1]['portfolios'][pf_name]
                newPortfolio = positions[i]['portfolios'][pf_name]
                for oldStock in oldPortfolio['stocks'] :
                    if oldStock in newPortfolio['stocks'] :
                        newPortfolio['trans_cost'] = abs(positions[i-1]['holdTotalReturn'][oldStock]-(oldPortfolio['rent']+1))*trans_rate/nbStock
                    else:
                        newPortfolio['trans_cost'] = (positions[i-1]['holdTotalReturn'][oldStock] + (oldPortfolio['rent']+1))*trans_rate/nbStock
        #en supposant qu'un dans les 10 premiers ne sera pas dans les dix derniers l'année d'après et inversement!! vrai en general mais ici??
        positions[i]['portfolios']['Momentum']['trans_cost'] = positions[i]['portfolios'][1]['trans_cost'] + positions[i]['portfolios'][int(100 / nbStock)]['trans_cost']


def computeSharpeRatio():
    for i in range(nbPositions):
        pos = positions[i]
        for pf_name in range(1, int(100 / nbStock) + 1):
            pf = pos['portfolios'][pf_name]
            tmpReturns = np.zeros(holdLength)
            for stock in pf['stocks']:
                tmpReturns += np.array(pos['holdReturns'][stock])/nbStock
            pf['returns'] = tmpReturns
            pf['sharpeRatio'] = np.sqrt(12) * tmpReturns.mean() / tmpReturns.std()
        pos['portfolios']["Momentum"]['returns'] = pos['portfolios'][int(100/nbStock)]['returns'] - pos['portfolios'][1]['returns']
        tmpReturns = pos['portfolios']["Momentum"]['returns']
        pos['portfolios']["Momentum"]['sharpeRatio'] = np.sqrt(12) * tmpReturns.mean() / tmpReturns.std()





def computeTransacCostBeta():
    for i in range(nbPositions):
            pf_name='beta'
            if i == 0 :
                positions[0]['portfolios'][pf_name]['trans_cost'] = trans_rate
            else:
                oldPortfolio = positions[i-1]['portfolios'][pf_name]
                newPortfolio = positions[i]['portfolios'][pf_name]
                for oldStock in oldPortfolio['stocks'] :
                    if oldStock in newPortfolio['stocks'] :
                        newPortfolio['trans_cost'] = abs(positions[i-1]['holdTotalReturn'][oldStock]-(oldPortfolio['rent']+1))*trans_rate/nbStock
                    else:
                        newPortfolio['trans_cost'] = (positions[i-1]['holdTotalReturn'][oldStock] + (oldPortfolio['rent']+1))*trans_rate/nbStock


def computeSharpeRatioBeta():
    for i in range(nbPositions):
        pos = positions[i]
        pf_name='beta'
        pf = pos['portfolios'][pf_name]
        tmpReturns = np.zeros(holdLength)
        for stock in pf['stocks']:
            tmpReturns += np.array(pos['holdReturns'][stock])/nbStock
        pf['returns'] = tmpReturns
        pf['sharpeRatio'] = np.sqrt(12) * tmpReturns.mean() / tmpReturns.std()


def splitData(data):
    stPos = [startMonth, startYear]
    endPos = incrMonth(startYear, startMonth, estLength)
    for i in range(nbPositions):
        positions[i] = {}
        positions[i]['estData'] = data.loc[isBetween([data['month'],data['year']],stPos,endPos)]
        stPos = endPos
        endPos = incrMonth(endPos[1], endPos[0], holdLength)
        positions[i]['holdData'] = data.loc[isBetween([data['month'],data['year']],stPos,endPos)]
        positions[i]['estTotalReturn'] = computeTotalReturns(positions[i]['estData'])
        if(i==0):
            positions[i]['estBetaHML'] = computeTotalBeta(positions[i]['estData'])
        else:
            positions[i]['estBetaHML']= positions[i-1]['estBetaHML']
        positions[i]['holdTotalReturn'] = computeTotalReturns(positions[i]['holdData'])
        positions[i]['holdReturns'] = computeReturns(positions[i]['holdData'])
        positions[i]['portfolios'] = constructPortfolios(positions[i]['estTotalReturn'])
        positions[i]['portfolios'] = computePortRent(positions[i]['holdTotalReturn'], positions[i]['portfolios'])
        stPos = decrMonth(endPos[1], endPos[0], estLength)

    computeTransacCostBeta()
    computeSharpeRatioBeta()



def getCumulPfReturns(pf_name) :
    results = []
    tmpCumulReturn = 1
    for pos_id in sorted(positions.keys()):
        tmpCumulReturn *= (1 + positions[pos_id]['portfolios'][pf_name]['rent'])
        results.append((tmpCumulReturn - 1)*100)
    return results

def getPfReturns(pf_name) :
    results = []
    tmpCumulReturn = 1
    for pos_id in sorted(positions.keys()):
        results.append(positions[pos_id]['portfolios'][pf_name]['rent']*100)
    return results

def getCumulTransCost(pf_name) :
    results = []
    tmpCost = 0
    tmpPortPrice2 = 1
    tmpPortPrice = 1
    for pos_id in sorted(positions.keys()):
        tmpCost += positions[pos_id]['portfolios'][pf_name]['trans_cost']*tmpPortPrice2
        tmpPortPrice2 = tmpPortPrice
        tmpPortPrice *= (1+positions[pos_id]['portfolios'][pf_name]['rent'])
        results.append(tmpCost*100)
    return results

def getTransCost(pf_name) :
    results = []
    for pos_id in sorted(positions.keys()):
        results.append(positions[pos_id]['portfolios'][pf_name]['trans_cost']*100)
    return results

def getSharpeRatio(pf_name) :
    results = []
    for pos_id in sorted(positions.keys()):
        results.append(positions[pos_id]['portfolios'][pf_name]['sharpeRatio'])
    return results



exc = pd.ExcelFile("./cleanedData.xlsx")
df = exc.parse(0)
splitData(df)
print()
print()
# print("\\hline " +"beta"+" & ",end="")
# Res = getPfReturns("beta")
# for j in range(0,nbPositions):
#     print("{:.5f}".format(Res[j]) + "\% & ", end="")
# print("\\\\")
# exit()

print(getSharpeRatio("Momentum"))
print(getPfReturns("Momentum"))
print(getCumulTransCost("Momentum"))
print()
print()
print()
for i in range(1, 11):
    print("\\hline " + 'P'+ str(i)+" & ",end="")
    Res = getSharpeRatio(i)
    for j in range(0,nbPositions):
        print("{:.2f}".format(Res[j])+" & ", end="")
    print("\\\\")

print("\\hline " +"M"+" & ",end="")
Res = getSharpeRatio("Momentum")
for j in range(0,nbPositions):
    print("{:.2f}".format(Res[j]) + " & ", end="")
print("\\\\")


