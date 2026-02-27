---
title: Binance Trading Robot
description: Create a Binance Trading Robot.
categories: [Finance, Crypto]
tags: [Crypto, Binance, Trading, Rest API]
layout: post
toc: true
---

> Disclaimer: I do not provide personal investment advice and I am not a qualified licensed investment advisor. The information provided may include errors or inaccuracies. Conduct your own due diligence, or consult a licensed financial advisor or broker before making any and all investment decisions. Any investments, trades, speculations, or decisions made on the basis of any information found on this site and/or script, expressed or implied herein, are committed at your own risk, financial or otherwise. No representations or warranties are made with respect to the accuracy or completeness of the content of this entire site and/or script, including any links to other sites and/or scripts. The content of this site and/or script is for informational purposes only and is of general nature. You bear all risks associated with the use of the site and/or script and content, including without limitation, any reliance on the accuracy, completeness or usefulness of any content available on the site and/or script. Use at your own risk.
{: .prompt-danger }

![jorgem0/binance-trading-robot](/assets/img/GitHub_Lockup_Black.svg){: .light width="100" height="100" }
![jorgem0/binance-trading-robot](/assets/img/GitHub_Lockup_White.svg){: .dark width="100" height="100" }
_<a href="https://github.com/jorgem0/binance-trading-robot" target="_blank" rel="noopener noreferrer">jorgem0/binance-trading-robot</a>_

## Introduction

This tutorial will show the reader how to set up a Binance Trading Robot. The robot is written in Python and uses the [Binance REST API](https://github.com/binance-us/binance-official-api-docs/blob/master/rest-api.md){:target="_blank" rel="noopener noreferrer"} to communicate with Binance's trading platform. [**RE**presentational **S**tate **T**ransfer (REST)](https://www.codecademy.com/article/what-is-rest){:target="_blank" rel="noopener noreferrer"} is a standardized architecture for systems to communicate with one another. An [Application Programming Interface (API)](https://www.redhat.com/en/topics/api/what-are-application-programming-interfaces){:target="_blank" rel="noopener noreferrer"} is a method for systems to communicate with one another. Therefore, a [REST API](https://www.redhat.com/en/topics/api/what-is-a-rest-api){:target="_blank" rel="noopener noreferrer"} is an API that adheres to the REST architecture. We will use the Python library [`requests`](https://docs.python-requests.org/en/latest/){:target="_blank" rel="noopener noreferrer"} to communicate with the Binance REST API. This will allow us (clients) to send `get` and `post` requests to Binance (servers) which will send back responses that contain account information and trade confirmations.

This Binance Trading Robot runs continuously in a `while True:` loop. The trading robot has four functions that are called upon in the while loop: `current_price()` (checks current price for selected symbol pair), `account_balance()` (checks account balance for selected symbol pair), `latest_transaction()` (checks latest transaction for selected symbol pair), and `submit_order()` (submits order for selected symbol pair). The robot submits market orders and its logic can be seen below.

1. Checks account balance `account_balance()` to see how much of the symbol pair is free to trade
2. Checks latest transaction `latest_transaction()` for the symbol pair to see the price it was traded at
3. Calculates buy/sell price for the next trade based on the latest transaction price
4. Submits order `submit_order()` to trade all available free asset if buy/sell price is met based on current price of symbol pair
5. Wait for a designated amount of time and go back to Step 1.

> The function `submit_order()` can be commented out in the while loop to avoid submitting an order to first understand the logic of the bot.
{: .prompt-warning }

## Importing Libraries and Keys

The first thing that needs to be done is to import the necessary libraries. The `numpy`, `time`, and `datetime` libraries are imported for maths and creating some verification timestamps for the Binance Rest API. The `requests` library is used to communicate with the Binance Rest API while the `hmac` and `hashlib` libraries are used to hash the keys for authentication with the Binance Rest API. The `yaml` library safely imports the configuration file config.yml (which contains the keys to access the account) using the function `yaml.safe_load()` instead of a .py file since we don't want potential malicious code to run within the .py file. The `json` library prints the response data from the Binance Rest API request in a more human readable format in order to better understand the format of the returned data. A link to the Binance Rest API is included along with the **USE AT YOUR OWN RISK** Disclaimer that is also located at the top of this page.

The API and Secret Keys are then loaded from the config.yml file. The Binance tutorial on how to create a Binance Rest API key pair can be seen at [How to Create API Keys on Binance?](https://www.binance.com/en/support/faq/detail/360002502072){:target="_blank" rel="noopener noreferrer"}. The config.yml file should have the information and format below. Select the desired `symbol_pair` to trade and make sure `symbol_first` and `symbol_second` match accordingly.

> DO NOT SHARE THESE KEYS WITH ANYBODY!!! This is how access to the account is granted.
{: .prompt-danger }

```yaml
apikey: 'API_KEY_HERE'
secretkey: 'SECRET_KEY_HERE'
```
{: file="config.yml" }

```python
import numpy as np
import time
from datetime import datetime, timezone, timedelta
import requests
import hmac
import hashlib
import yaml
import json


# Binance Rest API documentation
# https://github.com/binance-us/binance-official-api-docs/blob/master/rest-api.md
# Each url gets you slightly different information and has slightly different input params
# api/v3/exchangeInfo, api/v3/depth, api/v3/trades, etc...

# Disclaimer:
# I do not provide personal investment advice and I am not a qualified licensed investment advisor. 
# The information provided may include errors or inaccuracies. Conduct your own due diligence, or consult
# a licensed financial advisor or broker before making any and all investment decisions. Any investments, 
# trades, speculations, or decisions made on the basis of any information found on this site and/or script, 
# expressed or implied herein, are committed at your own risk, financial or otherwise. No representations 
# or warranties are made with respect to the accuracy or completeness of the content of this entire site 
# and/or script, including any links to other sites and/or scripts. The content of this site and/or script
# is for informational purposes only and is of general nature. You bear all risks associated with the use 
# of the site and/or script and content, including without limitation, any reliance on the accuracy, 
# completeness or usefulness of any content available on the site and/or script. Use at your own risk.


config = yaml.safe_load(open('config.yml')) # Load yaml file that has api and secret key

apikey=config['apikey'] # Api key from yaml file
secretkey=config['secretkey'] # Secret key from yaml file

symbol_pair='BNBBUSD' # Pair to trade
symbol_first='BNB' # Make sure this matches above
symbol_second='BUSD' # Make sure this matches above

```
{: file="binance_bot.py" }

## Current Price

The first of the four functions discussed in the Introduction section is the `current_price()` function. This function calls the Binance Rest API [ticker/price](https://github.com/binance-us/binance-official-api-docs/blob/master/rest-api.md#symbol-price-ticker){:target="_blank" rel="noopener noreferrer"} endpoint by passing in the endpoint url `urlcp` and parameters `paramscp` to the `requests.get()` method (which is from the `requests` library) to get the ticker price. A [response](https://restfulapi.net/http-status-codes/){:target="_blank" rel="noopener noreferrer"} of `<Response [200]>` signifies a successful request. We convert the response from the Binance Rest API to the json format to extract the necessary data as a Python dictionary. The `current_price()` function returns the current price `cp` of the `symbol_pair` that will be used to calculate the buy/sell price to decide if the trade should be executed. The pretty print version of the response in json format can be seen below. This is useful as it allows the user to understand the format of the data in order to extract the necessary information.

```python
def current_price():

	#################################
	##### Ticker price endpoint #####
	#################################
	urlcp='https://api.binance.us/api/v3/ticker/price'


	paramscp={'symbol':symbol_pair} # Ticker wanted
	response_cp = requests.get(urlcp, params=paramscp) # Sending GET request for ticker information
	# print(response_cp) # Returns HTTP Status, a value of 200 (OK) means no error

	pair_info = response_cp.json() # Convert response to JSON object for data extraction
	# print(json.dumps(pair_info, indent=4)) # Pretty print to understand structure of data
	cp = pair_info['price'] # Current price of symbol


	print('--------------------Current Price--------------------')
	print(f'{symbol_pair} Current Price: {cp}')
	print('\n')

	return cp


```
{: file="binance_bot.py" }

```python
>>> print(response_cp)

	<Response [200]>

>>> print(json.dumps(pair_info, indent=4))

	{
		"symbol": "BNBBUSD",
		"price": "411.13100000"
	}
```

## Account Balance

The next function is the `account_balance()` function which calls the Binance Rest API [account](https://github.com/binance-us/binance-official-api-docs/blob/master/rest-api.md#account-information-user_data){:target="_blank" rel="noopener noreferrer"} endpoint to acquire the `symbol_pair` account balance. The endpoint url `urlcp` and parameters `paramscp` are passed to the `requests.get()` function in a slightly different manner since we are now using the generated keys to get specific account information.

> Again: DO NOT SHARE THESE WITH ANYBODY!!! This is how access to the account is granted.
{: .prompt-danger }

A timestamp in milliseconds is created for this request since the Binance Rest API has [timing security](https://github.com/binance-us/binance-official-api-docs/blob/master/rest-api.md#timing-security){:target="_blank" rel="noopener noreferrer"} to ensure communication can only happen within a small window of time. The `hmac` (Hashing for Message Authentication) library hashes the secret key `secretkey` with Secure Hash Algorithm 256-bit (SHA-256) using the `hash` library to create an authentication `signature` for the API. The `url`, `queryString` (which contains the parameters), `signature`, and api key `apikey` are all passed to the `requests.get()` function to 'get' the account balance.

If we take a look at the pretty print version of the response in json format below, we can start extracting some key information now that we know how the response data looks like. We want to extract how much of each asset in the `symbol_pair` we have free to trade. The `balances` key in the response dictionary has a list of assets and how much of each are free to trade or [locked](https://support.binance.us/en/articles/9842883-why-is-a-portion-of-my-balance-unable-to-be-withdrawn-or-unavailable){:target="_blank" rel="noopener noreferrer"}. We want to extract the `symbol_pair` information but we can't get the value of the desired asset using the key:pair method since the value of the key `balances` is a list of dictionaries and not a dictionary itself so we cycle through the list until we get the index of the desired assets. We print some information regarding the account balance for the `symbol_pair` and return the `assetfree` and `assetfree2` variables. These variables contain the total amount of free assets in the `symbol_pair` that we can use to trade later on in the script.

```python
def account_balance():

	print('###############################################################')
	print('########################Account Balance########################')
	print('###############################################################')
	print('\n\n')

	########################################
	##### Account information endpoint #####
	########################################
	url = "https://api.binance.us/api/v3/account"


	# Creating datetime variable required for account connection
	now = datetime.now(timezone.utc) # current date
	epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)  # use POSIX epoch
	posix_timestamp_micros = (now - epoch) // timedelta(microseconds=1)
	posix_timestamp_millis = posix_timestamp_micros // 1000  # or `/ 1e3` for float

	# Input variables
	queryString = "timestamp=" + str(posix_timestamp_millis)
	# Creating hash for authentication
	signature = hmac.new(secretkey.encode(), queryString.encode(), hashlib.sha256).hexdigest()
	# Combining account information endpoint url with input variables and authentication hash
	url = url + f"?{queryString}&signature={signature}"

	# Sending GET request for account information
	response_ai = requests.get(url, headers={'X-MBX-APIKEY': apikey})

	# Convert response to JSON object for data extraction
	account_info=response_ai.json()
	# print(json.dumps(account_info, indent=4)) # Pretty print to understand structure of data


	# Can't call out the symbols directly because 'balances' is a list of dictionaries and not a dictionary
	# Cycle through the list of dictionaries containing the different assets
	for i, balance in enumerate(account_info['balances']):

		if balance['asset']==symbol_first: # Finding first symbol in symbol pair
			ifirst=i

		if balance['asset']==symbol_second: # Finding second symbol in symbol pair
			isecond=i

	# First asset information
	asset=account_info['balances'][ifirst]['asset'] # Asset name
	assetfree=account_info['balances'][ifirst]['free'] # Asset amount that is free to trade
	assetlocked=account_info['balances'][ifirst]['locked'] # Asset amount that is locked and can't be traded

	assetfreecp=float(assetfree)*float(cp) # Current price of asset that is free
	assetlockedcp=float(assetlocked)*float(cp) # Current price of asset that is locked

	# Printing information
	print(f'Asset: {asset}')
	print(f'Free: {assetfree} at {cp} = ${assetfreecp}' )
	print(f'Locked: {assetlocked} at {cp} = ${assetlockedcp}')
	print(f'Subtotal: $ {assetfreecp+assetlockedcp}')
	print(f'Subtotal: $ {assetfreecp+assetlockedcp}')
	print('\n')

	print('+')
	print('\n')

	# Second asset information
	asset2=account_info['balances'][isecond]['asset'] # Asset name
	assetfree2=account_info['balances'][isecond]['free'] # Asset amount that is free to trade
	assetlocked2=account_info['balances'][isecond]['locked'] # Asset amount that is locked and can't be traded

	# Printing information
	print(f'Asset: {asset2}')
	print(f'Free: {assetfree2}')
	print(f'Locked: {assetlocked2}')
	print(f'Subtotal: {float(assetfree2)+float(assetlocked2)}')
	print('\n')

	# Total net worth in account
	print('----------Total----------')
	print('$',assetfreecp+assetlockedcp+float(assetfree2)+float(assetlocked2))
	print('\n\n')

	print('###############################################################')
	print('########################Account Balance########################')
	print('###############################################################')
	print('\n')

	return assetfree, assetfree2


```
{: file="binance_bot.py" }

```python
>>> print(json.dumps(account_info, indent=4))

	{
		"makerCommission": 10,
		"takerCommission": 10,
		"buyerCommission": 0,
		"sellerCommission": 0,
		"canTrade": true,
		"canWithdraw": true,
		"canDeposit": true,
		"updateTime": ############,
		"accountType": "SPOT",
		"balances": [
			{
				"asset": "BTC",
				"free": "0.00000000",
				"locked": "0.00000000"
			},
			{
				"asset": "ETH",
				"free": "0.00000000",
				"locked": "0.00000000"
			},
			...,
			{
				"asset": "BNB",
				"free": "0.00000000",
				"locked": "0.00000000"
			},
			...,
			{
				"asset": "POLY",
				"free": "0.00000000",
				"locked": "0.00000000"
			}
		],
		"permissions": [
			"SPOT"
		]
	}
```

## Latest Transaction

The third function we have is the `latest_transaction()` function which calls the [myTrades](https://github.com/binance-us/binance-official-api-docs/blob/master/rest-api.md#account-trade-list-user_data){:target="_blank" rel="noopener noreferrer"} endpoint to see the user's latest transactions. Just like the account information endpoint in the last section, we pass in all the relevant parameters and key information to get access to the user's trade history. The response of the get request returns a list of dictionaries containing the latest 500 `symbol_pair` trades. However, we only want the latest trade `latest_transaction=trades[-1]` since this is what we base our trading criteria on. The function returns the price `tp_price` at which this latest transaction occurred and whether it was a buy or sell order `isBuyer`. The value of `isBuyer` refers to the first asset in the `symbol_pair`.

```python
def latest_transaction():

    ###################################
    ##### Account trades endpoint ##### 
    ###################################
    url = "https://api.binance.us/api/v3/myTrades"


    # Creating datetime variable required for account connection
    now = datetime.now(timezone.utc)
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)  # use POSIX epoch
    posix_timestamp_micros = (now - epoch) // timedelta(microseconds=1)
    posix_timestamp_millis = posix_timestamp_micros // 1000  # or `/ 1e3` for float

    # Input variables
    queryString = "symbol=" + symbol_pair + "&amp;timestamp=" + str(posix_timestamp_millis)
    # Creating hash for authentication
    signature = hmac.new(secretkey.encode(), queryString.encode(), hashlib.sha256).hexdigest()
    # Combining account information endpoint url with input variables and authentication hash
    url = url + f"?{queryString}&signature={signature}"

    # Sending GET request for account trades
    response_trades = requests.get(url, headers={'X-MBX-APIKEY': apikey})

    # Convert response to JSON object for data extraction
    trades=response_trades.json()
    # print(json.dumps(trades, indent=4)) # Pretty print to understand structure of data

    latest_transaction=trades[-1] # Latest transaction

    print('--------------------Latest Transaction--------------------')
    print('\n')

    tp=latest_transaction['symbol'] # Trading pair
    tp_price=latest_transaction['price'] # Trading pair price

    # Printing information
    print(f'Trading Pair: {tp}')
    print(f'Price: {tp_price}')
    print('\n')

    # Buy and Sell is for the first symbol of the trading pair
    # True is buy first symbol
    # False is sell first symbol
    isBuyer= latest_transaction['isBuyer']

    symbol_first_qty = latest_transaction['qty'] # First Symbol quantity
    symbol_second_qty = latest_transaction['quoteQty'] # Second Symbol quantity

    # Buy first symbol
    if isBuyer == True:

        print('BUY')
        print(f'{symbol_first} BOUGHT:  {symbol_first_qty}')
        print(f'{symbol_second} SOLD: {symbol_second_qty}')

    # Sell first symbol
    elif isBuyer == False:

        print('SELL')
        print(f'{symbol_first} SOLD:  {symbol_first_qty}')
        print(f'{symbol_second} BOUGHT: {symbol_second_qty}')
    print('\n')

    return tp_price, isBuyer


```
{: file="binance_bot.py" }

```python
>>> print(json.dumps(trades, indent=4))

	[
		{
			"symbol": "BNBBUSD",
			"id": ######,
			"orderId": ######,
			"orderListId": -1,
			"price": "######",
			"qty": "######",
			"quoteQty": "######",
			"commission": "######",
			"commissionAsset": "BUSD",
			"time": ######,
			"isBuyer": false,
			"isMaker": false,
			"isBestMatch": true
		},
		...,
		{
			"symbol": "BNBBUSD",
			"id": ######,
			"orderId": ######,
			"orderListId": -1,
			"price": "######",
			"qty": "######",
			"quoteQty": "######",
			"commission": "######",
			"commissionAsset": "BNB",
			"time": ######,
			"isBuyer": true,
			"isMaker": false,
			"isBestMatch": true
		}
	]
```

## Submit Order

The final function `submit_order()` uses the [order](https://github.com/binance-us/binance-official-api-docs/blob/master/rest-api.md#new-order--trade){:target="_blank" rel="noopener noreferrer"} endpoint to submit a buy or sell market order based on the `isBuyer` variable. This variable also determines the parameters we pass in to the `queryString`. 

> Binance also has a [dummy order endpoint](https://github.com/binance-us/binance-official-api-docs/blob/master/rest-api.md#test-new-order-trade){:target="_blank" rel="noopener noreferrer"} to practice submitting an order which will return a response of `<Response [200]>` if successful.
{: .prompt-info }

The `type` variable is set to `'MARKET'` as this script will submit a market order but other options are available. The `submit_order()` function will buy or sell the maximum amount of free assets available (`assetfree` and `assetfree2`) acquired from the `account_balance()` function. Note that this time we are using `requests.post()` rather than `requests.get()` (like all the previous functions) since we want to 'post' some data to the Binance Rest API in order to submit the order. The other functions were just 'getting' data that was already there to post process but this time we want to 'post' some data. An example of the pretty print response after submitting a successful order can be seen in the order endpoint documentation linked at the beginning of this section.

> The function `submit_order()` can be commented out in the while loop to avoid submitting an order to understand the logic of the bot.
{: .prompt-warning }

```python
def submit_order():

	##########################
	##### Order endpoint #####
	##########################
	url = "https://api.binance.us/api/v3/order"
	# url = "https://api.binance.us/api/v3/order/test" # Test url for dummy trades

	# Creating datetime variable required for account connection
	now = datetime.now(timezone.utc)
	epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)  # use POSIX epoch
	posix_timestamp_micros = (now - epoch) // timedelta(microseconds=1)
	posix_timestamp_millis = posix_timestamp_micros // 1000  # or `/ 1e3` for float

	# Input variables
	type='MARKET' # Order type

	if isBuyer == False:
		side='BUY' # Want to buy
		quoteOrderQty=str(symbol_second_avail) # How much second symbol you want to use to buy first symbol
		queryString = "symbol=" + symbol_pair + "&side=" + side + "&type=" + type + "&amp;quoteOrderQty=" + quoteOrderQty +  "&amp;timestamp=" + str(posix_timestamp_millis)

	elif isBuyer == True:
		side='SELL' # Want to sell
		quantity=str(symbol_first_avail) #how much first symbol you want to sell to buy second symbol
		queryString = "symbol=" + symbol_pair + "&side=" + side + "&type=" + type + "&quantity=" + quantity +  "&amp;timestamp=" + str(posix_timestamp_millis)

	# Creating hash for authentication
	signature = hmac.new(secretkey.encode(), queryString.encode(), hashlib.sha256).hexdigest()
	# Combining account information endpoint url with input variables and authentication hash
	url = url + f"?{queryString}&signature={signature}"

	# Sending POST request for order
	response_order = requests.post(url, headers={'X-MBX-APIKEY': apikey})

	# Convert response to JSON object for data extraction
	order=response_order.json()
	# print(json.dumps(order, indent=4)) # Pretty print to understand structure of data

	symbol_first_transaction=order['executedQty'] # How much of first symbol was bought/sold
	symbol_second_transaction=order['cummulativeQuoteQty'] # How much of second symbol was sold/bought
	fills=order['fills'] # Order fill information

	# Printing information

	if isBuyer == False:

		print('########################BOUGHT!########################')
		print(f'{symbol_first} Bought: {symbol_first_transaction}')
		print(f'{symbol_second} Sold: {symbol_second_transaction}')
		print(f'Fills: {fills}')
		print('########################BOUGHT!########################')

	elif isBuyer == True:

		print('########################SOLD!########################')
		print(f'{symbol_first} Sold: {symbol_first_transaction}')
		print(f'{symbol_second} Bought: {symbol_second_transaction}')
		print(f'Fills: {fills}')
		print('########################SOLD!########################')

	print('\n\n')

	time.sleep(5) # In seconds


```
{: file="binance_bot.py" }

## Trading Loop

Now that all the essential functions for this Binance Trading Robot have been defined, they can be called in the continuous while loop that will automatically trade the selected `symbol_pair`. This while loop continuously runs without end since it will always be true `while True:`. The logic of the loop can be seen below.

1. We first call the `current_price()` function to acquire the current price `cp` of the `symbol_pair`.
2. We then call the `account_balance()` function to calculate the user's `symbol_pair` account balance using `cp` and return how much of each asset is free (`assetfree` and `assetfree2`) to determine how much we can trade later on.
3. The `latest_transaction()` function is called to grab the latest transaction price `tp_price` at which the `symbol_pair` was traded at and to determine whether the first symbol was bought or sold `isBuyer`.
4. The next section of code determines what the buy/sell percentage `bsp` criteria is to submit an order to the Binance Rest API. The variable `bsp` is used to calculate buy/sell price `delta` needed to submit the order based off of the latest transaction price `tp_price`.
5. The script then goes into various if statements depending on the value of `isBuyer`.
	1. If `isBuyer` is equal to False, then the latest transaction was a SELL meaning that we want to buy the first symbol. The buy price `buyprice` is then calculated to be `buyprice = tp_price - delta` since we want to buy at a lesser price than what we sold it at. The buy price `buyprice` is compared to the current price `cp` to see if the buy order should be submitted `if cp &lt; buyprice`; else it doesn't do anything.
	2. If `isBuyer` is equal to True, then the latest transaction was a BUY meaning that we want to sell the first symbol. The sell price `sellprice` is then calculated to be `sellprice = tp_price + delta` since we want to sell at a greater price than what we bought it at. The sell price `sellprice` is compared to the current price `cp` to see if the sell order should be submitted `if cp &gt; sellprice`; else it doesn't do anything.
6. Once the if statement is exited, the script waits an hour `time.sleep(60*60)` before it goes to the next loop in the continous while loop.

> The function `submit_order()` is commented out by default for buying and selling orders in the actual script on GitHub.
{: .prompt-info }

```python
while True: # Continuously Run

	print('--------------------------------------------------New Check-------------------------------------------------')
	print('----------------------------------------',datetime.now(),'----------------------------------------')
	print('\n')

	#################
	# Current Price #
	#################

	cp = current_price() # Current price of symbol


	###################
	# Account Balance #
	###################

	assetfree, assetfree2 = account_balance()

	time.sleep(5)


	######################
	# Latest Transaction #
	######################

	tp_price, isBuyer = latest_transaction()


	############
	# BUY/SELL #
	############

	print('--------------------BUY/SELL Criteria--------------------')
	print('\n')

	# Trading fee is .075% if using bnb for fees https://www.binance.com/en/fee/schedule
	# Buy Sell Percentage bsp below must be greater than trading fee
	# But also needs to include a bit more margin to account for slippage since this script does market orders
	bsp=0.5 #buy/sell percent criteria in %
	print('Buy/Sell Percent Criteria: ', bsp, '%')
	delta=bsp/100*float(tp_price) # Delta of price calculated from buy/sell percent criteria
	print('Buy/Sell Criteria Delta (Previous Price * Percent): $', delta)
	print('\n')

	#################
	# Current Price #
	#################

	# Do this again to get the latest and greatest price since prices change so quickly
	cp = current_price() # Current price of symbol


	##################
	##### Buying #####
	##################

	if  isBuyer == False: # If latest transaction was a SELL

		buyprice=float(tp_price) - delta # Price to buy at
		print('--------------------Checking to see if time to BUY--------------------')
		print(f'Needed Price to Buy (Previous Price - Delta): ${buyprice}')
		print('\n')

		###################
		##### Yes Buy #####
		###################

		if float(cp) < buyprice:

			print('YES!')
			print(f'Current Price: {cp} < BUY Price: {buyprice}')
			print('\n')

			symbol_second_avail=np.floor(float(assetfree2)) # Round down to nearest whole number for second asset
			print(f'{symbol_second} Available: {symbol_second_avail}')
			print('\n')

			################
			# Submit Order #
			################

			submit_order()

			###################
			# Account Balance #
			###################

			#Do this again to get the latest and greatest account info after the new trade
			assetfree, assetfree2 = account_balance()


		##################
		##### No Buy #####
		##################

		elif float(cp) > buyprice:

			print('NO! PRICE IS HIGH!')
			print(f'Current Price: {cp} > BUY Price: {buyprice}')


		##################
		##### No Buy #####
		##################

		elif float(cp) == buyprice:

			print('NO! PRICE IS SAME!')
			print(f'Current Price: {cp} = BUY Price: {buyprice}')


	###################
	##### Selling #####
	###################

	elif isBuyer == True: # If latest transaction was a BUY

		sellprice=float(tp_price) + delta # Price to sell at
		print('--------------------Checking to see if time to SELL--------------------')
		print(f'Needed Price to Sell (Previous Price + Delta): ${sellprice}')
		print('\n')

		####################
		##### Yes Sell #####
		####################

		if float(cp) > sellprice:

			print('YES!')
			print(f'Current Price: {cp} > SELL Price: {sellprice}')

			# Round down to nearest hundredths place 0.01 for first asset
			n_decimals=2
			a=float(assetfree)
			symbol_first_avail=((a*10**n_decimals)//1)/(10**n_decimals)
			print(f'{symbol_first} Available: {symbol_first_avail}')

			################
			# Submit Order #
			################

			submit_order()

			###################
			# Account Balance #
			###################

			#Do this again to get the latest and greatest account info after the new trade
			assetfree, assetfree2 = account_balance()


		###################
		##### No Sell #####
		###################

		elif float(cp) < sellprice:

			print('NO! PRICE IS LOW!')
			print(f'Current Price: {cp} < SELL Price: {sellprice}')


		###################
		##### No Sell #####
		###################

		elif float(cp) == sellprice:

			print('NO! PRICE IS SAME!')
			print(f'Current Price: {cp} = SELL Price: {sellprice}')


	print('\n\n\n\n')
	time.sleep(60*60) # In seconds


```
{: file="binance_bot.py" }

## Bash Script

The b_rerun.sh bash script below can be used on a server/Raspberry Pi/etc... to run the binance_bot.py script and continuously check if it needs to be ran again just in case binance_bot.py crashes. The command `ps aux | grep '[p]ython binance_bot.py'` looks for a process running with the text `'[p]ython binance_bot.py'` to see if the binance_bot.py script is running. If it finds a matching process, it continues, does nothing, and then waits for 30 minutes before continuing to the next loop in the continuous while loop. If it doesn't find a matching process, it calls on python to run the script, outputs the script's print to b_output.txt, and then waits for 30 minutes before continuing to the next loop in the continuous while loop. The b_rerun.sh bash script can be ran with `sh b_rerun.sh &> b_rerunoutput.txt &` where the echo (print) is outputted to b_rerunoutput.txt.

If the process ID (PID) for either the b_rerun.sh or binance_bot.py script needs to be found in order to terminate the process, one can use `ps aux | grep '[b]_rerun.sh'` and `ps aux | grep '[b]inance_bot.py'`, respectively. Once the PIDs are found, one can terminate the scripts using `kill PID`. Note that b_rerun.sh needs to be killed as well or else it will start binance_bot.py up again after 30 minutes. If the square brackets [] are not included in these commands, the search itself will be returned as well. This is why the square brackets [] are used in the b_rerun.sh bash script since it will see the search itself and think the binance_bot.py script is still running when it is not.

```bash
while :
do
	if ps aux | grep '[p]ython binance_bot.py'; then

		echo $(date)
		echo "Script is still running"

	else

		echo $(date)
		echo "Script stopped running, time to rerun"
		python binance_bot.py &> b_output.txt &

	fi

	sleep 30m
done

```
{: file="b_rerun.sh" }

```bash
>>> ps aux | grep '[b]_rerun.sh'
	pi         618  0.0  0.0   1940   420 pts/1    S    22:53   0:00 sh b_rerun.sh

>>> ps aux | grep 'b_rerun.sh'
	pi         618  0.0  0.0   1940   420 pts/1    S    22:53   0:00 sh b_rerun.sh
	pi         769  0.0  0.0   7348   492 pts/1    S+   23:00   0:00 grep --color=auto b_rerun.sh

>>> kill 618
```
