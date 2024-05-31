#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 19:53:53 2024

@author: zhangjunzhi

主頁

"""

import pandas as pd 
import streamlit as st
import Indicator as Ec
import Chart as ch
import Fetch



html_content = """
<h1 style='color: blue; position: sticky; z-index: 9999;''>金融看板平台</h1>
"""
st.markdown(html_content, unsafe_allow_html=True)






#選擇資料來源
data= None
df = pd.read_excel("2014-05-31_2024-05-31_2330.tw.xlsx")
df= df.set_index('Date')


st.subheader("選擇金融商品")

mode = st.radio("抓取方式:", ["yfiance抓取", "雲端抓取"])

if mode == "yfiance抓取":
    Stock_ID= st.text_input("請輸入股票代碼 ex: 2330.tw", value="2330.tw")
    col1, col2= st.columns(2)
    with col1:
        start= st.date_input("選擇開始日")

    with col2:
        end= st.date_input("選擇結束日")
    if st.button("Fetch"):
        data= Fetch.Fetch(Stock_ID, start, end)
else:
    option= st.selectbox(
        "請選擇金融商品",
        ("2330", "3005")
        )


# if data is not None and not data.empty:
#     df= data
#     df= df.set_index('Date')
#     st.success("data成功")


###############################################################################


#填寫相關數據
st.subheader("設定指標參數")
#K棒參數
with st.expander("設定Ｋ棒相關參數"):
    Datenum= st.selectbox("選擇Ｋ棒時間單位",{"日", "週", "月"})
    Datelen= st.number_input("設定K棒長度(長度1~10)", min_value=1, max_value=10, value=1, key=int)
#平均線天數
with st.expander("設定平均線天數"):    
    Mdate1= st.slider("設定移動平均長度（日）", min_value= 1, max_value= 100, value= 5, key='mdate1' )
    #st.write(Mdate1)
    Mdate2= st.slider("設定移動平均長度（日）", min_value= 1, max_value= 100, value= 20, key='mdate2' )
#Rsi線天數
with st.expander("設定RSI天數"):
    Rsidate1= st.slider("設定RSI平均天數", min_value=1, max_value=100, value=6, key="Rsidate1")
    #st.write(Rsidate1)
    Rsidate2= st.slider("設定RSI平均天數", min_value=1, max_value=100, value=14, key="Rsidate2")
with st.expander("設定布林天數"):
    BLN= st.slider("設定布林天數", min_value=1, max_value=100, value=20, key="BLN")
with st.expander("設定威廉天數"):
    WLN= st.slider("設定威廉天數", min_value=1, max_value=100, value=24, key="WLN")
with st.expander("設定MACD"):
    EMAS= st.slider("設定短期", min_value=1, max_value=100, value=12, key="EMAS")
    EMAL= st.slider("設定長期", min_value=1, max_value=100, value=26, key="EMAL")
    MACDL= st.slider("設定MACD", min_value=1, max_value=100, value=9, key="MACDL")


#呼叫指標方法
Ec.KbarType(df)
Ec.KbarToDict(df)
#MA
df['MA1']=Ec.MA(df, Mdate1)
df['MA2']=Ec.MA(df, Mdate2)
#RSI
df['RSI1']= Ec.RSI2(df, Rsidate1)
df['RSI2']= Ec.RSI2(df, Rsidate2)
#MACD
DIF, DEM, OSC= Ec.MACD(df, EMAS, EMAL, MACDL)
#Bollinger
Upper, Middle, Lower= Ec.Bollinger(df, 20, 2)
#DC
DCmax, DCmin, DCmiddle= Ec.DC(df, 20)
#Willing
df['WR']= Ec.WR(df, WLN)




st.subheader("畫圖")
##### K線圖, 移動平均線 MA
ch.Kbarchart(df, Mdate1, Mdate2)
#####RSI
ch.Rsichart(df, Rsidate1, Rsidate2)
#####MACD
ch.Macdchart(df, DIF, DEM, OSC)
######Bollinger
ch.Bollingchart(df, Upper, Middle, Lower, BLN)
######Willinger
ch.Willingchart(df, WLN)
######唐奇安通道
ch.DCchart(df, DCmax, DCmiddle, DCmin)
#####KDJ
#####OBV




#呼叫交易方法


#呼叫交易損益並回測

st.subheader("程式交易回測")








footer_html = """
<footer style="text-align: center; padding-top: 20px;">
    <p>Copyright © 2024  Zhang-Jun-Zhi</p>
</footer>
"""
st.markdown(footer_html, unsafe_allow_html=True)