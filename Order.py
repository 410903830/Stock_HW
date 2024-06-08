#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 19:50:10 2024

@author: zhangjunzhi



指標交易回測方法


"""
import Record


#初始化
class OrderRecord():
    def __init__(self): ##建構子
        self.OrderRecord= Record.Record()


#############################################################################################################################################################################################################################################
#移動平均回測方法
def Order(OrderRecords,BS, OrderTime, OrderPrice, OrderQty, figpoint):
    
    #Record = OrderRecord 當前物件資訊
    Record= OrderRecords
    #當前為平倉數量
       
    if BS=='Buy':
        for i in range(OrderQty):
             Record.OrderRecord.StockQty+=1
             StockQty= Record.OrderRecord.StockQty
             Record.OrderRecord.AllTradeRecord.append([1, "OrderBuy",OrderTime, OrderPrice, figpoint])
             continue
    elif BS=='Sell':
         for i in range(OrderQty):
              Record.OrderRecord.StockQty-=1
              StockQty= Record.OrderRecord.StockQty
              Record.OrderRecord.AllTradeRecord.append([-1, "OrderSell",OrderTime, OrderPrice, figpoint])
              continue
                
def Cover(OrderRecords,CS, OrderTime, OrderPrice, OrderQty, figpoint):  
    #Record = OrderRecord 當前物件資訊
    Record= OrderRecords
    #當前為平倉數量
    Qty= Record.OrderRecord.StockQty
       
    if CS=='Buy':
        for i in range(OrderQty):
             Record.OrderRecord.StockQty+=1
             AllTradePrice= Record.OrderRecord.Profit
             StockQty= Record.OrderRecord.StockQty
             Record.OrderRecord.AllTradeRecord.append([1, "Cover Buy",OrderTime, OrderPrice, figpoint])

        profit= (OrderPrice- Record.OrderRecord.AllTradeRecord[-2][3])*Qty
        AllTradePrice.append(profit)
             

    elif CS=='Sell':
         for i in range(OrderQty):
              Record.OrderRecord.StockQty-=1
              AllTradePrice= Record.OrderRecord.Profit
              StockQty= Record.OrderRecord.StockQty
              Record.OrderRecord.AllTradeRecord.append([-1, "Cover Sell",OrderTime, OrderPrice, figpoint])
              
         profit= (OrderPrice- Record.OrderRecord.AllTradeRecord[-2][3])*Qty
         AllTradePrice.append(profit)
        
#############################################################################################################################################################################################################################################
#呼叫Record 方法     
def getprofit(Record):
    profit= Record.OrderRecord.Profit
    if len(Record.OrderRecord.Profit)>0:
        TotalProfit= [0]
        for i in Record.OrderRecord.Profit:
            TotalProfit.append(TotalProfit[-1]+i)
    return TotalProfit

def gettotalprofit(Record):
    AllTradePrice= Record.OrderRecord.Profit
    return sum(AllTradePrice)
    
def getAvgProfit(Record):
    AllTradePrice= Record.OrderRecord.Profit
    count= len(AllTradePrice)
    n= 0
    for i in AllTradePrice:
        if(i>0):
          n+=1;      
    Avg= n/count
    Avg= round(Avg * 100, 2)
    #print("勝率: {:.2f}%".format(Avg))
    
    return format(Avg)
    
    
def record(orderrecord):
    orderrecord.OrderRecord.StockQty+=1
    
    
    # 最大累計盈虧回落(MDD)
def GetMDD(Record):
    MDD,Capital,MaxCapital = 0,0,0
    for p in Record.OrderRecord.Profit:
        Capital += p  ## Capital = Capital+p
        MaxCapital = max(MaxCapital,Capital)
        DD = MaxCapital - Capital
        MDD = max(MDD,DD)
    return MDD


def getPprofit(Record):
    Profit= Record.OrderRecord.Profit
    Postive=0
    for i in Profit:
        if i >0:
            Postive+=i
    return Postive

def getNprofit(Record):
    Profit= Record.OrderRecord.Profit
    Nagative=0
    for i in Profit:
        if i <0:
            Nagative+=i
    return Nagative


    
    
    
    
    