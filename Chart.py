#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 19:43:28 2024

@author: zhangjunzhi


chart 畫圖


"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.offline as pyoff


#K線 and MA 
def Kbarchart(df, Mdate1, Mdate2):
    with st.expander("K線圖, 移動平均線"):
        fig1 = make_subplots(specs=[[{"secondary_y": True}]])
        fig1.add_trace(go.Candlestick(x=df.index,
                       open= df['open'], high= df['high'],
                       low= df['low'], close= df['close'], name='K線'),
                       secondary_y= True)  
        fig1.add_trace(go.Scatter(x=df.index,
                       y= df['MA1'],
                       line=dict(color="red", width=2),
                       name= f"MA{Mdate1}"),
                       secondary_y= True)  
        fig1.add_trace(go.Scatter(x=df.index,
                       y= df['MA2'],
                       line=dict(color="blue", width=2),
                       name= f"MA{Mdate2}"),
                       secondary_y= True)  
        
        fig1.update_xaxes(rangeslider_visible=True, range=['2023-01-01', df.index[-1]])
        fig1.add_trace(go.Bar(x= df.index, y= df['volume'], name='成交量', marker=dict(color='black')),secondary_y=False)  
        st.plotly_chart(fig1, use_container_width=True)
#RSI圖
def Rsichart(df, Rsidate1, Rsidate2):
    
    with st.expander("RSI圖"):
        fig2 = make_subplots(specs=[[{"secondary_y": True}]])    
        fig2.add_trace(go.Scatter(x=df.index,
                               y=df['RSI1'],
                               mode='lines',
                               line=dict(color='red', width=2),
                               name=f"RSI={Rsidate1}"),
                               secondary_y=True)
        fig2.add_trace(go.Scatter(x=df.index,
                               y=df['RSI2'],
                               mode='lines',
                               line=dict(color='blue', width=2),
                               name= f"RSI={Rsidate2}"),
                               secondary_y=True)
        
        fig2.update_xaxes(rangeslider_visible=True, range=['2023-01-01', df.index[-1]])
        st.plotly_chart(fig2, use_container_width=True)
#MACD圖
def Macdchart(df, DIF, DEM, OSC):
           
    positive_color = 'red'  
    negative_color = 'green'  
    bar_colors = [positive_color if val > 0 else negative_color for val in OSC]

    with st.expander("MACD圖"):
        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        fig3.add_trace(go.Scatter(x=df.index,
                           y=DIF,
                           mode='lines',
                           line=dict(color='orange', width=2),
                           name= "DIF"),
                           secondary_y=True)
        fig3.add_trace(go.Scatter(x=df.index,
                           y=DEM,
                           mode='lines',
                           line=dict(color='pink', width=2),
                           name= "DEM"),
                           secondary_y=True)
        fig3.add_trace(go.Bar(x=df.index,
                           y=OSC,
                           marker=dict(color=bar_colors),
                           name= "OSC"),
                           secondary_y=True)
    
        fig3.update_xaxes(rangeslider_visible=True, range=['2023-01-01', df.index[-1]])
        st.plotly_chart(fig3, use_container_width= True)
#Bolling圖
def Bollingchart(df, Upper, Middle, Lower, BLN):
    with st.expander("布林通道"):
        fig4 = make_subplots(specs=[[{"secondary_y": True}]])
        fig4.add_trace(go.Scatter(x=df.index,
                               y=Upper,
                               mode='lines',
                               line=dict(color='red', width=2),
                               name= f"布林上{BLN}"),
                               secondary_y=True)
        fig4.add_trace(go.Scatter(x=df.index,
                               y= Middle,
                               mode='lines',
                               line=dict(color='blue', width=2),
                               name= f"布林中{BLN}"),
                               secondary_y=True)
        fig4.add_trace(go.Scatter(x=df.index,
                               y=Lower,
                               mode='lines',
                               line=dict(color='green', width=2),
                               name= f"布林下{BLN}"),
                               secondary_y=True)
       
        
        fig4.update_xaxes(rangeslider_visible=True, range=['2023-01-01', df.index[-1]])
        st.plotly_chart(fig4, use_container_width= True)
#Willing圖
def Willingchart(df, WLN):
    with st.expander("威廉指標"):
        fig5 = make_subplots(specs=[[{"secondary_y": True}]])
        fig5.add_trace(go.Scatter(x=df.index,
                               y=df['WR'],
                               mode='lines',
                               line=dict(color='red', width=2),
                               name= f"威廉指標{WLN}"),
                               secondary_y=True)
        
        fig5.update_xaxes(rangeslider_visible=True, range=['2023-01-01', df.index[-1]])
        st.plotly_chart(fig5, use_container_width= True)
#唐奇安通道DC
def DCchart(df, DCmax, DCmiddle, DCmin):
    with st.expander("唐奇安通道"):
        fig6 = make_subplots(specs=[[{"secondary_y": True}]])
        fig6.add_trace(go.Candlestick(x=df.index,
                       open= df['open'], high= df['high'],
                       low= df['low'], close= df['close'], name='K線'),
                       secondary_y= True)  
        fig6.add_trace(go.Scatter(x=df.index,
                       y= DCmax,
                       line=dict(color="blue", width=2),
                       name= "上通道"),
                       secondary_y= True)  
        fig6.add_trace(go.Scatter(x=df.index,
                       y= DCmin,
                       line=dict(color="blue", width=2),
                       name= "下通道"),
                       secondary_y= True)   
        fig6.add_trace(go.Scatter(x=df.index,
                       y= DCmiddle,
                       line=dict(color="red", width=2),
                       name= "中通道"),
                       secondary_y= True)  
        
        fig6.update_xaxes(rangeslider_visible=True, range=['2023-01-01', df.index[-1]])
        st.plotly_chart(fig6, use_container_width=True)
#移動平均線回測
def MAbacktest(df, Mdate1, Mdate2, OB, CS, OS, CB):
    with st.expander("移動平均線回測"):
            fig7 = make_subplots(specs=[[{"secondary_y": True}]])
            fig7.add_trace(go.Candlestick(x=df.index,
                           open= df['open'], high= df['high'],
                           low= df['low'], close= df['close'], name='K線'),
                           secondary_y= True)  
            fig7.add_trace(go.Scatter(x=df.index,
                           y= df['MA1'],
                           line=dict(color="red", width=2),
                           name= f"MA{Mdate1}"),
                           secondary_y= True)  
            fig7.add_trace(go.Scatter(x=df.index,
                           y= df['MA2'],
                           line=dict(color="blue", width=2),
                           name= f"MA{Mdate2}"),
                           secondary_y= True)  
            fig7.add_trace(go.Scatter(x=[i[2] for i in OB], 
                                      y=[i[3] for i in OB], mode='markers',  
                                      marker=dict(color='red', 
                                                 symbol='triangle-up', 
                                                  size=8), 
                                      name='作多進場點'), 
                           secondary_y=False)
            fig7.add_trace(go.Scatter(x=[i[2] for i in CS], 
                                      y=[i[3] for i in CS], mode='markers',  
                                      marker=dict(color='green', 
                                                  symbol='triangle-down', 
                                                  size=8), 
                                      name='作多出場點'), 
                           secondary_y=False)
            fig7.add_trace(go.Scatter(x=[i[2] for i in OS], 
                                      y=[i[3] for i in OS], mode='markers',  
                                      marker=dict(color='pink', 
                                                  symbol='triangle-up', 
                                                  size=8), 
                                      name='作空進場點'), 
                           secondary_y=False)
            fig7.add_trace(go.Scatter(x=[i[2] for i in CB], 
                                      y=[i[3] for i in CB], mode='markers',  
                                      marker=dict(color='blue', 
                                                  symbol='triangle-down', 
                                                  size=8), 
                                      name='作空出場點'), 
                           secondary_y=False)
            
            
            st.plotly_chart(fig7, use_container_width=True)
            





































