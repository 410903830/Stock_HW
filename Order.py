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
def Order(OrderRecords,BS, OrderTime, OrderPrice, OrderQty):
    
    #Record = OrderRecord 當前物件資訊
    Record= OrderRecords
    #當前為平倉數量
       
    if BS=='Buy':
        for i in range(OrderQty):
             Record.OrderRecord.StockQty+=1
             StockQty= Record.OrderRecord.StockQty
             Record.OrderRecord.AllTradeRecord.append([1, "OrderBuy",OrderTime, OrderPrice])
             continue
    elif BS=='Sell':
         for i in range(OrderQty):
              Record.OrderRecord.StockQty-=1
              StockQty= Record.OrderRecord.StockQty
              Record.OrderRecord.AllTradeRecord.append([-1, "OrderSell",OrderTime, OrderPrice])
              continue
                
def Cover(OrderRecords,BS, OrderTime, OrderPrice, OrderQty):  
    #Record = OrderRecord 當前物件資訊
    Record= OrderRecords
    #當前為平倉數量
       
    if BS=='Buy':
        for i in range(OrderQty):
             Record.OrderRecord.StockQty+=1
             AllTradeStock= Record.OrderRecord.AllTradeRecord
             AllTradePrice= Record.OrderRecord.Profit
             StockQty= Record.OrderRecord.StockQty
             AllTradeStock.append([1, "Cover Buy",OrderTime, OrderPrice])
             profit= OrderPrice- AllTradeStock[-2][3]
             AllTradePrice.append(profit)
             profit_rate= profit/ AllTradeStock[-2][3]
             #print(profit)
             
             continue
    elif BS=='Sell':
         for i in range(OrderQty):
              Record.OrderRecord.StockQty-=1
              AllTradeStock= Record.OrderRecord.AllTradeRecord
              AllTradePrice= Record.OrderRecord.Profit
              StockQty= Record.OrderRecord.StockQty
              AllTradeStock.append([-1, "Cover Sell",OrderTime, OrderPrice])
              profit= OrderPrice- AllTradeStock[-2][3]
              AllTradePrice.append(profit)
              profit_rate= profit/ AllTradeStock[-2][3]
              #print(profit)
              continue
        
        
#############################################################################################################################################################################################################################################        
#RSI順勢回測方法    
        
        
        
#############################################################################################################################################################################################################################################        
#RSI逆勢回測方法    
        
        
        
#############################################################################################################################################################################################################################################
#呼叫Record 方法     
def gettotalprofit(Record):
    AllTradePrice= Record.OrderRecord.Profit
    print(sum(AllTradePrice))
def getAvgProfit(Record):
    AllTradePrice= Record.OrderRecord.Profit
    count= len(AllTradePrice)
    n= 0
    for i in AllTradePrice:
        if(i>0):
          n+=1;      
    Avg= n/count
    Avg = round(Avg * 100, 2)
    print("勝率: {:.2f}%".format(Avg))
def record(orderrecord):
    orderrecord.OrderRecord.StockQty+=1