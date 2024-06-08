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
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.font_manager import FontProperties as font
font_path = "Cactus_Classical_Serif/CactusClassicalSerif-Regular.ttf"
font = font(fname=font_path)


html_content = """


<div style='width: 43%; height: 150px; background-color: blue; position: fixed; top: 0; z-index:99999; border-radius:10px;'>
    <h1 style='color: white; margin: 50px 40px;'>金融看板平台</h1>
</div>

<br>
<br>
<br>



"""
st.markdown(html_content, unsafe_allow_html=True)






#選擇資料來源
data= None
df = pd.read_excel("2014-05-31_2024-05-31_2330.tw.xlsx")
df['Date'] = pd.to_datetime(df['Date'])
df= df.set_index('Date')




st.subheader("選擇金融商品")

st.text("預設資料:2330.tw")
mode = st.radio("抓取方式:", ["yfiance抓取", "雲端抓取"])

if mode == "yfiance抓取":
    Stock_ID= st.text_input("請輸入股票代碼 ex: 2330.tw (上市)/ 3213.TWO (上櫃) / TSLA(美股) / NVDA(美股)", value="2330.tw")
    col1, col2= st.columns(2)
    with col1:
        start= st.date_input("選擇開始日")

    with col2:
        end= st.date_input("選擇結束日")
    if st.button("Fetch"):
        data= Fetch.Fetch(Stock_ID, start, end)
        data= pd.DataFrame(data)
        data.reset_index(inplace=True)
        data['Date'] = pd.to_datetime(df['Date'])
        data= data.set_index(data['Date'])
        df= data
        if df.empty:
            st.error("此股票抓取失敗(沒有資料)")
        else:
            st.success("此股票抓取成功")
else:
    option= st.selectbox(
        "請選擇金融商品",
        ("2330")
        )


# if data is not None and not data.empty:
#     df= data
#     df= df.set_index('Date')
#     st.success("data成功")


#############################################################################################################################################################################################################################################


#填寫相關數據
st.subheader("設定指標參數")
#K棒參數
with st.expander("設定Ｋ棒相關參數"):
    data= df
    Datenum= st.selectbox("選擇時間單位",{"日", "週", "月"}, index=1)
    aggregation = {
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'open': 'first',
        'volume': 'sum'
    }
    if Datenum == "日":
        df = data
    elif Datenum == "週":
        df = df.resample('W').agg(aggregation)
    else:  # "月" 的情况
        df = df.resample('M').agg(aggregation)
#平均線天數
with st.expander("設定平均線天數"):    
    Mdate1= st.slider("設定短移動平均線長度（日）", min_value= 1, max_value= 100, value= 5, key='mdate1' )
    Mdate2= st.slider("設定長移動平均線長度（日）", min_value= 1, max_value= 100, value= 20, key='mdate2' )
    if Mdate1>Mdate2:
        st.warning("短平均線必須小於長平均線")
    
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
  
with st.expander("設定KDJ"):
    KDN1= st.slider("期間", min_value=1, max_value=100, value=14, key="KDN1")
    KDN2= st.slider("K", min_value=1, max_value=100, value=3, key="KDN2")
    KDN3= st.slider("D", min_value=1, max_value=100, value=3, key="KDN3")
#############################################################################################################################################################################################################################################    
    


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
#KDJ
df['K'], df['D'], df['J']= Ec.KDJ(df, KDN1, KDN2, KDN3)
#OBV
df['OBV']= Ec.OBV(df)


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
ch.KDJchart(df)
#####OBV
ch.OBVchart(df)


#############################################################################################################################################################################################################################################


st.subheader("回測參數")

    #順勢RSI回測參數
with st.expander("順勢RSI回測"):
    minline1= st.slider("RSI多少時停損/做空 ex: 45", value=50, max_value= 80, min_value= 20 )
    maxline1= st.slider("RSI多少時停損/作多 ex: 55", value=50, max_value= 80, min_value= 20 )
    
    
    #逆勢RSI回測參數
with st.expander("逆勢RSI回測"):
    minline2= st.slider("RSI突破多少時停損轉做多 ex: 45", value=20, max_value= 20, min_value= 0 )
    maxline2= st.slider("RSI跌破多少時停損轉作空 ex: 55", value=80, max_value= 100, min_value= 80 )






#############################################################################################################################################################################################################################################




#呼叫交易損益並回測
#績效


st.subheader("程式交易回測/績效")


#####平均線策略
#############################################################################################################################################################################################################################################

import Order
import Backtest as BT

MARecord= BT.BackMA(df)

#get all record 
allrecord= MARecord.OrderRecord.AllTradeRecord
#MA
MAOB= [i for i in allrecord if i[0]== 1 and i[1]== 'OrderBuy']
#進場做空
MAOS= [i for i in allrecord if i[0]== -1 and i[1]== 'OrderSell']
#出場賣出
MACS= [i for i in allrecord if i[0]== -1 and i[1]== 'Cover Sell']
#出場買入
MACB= [i for i in allrecord if i[0]== 1 and i[1]== 'Cover Buy']

totalprofit= Order.gettotalprofit(MARecord)
avgprofit= Order.getAvgProfit(MARecord)
Mdd= Order.GetMDD(MARecord)
profit= Order.getprofit(MARecord)
Postive= Order.getPprofit(MARecord)
Nagtive= Order.getNprofit(MARecord)

performance= {
                "項目":["交易總盈虧(元)", "平均投資報酬率", "獲利(只看獲利的)(元)", "虧損(只看虧損的)(元)", "最大盈虧回落(MDD)(元)"],
                "數值":[totalprofit, avgprofit+"%", Postive, Nagtive, Mdd]
    
    }



ch.MAbacktest(df, Mdate1, Mdate2, MAOB, MACS, MAOS, MACB)
with st.expander("績效"):
    x= np.arange(len(profit))
    plt.title("累計盈虧(多空)", fontproperties=font)
    plt.axhline(y=0, color="red", linestyle= '-')
    plt.plot(x, profit)
    plt.xlabel("(交易筆數)", fontproperties=font)
    plt.ylabel("(1000元)", fontproperties=font)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.table(performance)
    st.pyplot()

    
       
#####順勢RSI策略     
#############################################################################################################################################################################################################################################

Rsi1Record= BT.BackRsi1(df, maxline1, minline1)

allrecord= Rsi1Record.OrderRecord.AllTradeRecord
#RSI
#進場做多
RSIOB= [i for i in allrecord if i[0]== 1 and i[1]== 'OrderBuy']
#進場做空
RSIOS= [i for i in allrecord if i[0]== -1 and i[1]== 'OrderSell']
#出場賣出
RSICS= [i for i in allrecord if i[0]== -1 and i[1]== 'Cover Sell']
#出場買入
RSICB= [i for i in allrecord if i[0]== 1 and i[1]== 'Cover Buy']

totalprofit= Order.gettotalprofit(Rsi1Record)
avgprofit= Order.getAvgProfit(Rsi1Record)
Mdd= Order.GetMDD(Rsi1Record)
profit= Order.getprofit(Rsi1Record)
Postive= Order.getPprofit(Rsi1Record)
Nagtive= Order.getNprofit(Rsi1Record)

performance= {
                "項目":["交易總盈虧(元)", "平均投資報酬率", "獲利(只看獲利的)(元)", "虧損(只看虧損的)(元)", "最大盈虧回落(MDD)(元)"],
                "數值":[totalprofit, avgprofit+"%", Postive, Nagtive, Mdd]
    
    }



ch.RSIbacktest(df, Rsidate1, Rsidate2, RSIOB, RSICS, RSIOS, RSICB, "順勢RSI指標回測")
with st.expander("績效"):
    x= np.arange(len(profit))
    plt.title("累計盈虧(多空)", fontproperties=font)
    plt.axhline(y=0, color="red", linestyle= '-')
    plt.plot(x, profit)
    plt.xlabel("(交易筆數)", fontproperties=font)
    plt.ylabel("(1000元)", fontproperties=font)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.table(performance)
    st.pyplot()
    
    

#####逆勢RSI策略     
#############################################################################################################################################################################################################################################
Rsi2Record= BT.BackRsi2(df, minline2, maxline2)

allrecord= Rsi2Record.OrderRecord.AllTradeRecord

RSIOB2= [i for i in allrecord if i[0]== 1 and i[1]== 'OrderBuy']
#進場做空
RSIOS2= [i for i in allrecord if i[0]== -1 and i[1]== 'OrderSell']
#出場賣出
RSICS2= [i for i in allrecord if i[0]== -1 and i[1]== 'Cover Sell']
#出場買入
RSICB2= [i for i in allrecord if i[0]== 1 and i[1]== 'Cover Buy']

totalprofit= Order.gettotalprofit(Rsi2Record)
avgprofit= Order.getAvgProfit(Rsi2Record)
Mdd= Order.GetMDD(Rsi2Record)
profit= Order.getprofit(Rsi2Record)
Postive= Order.getPprofit(Rsi2Record)
Nagtive= Order.getNprofit(Rsi2Record)


performance= {
                "項目":["交易總盈虧(元)", "平均投資報酬率", "獲利(只看獲利的)(元)", "虧損(只看虧損的)(元)", "最大盈虧回落(MDD)(元)"],
                "數值":[totalprofit, avgprofit+"%", Postive, Nagtive, Mdd]
    
    }
ch.RSIbacktest(df, Rsidate1, Rsidate2, RSIOB2, RSICS2, RSIOS2, RSICB2, "逆勢RSI指標回測")
with st.expander("績效"):
    x= np.arange(len(profit))
    plt.title("累計盈虧(多空)", fontproperties=font)
    plt.axhline(y=0, color="red", linestyle= '-')
    plt.plot(x, profit)
    plt.xlabel("(交易筆數)", fontproperties=font)
    plt.ylabel("(1000元)", fontproperties=font)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.table(performance)
    st.pyplot()
    

####只做多RSI策略     
############################################################################################################################################################################################################################################
Rsi3Record= BT.BackRsi3(df, minline1)


allrecord= Rsi3Record.OrderRecord.AllTradeRecord

RSIOB3= [i for i in allrecord if i[0]== 1 and i[1]== 'OrderBuy']
#進場做空
RSIOS3= [i for i in allrecord if i[0]== -1 and i[1]== 'OrderSell']
#出場賣出
RSICS3= [i for i in allrecord if i[0]== -1 and i[1]== 'Cover Sell']
#出場買入
RSICB3= [i for i in allrecord if i[0]== 1 and i[1]== 'Cover Buy']

totalprofit= Order.gettotalprofit(Rsi3Record)
avgprofit= Order.getAvgProfit(Rsi3Record)
Mdd= Order.GetMDD(Rsi3Record)
profit= Order.getprofit(Rsi3Record)
Postive= Order.getPprofit(Rsi3Record)
Nagtive= Order.getNprofit(Rsi3Record)



performance= {
                "項目":["交易總盈虧(元)", "平均投資報酬率", "獲利(只看獲利的)(元)", "虧損(只看虧損的)(元)", "最大盈虧回落(MDD)(元)"],
                "數值":[totalprofit, avgprofit+"%", Postive, Nagtive, Mdd]
    
    }
ch.RSIbacktest(df, Rsidate1, Rsidate2, RSIOB3, RSICS3, RSIOS3, RSICB3, "RSI指標回測(只做多)")
with st.expander("績效"):
    x= np.arange(len(profit))
    plt.title("累計盈虧(多空)", fontproperties=font)
    plt.axhline(y=0, color="red", linestyle= '-')
    plt.plot(x, profit)
    plt.xlabel("(交易筆數)", fontproperties=font)
    plt.ylabel("(1000元)", fontproperties=font)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.table(performance)
    st.pyplot()
    
    
    



# #####只做空RSI策略     
# #############################################################################################################################################################################################################################################
Rsi4Record= BT.BackRsi4(df, maxline1)

allrecord= Rsi4Record.OrderRecord.AllTradeRecord

RSIOB4= [i for i in allrecord if i[0]== 1 and i[1]== 'OrderBuy']
#進場做空
RSIOS4= [i for i in allrecord if i[0]== -1 and i[1]== 'OrderSell']
#出場賣出
RSICS4= [i for i in allrecord if i[0]== -1 and i[1]== 'Cover Sell']
#出場買入
RSICB4= [i for i in allrecord if i[0]== 1 and i[1]== 'Cover Buy']

totalprofit= Order.gettotalprofit(Rsi4Record)
avgprofit= Order.getAvgProfit(Rsi4Record)
Mdd= Order.GetMDD(Rsi4Record)
profit= Order.getprofit(Rsi4Record)
Postive= Order.getPprofit(Rsi4Record)
Nagtive= Order.getNprofit(Rsi4Record)



performance= {
                "項目":["交易總盈虧(元)", "平均投資報酬率", "獲利(只看獲利的)(元)", "虧損(只看虧損的)(元)", "最大盈虧回落(MDD)(元)"],
                "數值":[totalprofit, avgprofit+"%", Postive, Nagtive, Mdd]
    
    }
ch.RSIbacktest(df, Rsidate1, Rsidate2, RSIOB4, RSICS4, RSIOS4, RSICB4, "RSI指標回測(只做空)")
with st.expander("績效"):
    x= np.arange(len(profit))
    plt.title("累計盈虧(多空)", fontproperties=font)
    plt.axhline(y=0, color="red", linestyle= '-')
    plt.plot(x, profit)
    plt.xlabel("(交易筆數)", fontproperties=font)
    plt.ylabel("(1000元)", fontproperties=font)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.table(performance)
    st.pyplot()


#####MACD策略     
#############################################################################################################################################################################################################################################
MACDRecord= BT.BcakMACD(df, DIF, DEM)

allrecord= MACDRecord.OrderRecord.AllTradeRecord

MACDOB= [i for i in allrecord if i[0]== 1 and i[1]== 'OrderBuy']
#進場做空
MACDOS= [i for i in allrecord if i[0]== -1 and i[1]== 'OrderSell']
#出場賣出
MACDCS= [i for i in allrecord if i[0]== -1 and i[1]== 'Cover Sell']
#出場買入
MACDCB= [i for i in allrecord if i[0]== 1 and i[1]== 'Cover Buy']

ch.MACDbacktest(df, MACDOB, MACDCS, MACDOS, MACDCB, DIF, DEM)

totalprofit= Order.gettotalprofit(MACDRecord)
avgprofit= Order.getAvgProfit(MACDRecord)
Mdd= Order.GetMDD(MACDRecord)
profit= Order.getprofit(MACDRecord)
Postive= Order.getPprofit(MACDRecord)
Nagtive= Order.getNprofit(MACDRecord)

performance= {
                "項目":["交易總盈虧(元)", "平均投資報酬率", "獲利(只看獲利的)(元)", "虧損(只看虧損的)(元)", "最大盈虧回落(MDD)(元)"],
                "數值":[totalprofit, avgprofit+"%", Postive, Nagtive, Mdd]
    
    }


with st.expander("績效"):
    x= np.arange(len(profit))
    plt.title("累計盈虧(多空)", fontproperties=font)
    plt.axhline(y=0, color="red", linestyle= '-')
    plt.plot(x, profit)
    plt.xlabel("(交易筆數)", fontproperties=font)
    plt.ylabel("(1000元)", fontproperties=font)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.table(performance)
    st.pyplot()


   
#############################################################################################################################################################################################################################################

footer_html = """
<footer style="text-align: center; bottom: 0;">
    <p>Copyright © 2024  Zhang-Jun-Zhi  CSCE4B</p>
</footer>
"""
st.markdown(footer_html, unsafe_allow_html=True)