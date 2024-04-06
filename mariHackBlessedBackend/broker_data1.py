import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
import json


data = pd.read_csv("chix.csv", sep = ";")

with open('bankHack.json', 'r') as file:
    data2 = json.load(file)


c = list(pd.unique(data["Contra Broker"].dropna()))
b = list(pd.unique(data["Broker"].dropna()))

for num in c:
    if num not in b:
        b.append(num)

brokers = []
for num in b:
    if num != np.nan and num != 1.0:
        brokers.append(int(num))


count_contrabro = {}

for bro_num in brokers:
    contrabro = data[data["Contra Broker"] == bro_num]
    count = len(contrabro)
    count_contrabro[bro_num] = count

orders = {}
notional = {}
for i in range(len(data2)):
    if data2[i]["Message Type"] != "X":
        notional[data2[i]["Broker"]] = 0
        orders[data2[i]["Order Reference"]] = {}
    if data2[i]["Message Type"] == "E":
        notional[data2[i]["Contra Broker"]] = 0
for i in range(len(data2)):
    if data2[i]['Message Type'] == 'A':
        orders[data2[i]['Order Reference']] = {
            "action" : data2[i]['Buy/Sell Indicator'],
            "Price": data2[i]['Price']
        }
    if data2[i]['Message Type'] == 'E':
        order = data2[i]['Order Reference']
        price = orders[order]["Price"]
        shares = data2[i]["Executed Shares"]

        notional[data2[i]["Broker"]] += price*shares
        notional[data2[i]["Contra Broker"]] += price*shares

del notional[1]


for i in range(len(data2)):
    data2[i]['Time Stamp'] = data2[i]['Time Stamp']['$numberLong'][:-6]

for i in range(len(data2)):
    data2[i]['Time Stamp'] = (int)(data2[i]['Time Stamp'])

y_brokers = [1, 2, 7, 9, 14, 19, 33, 39, 53, 65, 70, 72, 79, 80, 84, 85, 88, 124]
y_scores = {broker:[] for broker in y_brokers}
offers = {}


#sign = 1 is sell, -1 if buy
window_size = 1e5
def update_score(idx, y_broker,price, sign):
    nb_scores = []
    shares = data2[idx]['Executed Shares']
    trade_time = data2[idx]['Time Stamp']
    i = idx
    while i>=0 and (trade_time-data2[i]['Time Stamp'] < window_size):
        if data2[i]["Message Type"] == 'A':
            nb_scores.append(sign*(price-data2[i]['Price Decimal']))
        i-=1
    i = idx
    while i<len(data2) and (data2[i]['Time Stamp']-trade_time < window_size):
        if data2[i]["Message Type"] == 'A':
            nb_scores.append(sign*(price-data2[i]['Price Decimal']))
        i+=1
    y_scores[y_broker].append(np.mean(nb_scores)*shares)


for i in range(len(data2)):
    if data2[i]["Message Type"] == 'A':
        offer = data2[i]["Order Reference"]
        offers[offer] = {"action" : data2[i]['Buy/Sell Indicator'],"Price": data2[i]['Price Decimal']}
    if data2[i]["Message Type"] == 'E':
        offer = data2[i]["Order Reference"]
        price = offers[offer]["Price"]
        if offers[offer]["action"] == 'S':
            update_score(i, data2[i]['Broker'], price,  1)
            update_score(i, data2[i]['Contra Broker'], price, -1)
        else:
            update_score(i, data2[i]['Broker'], price, -1)
            update_score(i, data2[i]['Contra Broker'], price, 1)

scorePerTransaction = {}
for y_broker in y_scores:
    if len(y_scores[y_broker]) != 0:
        scorePerTransaction[y_broker] = np.mean(y_scores[y_broker])

    else:
        scorePerTransaction[y_broker] = 0

del scorePerTransaction[1]


exec = data[data["Message Type"] == "E"]
trade = {}

for bro_num in brokers:
    bro_exec = exec[exec["Broker"] == bro_num]
    count = len(bro_exec)
    trade[bro_num] = count

for key in trade:
    new_value = trade[key] + count_contrabro[key]
    trade[key] = new_value


volume = {}

for bro_num in brokers:
    bro_exec1 = exec[exec["Broker"] == bro_num]
    bro_exec2 = exec[exec["Contra Broker"] == bro_num]
    total = bro_exec1["Executed Shares"].sum() + bro_exec2["Executed Shares"].sum()
    volume[bro_num] = total


ratio = {}

for key in notional:
    try:
        r = notional[key] / trade[key]
        ratio[key] = r

    except ZeroDivisionError:
        ratio[key] = 0


criterias = [count_contrabro, notional, scorePerTransaction, trade, volume, ratio]

size = len(brokers)
initial_scores = [0.0] * size
scores = dict(zip(brokers, initial_scores))

for crit in criterias:
    crit_val = list(crit.values())
    mean = np.mean(crit_val)
    std = np.std(crit_val)

    for bk in crit:
        z = (crit[bk] - mean) * (size ** 0.5)/std
        scores[bk] += z

print(scores)