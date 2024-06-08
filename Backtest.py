#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 13:11:04 2024

@author: zhangjunzhi


回測Ｍethod 

"""
import pandas as pd
import Order
import streamlit as st




def BackMA(df):
    
        Record= Order.OrderRecord()
        StockQty= Record.OrderRecord.StockQty
        Order_Quantity= 1


        movesloss= 20    ###停損停利點
        for i in range(0, len(df.index)-1):
   
            StockQty= Record.OrderRecord.StockQty
    
            if StockQty==0:
                #進場
                ##多單進場
                if (df['MA1'][i-1] <= df['MA2'][i-1] and df['MA1'][i] > df['MA2'][i]) or (df['MA1'][i] > df['MA2'][i]):
                    Order.Order(Record, 'Buy', df.index[i+1], df['open'][i+1], Order_Quantity, df['open'][i+1])
                    orderprice= df['open'][i+1]
                    stop=  orderprice- 5   ##將moveloss 設成 5
                    continue
                ##空單進場
                if df['MA1'][i-1] >= df['MA2'][i-1] and df['MA1'][i] < df['MA2'][i]:
                    Order.Order(Record, 'Sell', df.index[i+1], df['open'][i+1], Order_Quantity, df['open'][i+1])
                    orderprice= df['open'][i+1]
                    stop= orderprice+ movesloss  
                    continue            
                #出場
                ##多單出場
            elif StockQty>0:
                
                if (df['close'][i]- movesloss <stop) or (df['MA1'][i-1] >= df['MA2'][i-1] and df['MA1'][i] < df['MA2'][i]) :
                    #停損停利出場
                    Order.Cover(Record, 'Sell', df.index[i+1], df['open'][i+1], Order_Quantity, df['open'][i+1])
                    continue
                elif df['close'][i]- movesloss >stop:
                    #繼續留
                    stop= df['close'][i]- movesloss
                    continue
    
            elif StockQty<0:    
                ##空單出場
                if (df['close'][i]- movesloss > stop) or (df['MA1'][i-1] <= df['MA2'][i-1] and df['MA1'][i] > df['MA2'][i]):
                    Order.Cover(Record, 'Buy', df.index[i+1], df['open'][i+1], Order_Quantity, df['open'][i+1])
                    #停損停利出場
                    continue    
                elif df['close'][i]+movesloss< stop:
                    #繼續留
                    stop= df['close'][i]+ movesloss
                    #停損停利出場
                    continue

        return Record
    
#順勢RSI  RSI(在maxline以下黃金交叉做多, 在minline以上死亡交叉做空)
def BackRsi1(df, maxline1, minline1):
    Order_Quantity= 1
    movesloss= 10    ###停損停利點
    Record= Order.OrderRecord()

    for i in range(0, len(df.index)-1):
        StockQty= Record.OrderRecord.StockQty
        if StockQty==0:    
            #進場Order
                ##多單進場(黃金交叉)
                if df['RSI1'][i-1]<=df['RSI2'][i-1] and df['RSI1'][i]> df['RSI2'][i-1] and df['RSI1'][i-1]>=maxline1:
                    Order.Order(Record, 'Buy', df.index[i+1], df['open'][i+1], Order_Quantity, df['RSI1'][i+1])
                    orderprice= df['open'][i+1]
                    stop= orderprice- movesloss
                    #order 
                    continue
                ##空單進場(死亡交叉)
                if df['RSI1'][i-1]>=df['RSI2'][i-1] and df['RSI1'][i]> df['RSI2'][i-1] and df['RSI1'][i-1]<=minline1:
                    Order.Order(Record, 'Sell', df.index[i+1], df['open'][i+1], Order_Quantity, df['RSI1'][i+1])
                    orderprice = df['open'][i+1]
                    stop= orderprice+ movesloss
                    #order 
                    continue
            #出場Cover 
                ##多單出場
        elif StockQty>0:
            if df['close'][i]-movesloss >stop:
                stop= df['close'][i]- movesloss
                continue
            elif df['close'][i]-movesloss< stop:
                ##cover 
                Order.Cover(Record, 'Sell', df.index[i+1], df['open'][i+1], Order_Quantity, df['RSI1'][i+1])
                continue    
                ##空單出場
        elif StockQty<0:
            if df['close'][i]+movesloss <stop:
                stop= df['close'][i]+ movesloss
                continue
            elif df['close'][i]+movesloss >stop:
                #cover
                Order.Cover(Record, 'Buy', df.index[i+1], df['open'][i+1], Order_Quantity, df['RSI1'][i+1])
                continue

    return Record


#逆勢RSI
def BackRsi2(df, minline2, maxline2):
    Record= Order.OrderRecord()
    Order_Quantity=1
    movesloss= 10
    for i in range(0, len(df.index)-1):
        StockQty= Record.OrderRecord.StockQty
        if StockQty==0:    
            #進場Order
                ##多單進場(黃金交叉)
                if df['RSI1'][i-1]<=minline2 and df['RSI1'][i]>minline2:
                    Order.Order(Record, 'Buy', df.index[i], df['open'][i], Order_Quantity, df['RSI1'][i])
                    orderprice= df['open'][i+1]
                    stop= orderprice- movesloss
                    #order 
                    continue
                ##空單進場(死亡交叉)
                if  df['RSI1'][i-1]>=maxline2 and df['RSI1'][i-1]<maxline2:
                    Order.Order(Record, 'Sell', df.index[i], df['open'][i], Order_Quantity, df['RSI1'][i])
                    orderprice = df['open'][i+1]
                    stop= orderprice+ movesloss
                    #order 
                    continue
            #出場Cover 
                ##多單出場
        elif StockQty==1:
            if (df['close'][i]-movesloss< stop):
                ##cover 
                Order.Cover(Record, 'Sell', df.index[i], df['open'][i], Order_Quantity, df['RSI1'][i])
                continue   
            elif df['close'][i]-movesloss >stop:
                stop= df['close'][i]- movesloss
                continue 
                ##空單出場
        elif StockQty==-1:
            if (df['close'][i]+movesloss) >stop :
                #cover
                Order.Cover(Record, 'Buy', df.index[i], df['open'][i], Order_Quantity, df['RSI1'][i])
                continue

            elif df['close'][i]+movesloss <stop:
                stop= df['close'][i]+ movesloss
                continue
    return(Record)




def BackRsi3(df, minline1):
    Record= Order.OrderRecord()
    Order_Quantity=1
    movesloss= 20
    for i in range(0, len(df.index)-1):
        StockQty= Record.OrderRecord.StockQty
        if StockQty==0:    
            #進場Order
                ##多單進場(黃金交叉)
                if (df['RSI1'][i-1]<=minline1 and df['RSI1'][i]>minline1) or (df['RSI1'][i-1]<df['RSI2'][i-1] and df['RSI1'][i]>df['RSI2'][i]):
                    Order.Order(Record, 'Buy', df.index[i], df['open'][i], Order_Quantity, df['RSI1'][i])
                    orderprice= df['open'][i+1]
                    stop= orderprice- movesloss
                    #order 
                    continue
                ##多單出場
        elif StockQty==1:
            if df['close'][i]-movesloss >stop:
                stop= df['close'][i]- movesloss
                continue
            elif df['close'][i]-movesloss< stop:
                ##cover 
                Order.Cover(Record, 'Sell', df.index[i], df['open'][i], Order_Quantity, df['RSI1'][i])
                continue    
                ##空單出場
        elif StockQty==-1:
            if df['close'][i]+movesloss <stop:
                stop= df['close'][i]+ movesloss
                continue
            elif df['close'][i]+movesloss >stop:
                #cover
                Order.Cover(Record, 'Buy', df.index[i], df['open'][i], Order_Quantity, df['RSI1'][i])
                continue
    return Record



def BackRsi4(df, maxline1):
    Record= Order.OrderRecord()
    Order_Quantity=1
    movesloss= 20
    for i in range(0, len(df.index)-1):
        StockQty= Record.OrderRecord.StockQty
        if StockQty==0:    
            #進場Order
                ##空單進場(死亡交叉)
                if  (df['RSI1'][i-1]>=maxline1 and df['RSI1'][i]<maxline1) or df['RSI1'][i-1]>80 and df['RSI1'][i]<80:
                    Order.Order(Record, 'Sell', df.index[i], df['open'][i], Order_Quantity, df['RSI1'][i])
                    orderprice = df['open'][i+1]
                    stop= orderprice+ movesloss
                    #order 
                    continue
            #出場Cover 
                ##多單出場
        elif StockQty==1:
            if df['close'][i]-movesloss >stop:
                stop= df['close'][i]- movesloss
                continue
            elif df['close'][i]-movesloss< stop:
                ##cover 
                Order.Cover(Record, 'Sell', df.index[i], df['open'][i], Order_Quantity, df['RSI1'][i])
                continue    
                ##空單出場
        elif StockQty==-1:
            if df['close'][i]+movesloss <stop:
                stop= df['close'][i]+ movesloss
                continue
            elif df['close'][i]+movesloss >stop:
                #cover
                Order.Cover(Record, 'Buy', df.index[i], df['open'][i], Order_Quantity, df['RSI1'][i])
                continue

    return Record


def BcakMACD(df, DIF,DEM):
    Record= Order.OrderRecord()
    Order_Quantity= 1
    movesloss= 20

    for i in range(0, len(df.index)-1):
        StockQty= Record.OrderRecord.StockQty
        if StockQty==0:    
            #進場Order
                ##多單進場(黃金交叉)
                if DEM[i-1]>=DIF[i-1] and DEM[i]<DIF[i]:
                    Order.Order(Record, 'Buy', df.index[i], df['open'][i], Order_Quantity, DIF[i])
                    orderprice= df['open'][i+1]
                    stop= orderprice- movesloss
                    #order 
                    continue
                ##空單進場(死亡交叉)
                if  DEM[i-1]<=DIF[i-1] and DEM[i]> DIF[i]:
                    Order.Order(Record, 'Sell', df.index[i], df['open'][i], Order_Quantity, DIF[i])
                    orderprice = df['open'][i+1]
                    stop= orderprice+ movesloss
                    #order 
                    continue
            #出場Cover 
                ##多單出場
        elif StockQty==1:
            if (df['close'][i]-movesloss< stop) or (DIF[i]<DEM[i]):
                ##cover 
                Order.Cover(Record, 'Sell', df.index[i], df['open'][i], Order_Quantity, DIF[i])
                continue   
            elif df['close'][i]-movesloss >stop:
                stop= df['close'][i]- movesloss
                continue 
                ##空單出場
        elif StockQty==-1:
            if (df['close'][i]+movesloss >stop) or (DIF[i]>DEM[i]):
                #cover
                Order.Cover(Record, 'Buy', df.index[i], df['open'][i], Order_Quantity, DIF[i])
                continue
            
            elif df['close'][i]+movesloss <stop:
                stop= df['close'][i]+ movesloss
                continue
            
    return Record





