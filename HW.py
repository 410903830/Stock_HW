#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 01:25:50 2024

@author: zhangjunzhi

@Title: HW

"""

import pandas as pd 

df = pd.read_excel("kbars_2330_2022-07-01-2022-07-31.xlsx")
df.columns

df= df.drop("Unnamed: 0", axis=1)
df


df= df.set_index("time")
df


import mplfinance as mpf 

mpf.plot(df, volume= True, type= "candle", style= "charles")



#數據形態
def KbarType(Kbar):
    print(type(Kbar))
    return None

#將數據轉乘dataframe
def KbarToDataframe(Kbar):
    pd.DataFrame(Kbar)
    return ""

#將數據轉乘dict
def KbarToDict(Kbar):
    return ""

#移動平均MA
def MA(Kbar, Period):
    ma= Kbar['close'].rolling(window= Period).mean()
    #print(ma)
    return ma

#RSI(Reletive Strength Index)相對強弱指標
def RSI(Kbar, period):
    diff= Kbar['close'].diff()
    gain= (diff.where(diff>0, 0)).rolling(window= period).mean()
    print(gain)
    loss= (diff.where(diff<0, 0)).rolling(window= period).mean()
    print(loss)
    rs= gain/loss
    rsi= 100-(100/(1+rs))
    return rsi

#MACD
#DIF= EMA(close,12)- EMA(close, 26)
#DEM= EMA(Dif, 9)
#OSC= DIF-DEM= DIF-MACD


#指數移動平均數
def EMA(Kbar, period):
    ema= Kbar.ewm(span= period, adjust=False).mean()    
    return ema


def MACD(Kbar, period1, period2):
    
    
    Kbar= Kbar['close']
    EMA1= EMA(Kbar, period1)
    EMA2= EMA(Kbar, period2)
    DIF= EMA1-EMA2    
    #print(DIF)
    Kbar= DIF
    #print(Kbar)
    DEM= EMA(Kbar, 9)
    #print(DEM)      
    OSC= DIF- DEM
    #print(OSC)
    return DIF, DEM, OSC



df['close']

KbarType(df)
KbarToDict(df)
MA(df, 10)
RSI(df, 5)
MACD(df, 12, 26)





