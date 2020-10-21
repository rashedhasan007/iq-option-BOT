def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import time
import logging
import candle1
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
    
    
    
def check(a):
    M=multiply(res1,money)
    status,id = API.buy(M,"EURUSD",a,1)
    p=API.check_win_v3(id)
    print(p)
    if p>0:
        res1.append('win')
    elif p<0:
        res1.append('loose')
        time.sleep(900)
    else:
        None
    return p
    
def res_len(res):
    if len(res)==7:
        res.remove(res[1])
    else:
        None
i1=API.get_candles("EURUSD",60,1,time.time())[0]['id']
while True:
    end_from_time=time.time()
    dat=API.get_candles("EURUSD",60,1,time.time())[0]
    i=dat['id']
    if i>i1:
        print("start")
        break
 
            
total=[]        
    
while True:
    end_from_time=time.time()
    data=API.get_candles("EURUSD",60,5, end_from_time)
    l=data
    res_len(res1)
    try:
        t=candle1.candle_score(l[3],l[2],l[1])[0]
    except:
        None
    if t>0:
        v=check("call")
        total.append(v)
        print(candle1.candle_score(l[3],l[2],l[1]),v)
        print(sum(total))
        time.sleep(5)
    elif t<0:
        v1=check("put")
        total.append(v1)
        print(candle1.candle_score(l[3],l[2],l[1]),v1)
        print(sum(total))
        time.sleep(5)
    else :
        None
            
            
            
            
            
            
            
            
            
            
            
            