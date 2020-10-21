  
def candle_score(lst_0,lst_1,lst_2):    
    
    O_0,H_0,L_0,C_0=lst_0['open'],lst_0['max'],lst_0['min'],lst_0['close']
    O_1,H_1,L_1,C_1=lst_1['open'],lst_1['max'],lst_1['min'],lst_1['close']
    O_2,H_2,L_2,C_2=lst_2['open'],lst_2['max'],lst_2['min'],lst_2['close']
    
    DojiSize = 0.1
    
    
   
    bearish_harami=(C_1 > O_1) & (O_0 > C_0) & (O_0 <= C_1) & (O_1 <= C_0) & ((O_0 - C_0) < (C_1 - O_1 ))
    
    Bullish_Harami=(O_1 > C_1) & (C_0 > O_0) & (C_0 <= O_1) & (C_1 <= O_0) & ((C_0 - O_0) < (O_1 - C_1))
    
   

    strCandle=''
    candle_score=0
    
    if    bearish_harami:
        strCandle=strCandle+'/ '+'bearish_harami'
        candle_score=candle_score-1
    if    Bullish_Harami:
        strCandle=strCandle+'/ '+'Bullish_Harami'
        candle_score=candle_score+1
    return candle_score,strCandle
