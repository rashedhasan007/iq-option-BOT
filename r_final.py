def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import pandas as pd
import datetime
import time
import logging
import json
import schedule
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



def binary(direcao, par):
    try:
        id = API.buy(1, par, direcao,2)
    except:
        None
    return id


def multiply(res1,money1,money2,current_money):
    if res1[len(res1) - 1] == 'start':
        return current_money
    elif res1[len(res1) - 1] == 'loose':
        i = len(res1) - 1
        count = 0
        while True:
            if res1[i] == 'win' or res1[i] == 'start':
                break
            elif res1[i] == 'loose':
                count = count + 1
            i = i - 1
        if count >= len(money2):
            res1[i] == 'loose'
            return current_money
        else:
            return money2[count]
    elif res1[len(res1)-1]=='win':
        i=len(res1)-1
        count=0
        while True:
            if res1[i]=='loose' or res1[i] == 'start':
                break
            elif res1[i]=='win':
                count=count+1
            i=i-1
        if count>=len(money1):
          res1[i]=='loose'
          return current_money
        else:
          return money1[count]

#print(multiply(res1,money1,money2))

def checker(a, j, instrument,res1,money1,money2,current_money,loss_count):
    ALL_Asset=API.get_all_open_time()
    #check if open or not
    if ALL_Asset["turbo"][instrument[j]]["open"]==True:
        status,id = API.buy(multiply(res1,money1,money2,current_money),instrument[j],a, 5)
        bo = API.check_win_v3(id)
        print(bo)
        if bo < 0:
            instrument.remove(instrument[j])
            res1.append("loose")
            loss_count.append('loose')
        elif bo>0:
            res1.append("win")
            instrument.remove(instrument[j])
        else:
            None

current_value1=API.get_balance()
current_value2=0
def rani_take_lov():
  current_value2=0
  print('start')
  res1=['start']
  loss_count=[]
  current_money1=API.get_balance()
  current_money1=int( current_money1)
  current_money=current_money1*.028
  money1=[current_money,current_money+current_money*.12,current_money+current_money*.24]
  money2=[current_money,current_money/.80,(current_money/.80+current_money)/.80]
  while True:
      instrument1 = ["EURUSD", "AUDJPY", "USDJPY","AUDUSD","EURJPY","GBPUSD","EURNZD","EURGBP","GBPCAD","EURCAD","GBPAUD","GBPJPY"]
      y={}
      y1 = json.dumps(y)
      # parsing JSON string:
      z = json.loads(y1)
      for i in range(len(instrument1)):
          instrument = instrument1.copy()
          df = data(60, instrument[i],700)
          a = supres(df['Low'], df['High'], min_touches=2, stat_likeness_percent=5, bounce_percent=5)

          x1={
              ""+str(instrument[i]):{"support":a[0],"resistance":a[1]}
          }
          z.update(x1)
          t1 = time.localtime(time.time())
          t1 = t1[3] * 60 + t1[4]
          t2 = 0
          j = 0
          print(x1)
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
                  checker('call', j, instrument,res1,money1,money2,current_money,loss_count)
                  print('done')
          if p[''+instrument[j]]['resistance'] != None:
              if d>=p[''+instrument[j]]['resistance'] and rsi[13]<50:
                  print('this instrument',instrument[j])
                  checker('put', j, instrument,res1,money1,money2,current_money,loss_count)
                  print('done')
          j = j+1
          if j == len(instrument)-1:
              j = 0
          t2 = time.localtime(time.time())
          t2 = t2[3] * 60 + t2[4]
      if current_value2-current_value1>=1.5*current_money:
        print('today finished')
        break
      elif len(loss_count)>=2:
        print('today finished')
        break
      else:
        None
  
schedule.every().sunday.at("15:30").do(rani_take_lov)
schedule.every().monday.at("13:15").do(rani_take_lov)
schedule.every().wednesday.at("07:50").do(rani_take_lov)
schedule.every().thursday.at("08:32").do(rani_take_lov)
schedule.every().friday.at("1:55").do(rani_take_lov)
while True:
    schedule.run_pending()
    time.sleep(1)
