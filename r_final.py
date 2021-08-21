def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import pandas as pd
import datetime
import time
import logging
import json
 
import absl.logging
import numpy as np
logging.root.removeHandler(absl.logging._absl_handler)
absl.logging._warn_preinit_stderr = False
logging.basicConfig(filename='log.txt', filemode='w', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO,
                    format='%(asctime)-15s %(message)s')
logging.info('logs to file, as expected')
from iqoptionapi.stable_api import IQ_Option
 
API = IQ_Option('amazingalim@gmail.com', 'Googlesaibot4356@@')
API.connect()
API.change_balance('PRACTICE')  # PRACTICE / REAL
 
while True:
    if API.check_connect() == False:
        print('Erro ao se conectar')
        API.connect()
    else:
        print('Conectado com sucesso')
        break
 
 
#Relative Strength Index  
def rsiFunc(prices, n=14):
 
    deltas = np.diff(prices)
 
    seed = deltas[:n+1]
 
    up = seed[seed>=0].sum()/n
 
    down = -seed[seed<0].sum()/n
 
    rs = up/down
 
    rsi = np.zeros_like(prices)
 
    rsi[:n] = 100. - 100./(1.+rs)
 
 
 
    for i in range(n, len(prices)):
 
        delta = deltas[i-1] # cause the diff is 1 shorter
 
 
 
        if delta>0:
 
            upval = delta
 
            downval = 0.
 
        else:
 
            upval = 0.
 
            downval = -delta
 
 
 
        up = (up*(n-1) + upval)/n
 
        down = (down*(n-1) + downval)/n
 
 
 
        rs = up/down
 
        rsi[i] = 100. - 100./(1.+rs)
 
 
 
    return rsi
 
instrument_type="cfd"
#instrument_id="BTCUSD"
side="buy"#input:"buy"/"sell"
amount=1.23#input how many Amount you want to play
 
#"leverage"="Multiplier"
leverage=3#you can get more information in get_available_leverages()
 
type="market"#input:"market"/"limit"/"stop"
 
#for type="limit"/"stop"
 
# only working by set type="limit"
limit_price=None#input:None/value(float/int)
 
# only working by set type="stop"
stop_price=None#input:None/value(float/int)
 
#"percent"=Profit Percentage
#"price"=Asset Price
#"diff"=Profit in Money
 
stop_lose_kind="percent"#input:None/"price"/"diff"/"percent"
stop_lose_value=5#input:None/value(float/int)
 
take_profit_kind="percent"#input:None/"price"/"diff"/"percent"
take_profit_value=10#input:None/value(float/int)
 
#"use_trail_stop"="Trailing Stop"
use_trail_stop=True#True/False
 
#"auto_margin_call"="Use Balance to Keep Position Open"
auto_margin_call=False#True/False
#if you want "take_profit_kind"&
#            "take_profit_value"&
#            "stop_lose_kind"&
#            "stop_lose_value" all being "Not Set","auto_margin_call" need to set:True
 
use_token_for_commission=False#True/False
 
# data load
def data(t,ins,nums):
    end_from_time = time.time()
    data = API.get_candles(ins, t, nums, end_from_time)
 
    candles = pd.DataFrame(data,
                           columns=['id', 'from', 'at', 'to', 'open', 'close', 'min', 'max', 'volume'])
    candles.columns = ['id', 'from', 'at', 'to', 'open', 'Close', 'Low', 'High', 'volume']
    return candles
 
 
def supres(low, high, min_touches=3, stat_likeness_percent=1.5, bounce_percent=5):
    """Support and Resistance Testing
    Identifies support and resistance levels of provided price action data.
    Args:
        low(pandas.Series): A pandas Series of lows from price action data.
        high(pandas.Series): A pandas Series of highs from price action data.
        min_touches(int): Minimum # of touches for established S&R.
        stat_likeness_percent(int/float): Acceptable margin of error for level.
        bounce_percent(int/float): Percent of price action for established bounce.
    ** Note **
        If you want to calculate support and resistance without regard for
        candle shadows, pass close values for both low and high.
    Returns:
        sup(float): Established level of support or None (if no level)
        res(float): Established level of resistance or None (if no level)
    """
    # Setting default values for support and resistance to None
    sup = None
    res = None
 
    # Identifying local high and local low
    maxima = high.max()
    minima = low.min()
 
    # Calculating distance between max and min (total price movement)
    move_range = maxima - minima
 
    # Calculating bounce distance and allowable margin of error for likeness
    move_allowance = move_range * (stat_likeness_percent / 100)
    bounce_distance = move_range * (bounce_percent / 100)
 
    # Test resistance by iterating through data to check for touches delimited by bounces
    touchdown = 0
    awaiting_bounce = False
    for x in range(0, len(high)):
        if abs(maxima - high[x]) < move_allowance and not awaiting_bounce:
            touchdown = touchdown + 1
            awaiting_bounce = True
        elif abs(maxima - high[x]) > bounce_distance:
            awaiting_bounce = False
    if touchdown >= min_touches:
        res = maxima
 
    # Test support by iterating through data to check for touches delimited by bounces
    touchdown = 0
    awaiting_bounce = False
    for x in range(0, len(low)):
        if abs(low[x] - minima) < move_allowance and not awaiting_bounce:
            touchdown = touchdown + 1
            awaiting_bounce = True
        elif abs(low[x] - minima) > bounce_distance:
            awaiting_bounce = False
    if touchdown >= min_touches:
        sup = minima
    return sup, res
 
 
 
 
 
current_value1=API.get_balance()
current_value2=0
def take_lov():
  while True:
      instrument1 = ["AMAZON","APPLE","BAIDU","CISCO","FACEBOOK","GOOGLE","INTEL","MSFT","YAHOO","AIG","CITI","COKE","GE","GM","GS","JPM","MCDON","MORSTAN","TWITTER","FERRARI","TESLA","USDNOK","MMM:US"]
      y={}
      y1 = json.dumps(y)
      # parsing JSON string:
      z = json.loads(y1)
      instrument=[]
      for i in range(len(instrument1)):
          instruments = instrument1.copy()
          ALL_Asset=API.get_all_open_time()
          print(ALL_Asset["cfd"][instruments[i]]["open"])
          if ALL_Asset["cfd"][instruments[i]]["open"]==True:
            df = data(60, instruments[i],700)
            a = supres(df['Low'], df['High'], min_touches=2, stat_likeness_percent=5, bounce_percent=5)
  
            x1={
                ""+str(instruments[i]):{"support":a[0],"resistance":a[1]}
            }
            z.update(x1)
            print(x1)
            instrument.append(instruments[i])
          else:
            None
          t1 = time.localtime(time.time())
          t1 = t1[3] * 60 + t1[4]
          t2 = 0
          j = 0
      print(instrument)
      print(z)
      p = json.dumps(z)
      p = json.loads(p)
      while (t2 - t1 <= 15):
          end_from_time = time.time()
          d = API.get_candles(instrument[j], 1, 1, end_from_time)
          d =d[0]['close']
          #print(d)
          current_value2=API.get_balance()
          rs=data(86400,instrument[j],20)
          rsi=rsiFunc(rs['Close'].tail(14), n=14)
          print(instrument[j],rsi[13])
          #trend=trendline(index,rs['Close'].tail(6), order=1)
          if p[''+instrument[j]]['support'] != None:
              if d<=p[''+instrument[j]]['support'] and rsi[13]>50:
                  print('this instrument',instrument[j])
                  check,order_id=I_want_money.buy_order(instrument_type=instrument_type, instrument_id=instrument[j],
                  side=side, amount=amount,leverage=leverage,
                  type=type,limit_price=limit_price, stop_price=stop_price,
                  stop_lose_value=stop_lose_value, stop_lose_kind=stop_lose_kind,
                  take_profit_value=take_profit_value, take_profit_kind=take_profit_kind,
                  use_trail_stop=use_trail_stop, auto_margin_call=auto_margin_call,
                  use_token_for_commission=use_token_for_commission)
          if p[''+instrument[j]]['resistance'] != None:
              if d>=p[''+instrument[j]]['resistance'] and rsi[13]<50:
                  print('this instrument',instrument[j])
                  check,order_id=I_want_money.buy_order(instrument_type=instrument_type, instrument_id=instrument[j],
                  side=side, amount=amount,leverage=leverage,
                  type=type,limit_price=limit_price, stop_price=stop_price,
                  stop_lose_value=stop_lose_value, stop_lose_kind=stop_lose_kind,
                  take_profit_value=take_profit_value, take_profit_kind=take_profit_kind,
                  use_trail_stop=use_trail_stop, auto_margin_call=auto_margin_call,
                  use_token_for_commission=use_token_for_commission)
                  
          j = j+1
          if j == len(instrument)-1:
              j = 0
          t2 = time.localtime(time.time())
          t2 = t2[3] * 60 + t2[4]
  
      else:
        None
take_lov()
