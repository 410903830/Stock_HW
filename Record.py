#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 18:08:32 2024

@author: zhangjunzhi


#####交易紀錄


"""

import pandas as pd 
import random


class Record():
    def __init__(self): ##建構子
    
        #績效
        self.Profit= []
        self.ProfitRate= []
        #未平倉        
            #資訊
        self.StockRecord= []
            #數量
        self.StockQty= 0
        
        #全部交易紀錄
        self.AllTradeRecord= []
        
        
        #進場紀錄
        #出場紀錄