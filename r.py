
import pandas as pd
from tapy import Indicators
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 00:14:46 2020

@author: Rashed
"""
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import time
import logging
import absl.logging
logging.root.removeHandler(absl.logging._absl_handler)
absl.logging._warn_preinit_stderr = False
logging.basicConfig(filename='log.txt', filemode='w', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO, format='%(asctime)-15s %(message)s')
logging.info('logs to file, as expected')
from iqoptionapi.stable_api import IQ_Option

API = IQ_Option("rashedhasanai@gmail.com","rostugbot007")
API.connect()
API.change_balance('PRACTICE') # PRACTICE / REAL
while True:
    if API.check_connect() == False:
    	print('Erro ao se conectar')
    	API.connect()
    else:
    	print('Conectado com sucesso')
    	break


def data(t,ins,r):
    end_from_time=time.time()
    data=API.get_candles(ins,t,200, end_from_time)

    candles= pd.DataFrame(data,
                          columns=['id', 'from','at','to','open','close','min','max','volume'])
    candles.columns = ['id', 'from', 'at', 'to', 'open', 'Close', 'Low', 'High','volume']
    candles=candles.tail(r)
    return candles

res1=['loose']
money=[70,126,226,407]
def multiply(res1,money):
    if res1[len(res1)-1]=='loose':
        return 70
    elif res1[len(res1)-1]=='win':
        i=len(res1)-1
        count=0
        while True:
            if res1[i]=='loose':
                break
            elif res1[i]=='win':
                count=count+1
            i=i-1
        return money[count]
  
def check(a,inst):
    status,id = API.buy(multiply(res1,money),inst,a,1)
    p=API.check_win_v3(id)
    print(p)
    if p>0:
      res1.append('win')
    elif p<0:
      res1.append('loose')
      status,id = API.buy(multiply(res1,money),inst,a,1)
      p=API.check_win_v3(id)
    else:
      None
    return p


#find out market
final=["EURUSD","USDJPY","AUDJPY","AUDUSD","CADCHF","GBPCAD","EURCHF","EURCAD","GBPAUD","GBPNZD","AUDCHF","EURAUD","EURNZD","USDSGD","EURJPY","EURGBP","USDCHF","AUDCAD"]

signal={""}
n=0
while True:
    df =data(60,"EURUSD",200)
    indicators = Indicators(df)
    a=indicators.awesome_oscillator(column_name='ao')
    b=indicators.ema(period=100, column_name='ema')
    df = indicators.df
    if df['ao'][len(df)-2]>=0:
        print(df['ao'][len(df)-2],df['ema'][len(df)-2],df['Close'][len(df)-2],"UP")
        check('call',"EURUSD")
    elif df['ao'][len(df)-2]<=0:
        print(df['ao'][len(df)-2],df['ema'][len(df)-2],df['Close'][len(df)-2],"Down")
        check('put',"EURUSD")
    else:
        print(final[n])
    #print(df['ao'][len(df)-2],df['ema'][len(df)-2],df['Close'][len(df)-2],"ok")
    
        
        
        
