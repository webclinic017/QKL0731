#encoding=utf-8

import tushare as ts
import numpy as num
import time
from dingtalkchatbot.chatbot import DingtalkChatbot
import matplotlib
import matplotlib.pyplot as plt
import os
import tushare as ts
import talib as ta
import pandas as pd
import ccxt

'''
公共功能：ENE指标
'''
def ENE_zhibiao(doubleCloseArray):
     param_m1 = 11
     param_m2 = 9
     param_n = 10
     sma_n = ta.SMA(doubleCloseArray, param_n)
     upper = (1 + param_m1 / 100) * sma_n
     lower = (1 - param_m2 / 100) * sma_n
     ene = (upper + lower) / 2
     upper = upper.round(2)
     ene = ene.round(2)
     lower = lower.round(2)

'''
公共功能：KDJ指标
'''
def KDJ_zhibiao(data_history, doubleCloseArray):
     stock_data = {}
     low_list = data_history.low.rolling(9).min()
     low_list.fillna(value=data_history.low.expanding().min(), inplace=True)
     high_list = data_history.high.rolling(9).max()
     high_list.fillna(value=data_history.high.expanding().max(), inplace=True)
     rsv = (doubleCloseArray - low_list) / (high_list - low_list) * 100
     stock_data['KDJ_K'] = pd.DataFrame.ewm(rsv, com=2).mean()
     stock_data['KDJ_D'] = pd.DataFrame.ewm(stock_data['KDJ_K'], com=2).mean()
     stock_data['KDJ_J'] = 3 * stock_data['KDJ_K'] - 2 * stock_data['KDJ_D']
     dddd = pd.DataFrame(stock_data)
     KDJ_J_title = "KDJ_" + "%.2f" % dddd.KDJ_J[len(dddd) - 1] + " "
     KDJ_K = "%.2f" % dddd.KDJ_K[len(dddd) - 1]
     KDJ_D = "%.2f" % dddd.KDJ_D[len(dddd) - 1]
     KDJ_J = "%.2f" % dddd.KDJ_J[len(dddd) - 1]
     return KDJ_K, KDJ_D, KDJ_J, KDJ_J_title


'''
公共功能：BULL指标
'''
def BULL_zhibiao(doubleCloseArray, closeArray, lowArray):
     upperband, middleband, lowerband = ta.BBANDS(doubleCloseArray, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
     BULL_middleband = ""
     if (middleband[-1] >= middleband[-2]):
          BULL_middleband = "布林中线趋势上升"
     else:
          BULL_middleband = "布林中线趋势下降"

     BULL_title = ""
     if (closeArray[-1] > upperband[-1]):
          BULL_title = "上穿布林线上沿"

     if (lowArray[-1] < lowerband[-1] * 1.005):
          BULL_title = "下穿布林线下沿"

     upperband = "%.2f" % upperband[-1]
     middleband = "%.2f" % middleband[-1]
     lowerband = "%.2f" % lowerband[-1]
     return upperband, middleband, lowerband, BULL_title, BULL_middleband

'''
公共功能：MACD指标
'''
def MACD_zhibiao(doubleCloseArray):
     # macd 为快线 macdsignal为慢线，macdhist为柱体
     macd, macdsignal, macdhist = ta.MACD(doubleCloseArray, fastperiod=12, slowperiod=26, signalperiod=9)
     MACD_title = ""
     if (macdsignal[-1] > macdsignal[-2]):
          MACD_title = "MACD慢线上行1"
          if (macdsignal[-2] > macdsignal[-3]):
               MACD_title = "MACD慢线上行2"
               if (macdsignal[-3] > macdsignal[-4]):
                    MACD_title = "MACD慢线上行3"
                    if (macdsignal[-4] > macdsignal[-5]):
                         MACD_title = "MACD慢线上行4"
                         if (macdsignal[-5] > macdsignal[-6]):
                              MACD_title = "MACD慢线上行5"
                              if (macdsignal[-6] > macdsignal[-7]):
                                   MACD_title = "MACD慢线上行6"
                                   if (macdsignal[-7] > macdsignal[-8]):
                                        MACD_title = "MACD慢线上行7"
                                        if (macdsignal[-8] > macdsignal[-9]):
                                             MACD_title = "MACD慢线上行8"
                                             if (macdsignal[-9] > macdsignal[-10]):
                                                  MACD_title = "MACD慢线上行9"
                                                  if (macdsignal[-11] > macdsignal[-12]):
                                                       MACD_title = "MACD慢线上行10"

     return MACD_title

'''
公共功能：均线指标
'''
def junxian_zhibiao(doubleCloseArray, doubleOpenArray):
     MA_5 = ta.SMA(doubleCloseArray, timeperiod=5)
     MA_10 = ta.SMA(doubleCloseArray, timeperiod=10)
     MA_20 = ta.SMA(doubleCloseArray, timeperiod=20)
     MA20_titile = ""
     if (doubleCloseArray[-1] > MA_20[-1] and doubleOpenArray[-1] < MA_20[-1]):
          MA20_titile = "20均线上穿"

     MA30_titile = ""
     MA_30 = ta.SMA(doubleCloseArray, timeperiod=30)
     if (MA_30[-1] > MA_30[-2]):
          MA30_titile = "30均线上行1"
          if (MA_30[-2] > MA_30[-3]):
               MA30_titile = "30均线上行2"
               if (MA_30[-3] > MA_30[-4]):
                    MA30_titile = "30均线上行3"
                    if (MA_30[-4] > MA_30[-5]):
                         MA30_titile = "30均线上行4"
                         if (MA_30[-5] > MA_30[-6]):
                              MA30_titile = "30均线上行5"
                              if (MA_30[-6] > MA_30[-7]):
                                   MA30_titile = "30均线上行6"
                                   if (MA_30[-7] > MA_30[-8]):
                                        MA30_titile = "30均线上行7"
                                        if (MA_30[-8] > MA_30[-9]):
                                             MA30_titile = "30均线上行8"
                                             if (MA_30[-9] > MA_30[-10]):
                                                  MA30_titile = "30均线上行9"
                                                  if (MA_30[-10] > MA_30[-11]):
                                                       MA30_titile = "30均线上行10"

     MA60_titile = ""
     MA_60 = ta.SMA(doubleCloseArray, timeperiod=60)
     if (MA_60[-1] > MA_60[-2]):
          MA60_titile = "60均线上行1"
          if (MA_60[-2] > MA_60[-3]):
               MA60_titile = "60均线上行2"
               if (MA_60[-3] > MA_60[-4]):
                    MA60_titile = "60均线上行3"
                    if (MA_60[-4] > MA_60[-5]):
                         MA60_titile = "60均线上行4"
                         if (MA_60[-5] > MA_60[-6]):
                              MA60_titile = "60均线上行5"
                              if (MA_60[-6] > MA_60[-7]):
                                   MA60_titile = "60均线上行6"
                                   if (MA_60[-7] > MA_60[-8]):
                                        MA60_titile = "60均线上行7"
                                        if (MA_60[-8] > MA_60[-9]):
                                             MA60_titile = "60均线上行8"
                                             if (MA_60[-9] > MA_60[-10]):
                                                  MA60_titile = "60均线上行9"
                                                  if (MA_60[-10] > MA_60[-11]):
                                                       MA60_titile = "60均线上行10"

     qushi_5_10_20_30 = ""
     if (MA_5[-1] > MA_5[-2] and MA_10[-1] > MA_10[-2] and MA_20[-1] > MA_20[-2] and MA_30[-1] > MA_30[-2]):
          qushi_5_10_20_30 = "均线5、10、20、30齐升1"
          if (MA_5[-2] > MA_5[-3] and MA_10[-2] > MA_10[-3] and MA_20[-2] > MA_20[-3] and MA_30[-2] > MA_30[-3]):
               qushi_5_10_20_30 = "均线5、10、20、30齐升2"
               if (MA_5[-3] > MA_5[-4] and MA_10[-3] > MA_10[-4] and MA_20[-3] > MA_20[-4] and MA_30[-3] > MA_30[-4]):
                    qushi_5_10_20_30 = "均线5、10、20、30齐升3"
                    if (MA_5[-4] > MA_5[-5] and MA_10[-4] > MA_10[-5] and MA_20[-4] > MA_20[-5] and MA_30[-4] > MA_30[
                         -5]):
                         qushi_5_10_20_30 = "均线5、10、20、30齐升4"
                         if (MA_5[-5] > MA_5[-6] and MA_10[-5] > MA_10[-6] and MA_20[-5] > MA_20[-6] and MA_30[-5] >
                                 MA_30[-6]):
                              qushi_5_10_20_30 = "均线5、10、20、30齐升5"
                              if (MA_5[-6] > MA_5[-7] and MA_10[-6] > MA_10[-7] and MA_20[-6] > MA_20[-7] and MA_30[
                                   -6] > MA_30[-7]):
                                   qushi_5_10_20_30 = "均线5、10、20、30齐升6"
                                   if (MA_5[-7] > MA_5[-8] and MA_10[-7] > MA_10[-8] and MA_20[-7] > MA_20[-8] and
                                           MA_30[-7] > MA_30[-8]):
                                        qushi_5_10_20_30 = "均线5、10、20、30齐升7"
                                        if (MA_5[-8] > MA_5[-9] and MA_10[-8] > MA_10[-9] and MA_20[-8] > MA_20[-9] and
                                                MA_30[-8] > MA_30[-9]):
                                             qushi_5_10_20_30 = "均线5、10、20、30齐升8"
                                             if (MA_5[-9] > MA_5[-10] and MA_10[-9] > MA_10[-10] and MA_20[-9] > MA_20[
                                                  -10] and MA_30[-9] > MA_30[-10]):
                                                  qushi_5_10_20_30 = "均线5、10、20、30齐升9"

     if (MA_5[-1] < MA_5[-2] and MA_10[-1] < MA_10[-2] and MA_20[-1] < MA_20[-2] and MA_30[-1] < MA_30[-2]):
          qushi_5_10_20_30 = "均线5、10、20、30齐降1"
          if (MA_5[-2] < MA_5[-3] and MA_10[-2] < MA_10[-3] and MA_20[-2] < MA_20[-3] and MA_30[-2] < MA_30[-3]):
               qushi_5_10_20_30 = "均线5、10、20、30齐降2"
               if (MA_5[-3] < MA_5[-4] and MA_10[-3] < MA_10[-4] and MA_20[-3] < MA_20[-4] and MA_30[-3] < MA_30[-4]):
                    qushi_5_10_20_30 = "均线5、10、20、30齐降3"
                    if (MA_5[-4] < MA_5[-5] and MA_10[-4] < MA_10[-5] and MA_20[-4] < MA_20[-5] and MA_30[-4] < MA_30[
                         -5]):
                         qushi_5_10_20_30 = "均线5、10、20、30齐降4"
                         if (MA_5[-5] < MA_5[-6] and MA_10[-5] < MA_10[-6] and MA_20[-5] < MA_20[-6] and MA_30[-5] <
                                 MA_30[-6]):
                              qushi_5_10_20_30 = "均线5、10、20、30齐降5"
                              if (MA_5[-6] < MA_5[-7] and MA_10[-6] < MA_10[-7] and MA_20[-6] < MA_20[-7] and MA_30[
                                   -6] < MA_30[-7]):
                                   qushi_5_10_20_30 = "均线5、10、20、30齐降6"
                                   if (MA_5[-7] < MA_5[-8] and MA_10[-7] < MA_10[-8] and MA_20[-7] < MA_20[-8] and
                                           MA_30[-7] < MA_30[-8]):
                                        qushi_5_10_20_30 = "均线5、10、20、30齐降7"
                                        if (MA_5[-8] < MA_5[-9] and MA_10[-8] < MA_10[-9] and MA_20[-8] < MA_20[-9] and
                                                MA_30[-8] < MA_30[-9]):
                                             qushi_5_10_20_30 = "均线5、10、20、30齐降8"
                                             if (MA_5[-9] < MA_5[-10] and MA_10[-9] < MA_10[-10] and MA_20[-9] < MA_20[
                                                  -10] and MA_30[-9] < MA_30[-10]):
                                                  qushi_5_10_20_30 = "均线5、10、20、30齐降9"

     return MA20_titile, MA30_titile, MA60_titile, qushi_5_10_20_30

'''
公共功能：指标
'''
def zhibiao(name, zhouqi):
     gateio = ccxt.gateio()
     huobi = ccxt.huobipro()
     binance = ccxt.binance()
     limit = 500
     current_time = int(time.time() // 60 * 60 * 1000)

     if (zhouqi == '15m'):
          since_time_15 = current_time - limit * 1 * 15 * 60 * 1000
          data = huobi.fetch_ohlcv(symbol=name, timeframe='15m', limit=500, since=since_time_15)
     if (zhouqi == '30m'):
          since_time_30 = current_time - limit * 1 * 30 * 60 * 1000
          data = huobi.fetch_ohlcv(symbol=name, timeframe='30m', limit=500, since=since_time_30)
     if (zhouqi == '1h'):
          since_time = current_time - limit * 1 * 60 * 60 * 1000
          data = huobi.fetch_ohlcv(symbol=name, timeframe='1h', limit=500, since=since_time)
     if (zhouqi == '4h'):
          since_time = current_time - limit * 4 * 60 * 60 * 1000
          data = binance.fetch_ohlcv(symbol=name, timeframe='4h', limit=500, since=since_time)

     df = pd.DataFrame(data)
     df = df.rename(columns={0: 'open_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'})
     df['open_time'] = pd.to_datetime(df['open_time'], unit='ms') + pd.Timedelta(hours=8)
     closeArray = num.array(df['close'])
     highArray = num.array(df['high'])
     lowArray = num.array(df['low'])
     openArray = num.array(df['open'])
     doubleCloseArray = num.asarray(closeArray, dtype='double')
     doubleHighArray = num.asarray(highArray, dtype='double')
     doubleLowArray = num.asarray(lowArray, dtype='double')
     doubleOpenArray = num.asarray(openArray, dtype='double')

     ########################################################################################################## 股票价格
     price =  "%.2f" % doubleCloseArray[-1] + "_" + "%.2f" % doubleCloseArray[-2] + "_" + "%.2f" % doubleCloseArray[-3]
     # print("Price:" + price)
     ########################################################################################################## KDJ 指标
     # KDJ_K, KDJ_D, KDJ_J, KDJ_J_title = KDJ_zhibiao(data, doubleCloseArray)
     # print("KDJ_K:" + KDJ_K)
     # print("KDJ_D:" + KDJ_D)
     # print("KDJ_J:" + KDJ_J)
     ########################################################################################################## MACD 指标
     MACD_title = MACD_zhibiao(doubleCloseArray)
     ########################################################################################################## BULL 指标
     upperband, middleband, lowerband, BULL_title, BULL_middleband = BULL_zhibiao(doubleCloseArray, closeArray, lowArray)
     # print("上沿：" + upperband)
     # print("中线：" + middleband)
     # print("下沿：" + lowerband)
     ########################################################################################################## 均线指标
     MA20_titile, MA30_titile, MA60_titile, qushi_5_10_20_30 = junxian_zhibiao(doubleCloseArray, doubleOpenArray)
     # 指标返回
     return price, MA20_titile, MA30_titile, MA60_titile, qushi_5_10_20_30, MACD_title, BULL_title, BULL_middleband

# price, MA20_titile, MA30_titile, MA60_titile, qushi_5_10_20_30, MACD_title, BULL_title, BULL_middleband = zhibiao("BTC/USDT","30m")
