def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import time
import logging
import absl.logging
import investpy
logging.root.removeHandler(absl.logging._absl_handler)
absl.logging._warn_preinit_stderr = False
logging.basicConfig(filename='log.txt', filemode='w', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO, format='%(asctime)-15s %(message)s')
logging.info('logs to file, as expected')
from iqoptionapi.stable_api import IQ_Option
seating=str(input('input REAL?PRACTIC'))
API = IQ_Option("rashedhasanai@gmail.com","rostugbot007")
API.connect()
API.change_balance(seating) # PRACTICE / REAL
while True:
    if API.check_connect() == False:
    	print('Erro ao se conectar')
    	API.connect()
    else:
    	print('Conectado com sucesso')
    	break



def buyoption(forecast,actual,instrument):
  if forecast[0]>=actual[0]:
    status,id = API.buy(200,instrument,'put',1)
  elif forecast[0]<=actual[0]:
    status,id = API.buy(200,instrument,'call',1)
  else:
    None
s=investpy.get_calendar('GMT +6:00','time_only',None,['high'],None,None,None)
try:
    print(s['currency'],s['previous'],s['actual'],s['forecast'])
except:
    None
instrument=str(input("Input instrument"))
i=int(input("cordinate"))
while True:
  s=investpy.get_calendar('GMT +6:00','time_only',None,['high'],None,None,None)
  fore=s['forecast'][i]
  act=s['actual'][i]
  if fore!=None and act!=None:
    newstr = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in fore)
    forecast= [float(i) for i in newstr.split()]
    print(forecast)
    newstr = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in act)
    actual= [float(i) for i in newstr.split()]
    print(actual)
    buyoption(forecast,actual,instrument)
    break
  else:
    None
