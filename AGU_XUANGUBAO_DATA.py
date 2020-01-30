#encoding=utf-8
import pandas as pd
import time
import numpy as num
import tushare as ts
import talib as ta
from email_util import *
import common
import common_image
import common_zhibiao
import common_mysqlUtil

def strategy():
    # 获取实时数据
    data = common_mysqlUtil.select_xuangubao()
    # 数据遍历
    for i in range(len(data)):
        code = str(data[i][0])
        name = str(data[i][1])
        df = common.daily_basic(code)
        # 判断DataFrame是否为空
        if df.empty:
            continue
        # 总市值
        total_mv = num.array(df['total_mv'])
        # 市盈率
        pe = num.array(df['pe'])

        if pe[0] is None:
            pe[0] = 0.0
        # 换手率
        turnover_rate = num.array(df['turnover_rate'])
        # 名称
        time.sleep(1)
        name = common.codeName(code)
        time.sleep(1)
        eps, epsup, yingyeup, eps_2, epsup_2, yingyeup_2 = common.codeEPS(code)
        common_mysqlUtil.update_xuangubao(name, "%.2f" % (total_mv / 10000), "%.2f" % pe, "%.2f" % turnover_rate, code, "%.2f" % epsup, "%.2f" % yingyeup)
        time.sleep(1)

def strategy_all_code():
    # 获取实时数据
    data = common_mysqlUtil.select_all_code()
    # 数据遍历
    for i in range(len(data)):
        code = str(data[i][0])
        name = str(data[i][1])
        df = common.daily_basic(code)
        # 判断DataFrame是否为空
        if df.empty:
            continue
        # 总市值
        total_mv = num.array(df['total_mv'])
        # 市盈率
        pe = num.array(df['pe'])

        if pe[0] is None:
            pe[0] = 0.0
        # 换手率
        turnover_rate = num.array(df['turnover_rate'])
        # 名称
        time.sleep(1)
        name = common.codeName(code)
        time.sleep(1)
        eps, epsup, yingyeup, eps_2, epsup_2, yingyeup_2 = common.codeEPS(code)
        common_mysqlUtil.update_all_code(name, "%.2f" % (total_mv / 10000), "%.2f" % pe, "%.2f" % turnover_rate, code, "%.2f" % epsup, "%.2f" % yingyeup)
        time.sleep(1)

# strategy()
strategy_all_code()