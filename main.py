'''
This is a program in which a user will enter their cryptocurrency portfolio with amounts,
and then this portfolio will tell you what your portfolio would be valued at if every coin
returned to its ATH! 
Written by Jett Black
The University of New Mexico 
'''
import requests 
import json 
import math 
COINGECKO_URL = 'https://api.coingecko.com/api/v3/' ## constant to hold the api link to coingecko's website, will add different substrings to call to get different data later 

######### MAKING CALL TO API TO GET JSON OF ALL COINS #############

coinlist_params = {'vs_currency' : 'usd'}
coinlist_url = COINGECKO_URL + "coins/list" ## variable to hold the api call to get list of coins from coingecko's website 
response = requests.get(coinlist_url,params=coinlist_params) ## variable to store response from API call for coin list 
if response.status_code == 200 : ## if the call is successful
    coin_list_data = json.loads(response.content) ## place the data from response into a json.loads object 
   
else : ## if call is not successful 
    print(f"Error: {response.status_code}") ## print the error code 

###################################################################

############### PLACING COIN TICKERS INTO A LIST ##################

coin_tickers_list = []
for coin_data in coin_list_data :
    coin_tickers_list.append(coin_data['symbol'])

###################################################################

############## GETTING PORTFOLIO AND AMOUNT #######################

print("Here you will enter each of your crypto holdings along with amounts") ## informs user of what they will be entering 

portfolio = {} ## dictionary to hold portfolio, key will be coin ticker and value will be amount held 

while True : ## while loop in case there are multiple coins

    coin = input("Please enter the ticker for your coin. For example, if entering bitcoin you will enter 'BTC'. If done entering, press SPACE and enter: ").upper() ## variable to store ticker 

    if coin == ' ' : ## if space bar was entered, user is done entering coins so break loop 
        break
    elif coin.lower() not in coin_tickers_list : ## checks if coin exists, or user entered ticker incorrectly 
        print("Coin ticker not recognized, please try again")
        continue
    
    amount = float(input("Now enter amount of coin: ").replace(',','')) ## if entered correctly, take amont of coin held 

    coin_info = [] 

    for coin_data in coin_list_data :
        if coin.lower() == coin_data['symbol'] :
            if 'peg' in coin_data['id'] :
                continue
            coin_info.append(coin_data['symbol'])
            coin_info.append(amount)
            portfolio[coin_data['id']] = coin_info
            break 
        
print(portfolio)
        

wagmi_amount = 0

for coin in portfolio :
    coin_history_params = {"id" : coin,
    }
    coin_history_url = COINGECKO_URL + f"/coins/{coin}"
    response = requests.get(coin_history_url,params=coin_history_params)
    if response.status_code == 200 : ## if the call is successful
        coin_history_data = json.loads(response.content) ## place the data from response into a json.loads object 
        ath = float(coin_history_data['market_data']['ath']['usd'])
    else : ## if call is not successful 
        print(f"Error: {response.status_code}") ## print the error code 
    wagmi_amount += (portfolio[coin][1] * ath)
    
print(f"Price of youyr portfolio if every coin returned to its all time high: ${math.floor(wagmi_amount)}.00")
  

