#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 01:25:50 2024

@author: zhangjunzhi

@Title: 技術分析方法

"""

import pandas as pd 
import talib


#數據形態
def KbarType(df):
    print(type(df))
    return None

#將數據轉乘dataframe
def KbarToDataframe(df):
    pd.DataFrame(df)
    return ""

#將數據轉乘dict
def KbarToDict(df):
    return ""

#移動平均MA
def MA(df, Period):
    ma= df['close'].rolling(window= Period).mean()
    return ma

#RSI(Reletive Strength Index)相對強弱指標         ####錯誤
def RSI(df, period):
    diff= df['close'].diff()
    gain= (diff.where(diff>0, 0)).rolling(window= period).mean()
    loss= (diff.where(diff<0, 0)).rolling(window= period).mean()
    rs= gain/loss
    df['rsi']= 100-(100/(1+rs))
    return df
def RSI2(df, period):
    RSI =talib.RSI(df['close'], period)
    return RSI

#MACD
#DIF= EMA(close,12)- EMA(close, 26)
#DEM= EMA(Dif, 9)
#OSC= DIF-DEM= DIF-MACD
#指數移動平均數
def EMA(df, period):
    ema= df.ewm(span= period, adjust=False).mean()    
    return ema
def MACD(df, period1, period2, period3):
    
    
    Kbar= df['close']
    EMA1= EMA(Kbar, period1)
    EMA2= EMA(Kbar, period2)
    DIF= EMA1-EMA2    
    #print(DIF)
    Kbar= DIF
    #print(Kbar)
    DEM= EMA(Kbar, period3)
    #print(DEM)      
    OSC= DIF- DEM
    #print(OSC)
    return DIF, DEM, OSC

#布林通道(Bollinger Band)
#Bollinger(df, 移動平均值, 標準差值)
#長線：平均線+標準差  中線：平均線 短線：平均線-標準差
#標準差公式
def SD(df, period):
    sd= df['close'].rolling(window= period).std()
    return sd
def Bollinger(df, period, sdv):
    middle= MA(df, period)
    sd= SD(df, period)
    upper= middle+ sd*sdv
    lower= middle- sd*sdv    
    return middle, upper, lower

#Donchain Channel(DC, 唐奇安通道)
def DC(df, period):
    max= df['close'].rolling(window= period).max()
    min= df['close'].rolling(window= period).min()
    middle= (max+min)/2
    return max, min, middle

#williams(威廉通道)
def WR(df, period):
    close= df['close']
    high= df['high'].rolling(window= period).max()
    low= df['low'].rolling(window= period).min()
    wr= (high- close)/(high- low)*-100
    return wr



# #KDJ(隨機指標)
# import talib
# from talib import abstract
# abstract.STOCH(df)

# #OBV
# talib.OBV(df['close'], df['volume'])


