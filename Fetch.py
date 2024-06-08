#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 13:58:38 2024

@author: zhangjunzhi

抓取股票價格
"""


import pandas as pd
import streamlit as st 
import yfinance as yf
import Driver


def Fetch(Stock_ID, start, end):
        try:
            data= yf.download(Stock_ID, start= start, end= end)
            data= pd.DataFrame(data)
            try:
                new_titles = {'Date': 'Date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}
                data.rename(columns=new_titles, inplace=True)
                file_name= f"{start}_{end}_{Stock_ID}.xlsx"
                data.to_excel(file_name)
                Driver.upload_file(file_name, file_name)
                st.success("存取成功")
                return data
            except:
                    st.error("存取失敗")
        except Exception as e:
            st.error("抓取失敗")
            st.error(str(e))
            

#data= yf.download('2330', start= '2024-5-24', end= '2024-5-24')
