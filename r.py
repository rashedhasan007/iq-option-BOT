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
    data=API.get_candles(ins,t,r, end_from_time)

    candles= pd.DataFrame(data,
                          columns=['id', 'from','at','to','open','close','min','max','volume'])
    candles.columns = ['id', 'from', 'at', 'to', 'open', 'Close', 'Low', 'High','volume']
    return candles

res1=['loose']
money=[70,126,226,70,570]
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
        if len(money)==count:
          return 70
        else:
          return money[count]
  
def check(a,inst):
    status,id = API.buy(multiply(res1,money),inst,a,1)
    p=API.check_win_v3(id)
    if p>0:
      res1.append('win')
    elif p<0:
      res1.append('loose')
      #status,id = API.buy(multiply(res1,money),inst,a,1)
      #p=API.check_win_v3(id)
    else:
      None
    return p


#find out market
final=["EURUSD","USDJPY","AUDJPY","AUDUSD","CADCHF","GBPCAD","EURCHF","EURCAD","GBPAUD","GBPNZD","AUDCHF","EURAUD","EURNZD","USDSGD","EURJPY","EURGBP","USDCHF","AUDCAD"]

signal={""}
def candle_s(df):
  if df['Close'][len(df)-2]>df['Close'][len(df)-3]:
    r=1
    return r
  elif df['Close'][len(df)-2]<df['Close'][len(df)-3]:
    r=0
    return r
  else:
    None
n=0
end_from_time=time.time()
start1=API.get_candles("EURUSD",60,2, end_from_time)
while True:
  end_from_time=time.time()
  start2=API.get_candles("EURUSD",60,2, end_from_time)
  if start2[1]['id']>start1[1]['id']:
    break
while True:
    time.sleep(2)
    df =data(60,"EURUSD",200)
    indicators = Indicators(df)
    a=indicators.awesome_oscillator(column_name='ao')
    df = indicators.df
    df1 =data(60,"EURUSD",5)
    if df['ao'][len(df)-1]>=0 and (df1['Close'][len(df1)-2]>df1['Close'][len(df1)-3]):
      while True:
        status,id = API.buy(multiply(res1,money),'EURUSD','call',1)
        p1=API.check_win_v3(id)
        if p1>=0:
          res1.append('win')
        elif p1==-70:
          status,id = API.buy(70,'EURUSD','call',1)
          API.check_win_v3(id)
          break
        else:
          res1.append('loose')
          break
      print('break')
    elif df['ao'][len(df)-1]<=0 and (df1['Close'][len(df1)-2]<df1['Close'][len(df1)-3]):
      while True:
        status,id = API.buy(multiply(res1,money),'EURUSD','put',1)
        p2=API.check_win_v3(id)
        if p2>=0:
          res1.append('win')
        elif p2==-70:
          status,id = API.buy(70,'EURUSD','put',1)
          API.check_win_v3(id)
          break
        else:
          res1.append('loose')
          break
      print('break')
    else:
        None
    #print(df['ao'][len(df)-2],df['ema'][len(df)-2],df['Close'][len(df)-2],"ok")
    print(df['ao'][len(df)-1],candle_s(data(60,"EURUSD-OTC",5)))
    
        
        
