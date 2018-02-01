
# coding: utf-8
# IbPy and Interactive Brokers Features Demonstration
"""
Tested on Python 2

## Learning Outcomes
At the end of this simple workshop, you will be able to 
1. Extract Account and Portfolio Information
2. Placing Orders
3. Request Market Data
4. Obtain Historical Data
5. Access Market Depth Information
6. Download Real Time Bars
7. Extract Executions Information, including commission report
# In[1]:
"""
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import sys
sys.path.insert(0,'ib')


# In[6]:

import time
from datetime import datetime
from IBWrapper import IBWrapper, contract
from ib.ext.EClientSocket import EClientSocket
from ib.ext.ScannerSubscription import ScannerSubscription


# In the example to follow, **`callback`** is our `IBWrapper` instantiated. We **receive** information via `callback`.
# 
# 
# In the example to follow, **`tws`** is our `EClientSocket` instantiated. We **request** information via `tws`

# In[7]:

accountName = "DU2251402"
print("---1----")
callback = IBWrapper()             # Instantiate IBWrapper. callback 
print("---2----")
tws = EClientSocket(callback)      # Instantiate EClientSocket and return data to callback
host = ""
port = 7497
clientId = 334


# In[9]:

tws.eConnect(host, port, clientId) # Connect to TWS


# In[10]:

tws.setServerLogLevel(5)           # Set error output to verbose


# In[11]:

create = contract()               # Instantiate contract class
callback.initiate_variables()


# Note how the work flow goes. We send a request via the prefix **tws.** followed by the request for the specific type of data after the dot for the information we are interested in. 
# 
# For example, we would like to get an update on account time, which required us calling `reqAccountUpdates`. 
# 
# We request for info by calling **`tws.reqAccountUpdates`** and the data will be returned via our callback function. In this case **`callback.update_AccountTime`**

# *****

# # Account and Portfolio
# ### Learning Outcomes
# For this section, you will learn how you can obtain the following information:
# 1. Account Updates
#    * Account Value
#    * Portfolio
#    * Account Time
# 2. Account Summary
# 3. Positions

# ### Summary of Account and Portfolio 
# 
# | Request Call | Functions Utilised | Data Stored in |
# | --- | --- | --- |
# | reqAccountUpdates | updateAccountValue | self.update_AccountValue |
# | | updatePortfolio | self.update_Portfolio |
# | | updateAccountTime | self.update_AccountTime |
# | reqAccountSummary | accountSummary | self.account_Summary |
# | reqPositions | position | self.update_Position |

# ### Sending Account Updates Request
# `reqAccountUpdates`

# In[12]:

tws.reqAccountUpdates(1, accountName)


# #### Obtaining Account Value
# `self.update_AccountValue`

# In[13]:

df1 = pd.DataFrame(callback.update_AccountValue, 
            columns = ['key', 'value', 'currency', 'accountName'])[:]
print("df1",df1)

# #### Obtaining Portfolio Value
# `self.update_Portfolio`

# In[14]:

df2 = pd.DataFrame(callback.update_Portfolio, 
             columns=['Contract ID','Currency',
                      'Expiry','Include Expired',
                      'Local Symbol','Multiplier',
                      'Primary Exchange','Right',
                      'Security Type','Strike',
                      'Symbol','Trading Class',
                      'Position','Market Price','Market Value',
                      'Average Cost', 'Unrealised PnL', 'Realised PnL', 
                      'Account Name'])[:]

print("df2",df2)
# #### Obtaining Account Time
# `self.update_AccountTime`

# In[10]:

callback.update_AccountTime

# ### Sending Account Summary Request
# `reqAccountSummary`
# 
# This function call can only be made when connected to a Financial Advisor (FA) account. Another way to look at this is that if you have more than one account, use this function.

# In[11]:

tws.reqAccountSummary(2,"All","NetLiquidation")


# #### Obtaining Account Summary
# `self.account_Summary`

# In[12]:

df3 = pd.DataFrame(callback.account_Summary, columns = ['Request_ID','Account','Tag','Value','Curency'])[:2]
print("df3",df3)


# ### Sending Position Request
# `reqPositions`
# 
# This function call request all positions for all accounts. This is more suitable for Financial Advisor. In the following example, I used pandas selection criteria to disply a specific account position.

# In[13]:

tws.reqPositions()


# #### Obtaining Position
# `self.update_Position`

# In[14]:

dat = pd.DataFrame(callback.update_Position, 
                   columns=['Account','Contract ID','Currency','Exchange','Expiry',
                            'Include Expired','Local Symbol','Multiplier','Right',
                            'Security Type','Strike','Symbol','Trading Class',
                            'Position','Average Cost'])
dat[dat["Account"] == accountName]
print(dat)
exit(0)

# *****

# # Orders
# ### Learning Outcomes
# For this section, you will learn how you can obtain the following information:
# 1. Open Order
# 2. Next Valid ID
# 3. Order Status

# ### Summary of Orders
# 
# | Request Call | Functions Utilised | Data Stored in |
# | --- | --- | --- |
# | reqIds | nextValidId | self.next_ValidId |
# | placeOrder | orderStatus | self.order_Status |
# | cancelOrder | | |
# | reqOpenOrders & reqAllOpenOrders | openOrder | self.open_Order |
# | | orderStatus | self.order_Status |
# | reqGlobalCancel | | |

# #### Demo - Stock Purchase
# * ** Request Next Valid Id**. `reqIds`
# * ** Using Create**. `create`

# In[15]:
"""
tws.reqIds(1)
order_id = callback.next_ValidId + 1
contract_info = create.create_contract("GOOG", "STK", "SMART", "USD")
order_info = create.create_order(accountName, "MKT", 100, "BUY")


# #### Placing an Order
# `placeOrder`

# In[16]:

tws.placeOrder(order_id, contract_info, order_info)


# #### Checking Order Status
# `self.order_Status`

# In[17]:

pd.DataFrame(callback.order_Status,
             columns = ['orderId', 'status', 'filled', 'remaining', 'avgFillPrice',
                        'permId', 'parentId', 'lastFillPrice', 'clientId', 'whyHeld'])


# #### Checking on Open Order
# `self.open_Order`

# In[18]:

callback.open_Order[:1]


# #### Cancelling Open Order
# `cancelOrder`

# In[19]:

tws.cancelOrder(order_id)


# #### Demo
# * ** Request Next Valid Id**. `reqIds`
# * ** Using Create**. `create`
# * ** Placing an Order to purchase Futures**. `placeOrder`

# In[20]:

tws.reqIds(1)
order_id = callback.next_ValidId + 1
contract_info = create.create_contract(symbol = "ES", secType = "FUT", 
                                       exchange = "GLOBEX", currency = "USD", 
                                       right = None, strike = None,
                                       expiry = "201703", multiplier=None,
                                       tradingClass=None)
order_info = create.create_order(accountName, "MKT", 1, "BUY")
tws.placeOrder(order_id, contract_info, order_info)


# #### Checking Order Status

# In[21]:

pd.DataFrame(callback.order_Status,
             columns = ['orderId', 'status', 'filled', 'remaining', 'avgFillPrice',
                        'permId', 'parentId', 'lastFillPrice', 'clientId', 'whyHeld'])


# IB provided two more methods:
# * `reqOpenOrders()` to request any open orders that were placed from this API client.
# * `reqAllOpenOrders()` to request all open orders that were placed from all API clients linked to one TWS and also from the TWS.
# 
# Each open order will be fed back through `openOrder()` and `orderStatus()` methods.

# Finally, use `reqGlobalCancel()` to cancel all open orders globally.

# *****

# # Market Data
# ### Learning Outcomes
# For this section, you will learn how you can obtain the following information:
# 1. Request Market Data
#    * Tick Price
#    * Tick Size
# 2. Cancel Market Data
# 3. Calculate Implied Volatility
# 4. Calculate Option Price

# ### Summary of Market Data
# 
# | Request Call | Functions Utilised | Data Stored in |
# | --- | --- | --- |
# | reqMktData | tickPrice  | self.tick_Price |
# |  | tickSize | self.tick_Size |
# |  | tickOptionComputation  | self.tick_OptionComputation |
# |  | tickGeneric | self.tick_Generic |
# |  | tickString | self.tick_String |
# |  | tickEFP  | self.tick_EFP |
# |  | tickSnapshotEnd | self.tickSnapshotEnd_flag |
# | cancelMktData | | |
# | calculateImpliedVolatility | tickOptionComputation  | self.tick_OptionComputation |
# | cancelcalculateImpliedVolatility | | |
# | calculateOptionPrice  | tickOptionComputation  | self.tick_OptionComputation |
# | cancelCalculateOptionPrice | | |
# | reqMktDataType | marketDataType | self.market_DataType |
# 
# The method `reqMktDataType` allows you to toggle between receiving real-time or frozen market data.

# #### Requesting Market Data
# `reqMktData`

# In[22]:

contract_info = create.create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')
tickedId = 1002
tws.reqMktData(tickedId, contract_info, "", False)


# #### Receiving Tick Price
# `self.tick_Price`

# In[23]:

tick_data = pd.DataFrame(callback.tick_Price, 
                         columns = ['tickerId', 'field', 'price', 'canAutoExecute'])
tick_type = {0 : "BID SIZE",
             1 : "BID PRICE",
             2 : "ASK PRICE",
             3 : "ASK SIZE",
             4 : "LAST PRICE",
             5 : "LAST SIZE",
             6 : "HIGH",
             7 : "LOW",
             8 : "VOLUME",
             9 : "CLOSE PRICE",
             10 : "BID OPTION COMPUTATION",
             11 : "ASK OPTION COMPUTATION",
             12 : "LAST OPTION COMPUTATION",
             13 : "MODEL OPTION COMPUTATION",
             14 : "OPEN_TICK",
             15 : "LOW 13 WEEK",
             16 : "HIGH 13 WEEK",
             17 : "LOW 26 WEEK",
             18 : "HIGH 26 WEEK",
             19 : "LOW 52 WEEK",
             20 : "HIGH 52 WEEK",
             21 : "AVG VOLUME",
             22 : "OPEN INTEREST",
             23 : "OPTION HISTORICAL VOL",
             24 : "OPTION IMPLIED VOL",
             27 : "OPTION CALL OPEN INTEREST",
             28 : "OPTION PUT OPEN INTEREST",
             29 : "OPTION CALL VOLUME"}
tick_data["Type"] = tick_data["field"].map(tick_type)
tick_data[-10:]


# #### Receiving Tick Size
# `self.tick_Size`

# In[24]:

tick_data = pd.DataFrame(callback.tick_Size, 
                         columns = ["tickerId", "field", "size"])
tick_data["Type"] = tick_data["field"].map(tick_type)
tick_data[-10:]


# #### Calculate Implied Volatility
# `calculateImpliedVolatility`

# In[25]:

contract_info = create.create_contract(symbol='NFLX 160819C00095000',
                                       secType='OPT', exchange='SMART', 
                                       currency='USD',
                                       right='CALL', 
                                       strike='95', 
                                       expiry='20160819',
                                       multiplier=100, 
                                       tradingClass="NFLX")
tws.calculateImpliedVolatility(tickedId, 
                               contract_info, 
                               5.89, 
                               89.91)


# In[27]:

pd.DataFrame(callback.tick_OptionComputation,
             columns=["tickerId", "field", "impliedVol", "delta",
                      "optPrice", "pvDividend", "gamma", "vega",
                      "theta", "undPrice"])


# #### Calculate Option Price
# `tick_OptionComputation`

# In[28]:

tws.calculateOptionPrice(tickedId, 
                         contract_info, 
                         0.84, 
                         89.91)


# In[29]:

pd.DataFrame(callback.tick_OptionComputation,
             columns=["tickerId", "field", "impliedVol", "delta",
                      "optPrice", "pvDividend", "gamma", "vega",
                      "theta", "undPrice"])


# #### Cancelling Market Data Stream
# `cancelMktData`

# In[30]:

tws.cancelMktData(tickedId)


# *****

# # Historical Data
# ### Learning Outcomes
# For this section, you will learn how you can obtain the following information:
# 1. Historical Data

# ### Summary of Historical Data
# 
# | Request Call | Functions Utilised | Data Stored in |
# | --- | --- | --- |
# | reqHistoricalData | historicalData  | self.historical_Data |

# In[31]:

#contract_Details = create.create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')
contract_Details = create.create_contract('AAPL', 'STK', 'SMART', 'USD')


# In[32]:

data_endtime = datetime.now().strftime("%Y%m%d %H:%M:%S")


# #### Requesting Historical Data
# `reqHistoricalData`

# In[33]:

tickerId = 9002
tws.reqHistoricalData(tickerId, 
                      contract_Details, 
                      data_endtime,
                      "1 M", 
                      "1 day", 
                      "BID", 
                      0, 
                      1)


# In[35]:

data= pd.DataFrame(callback.historical_Data, 
                   columns = ["reqId", "date", "open",
                              "high", "low", "close", 
                              "volume", "count", "WAP", 
                              "hasGaps"])
data[-10:]


# *****

# # Market Depth
# ### Learning Outcomes
# For this section, you will learn how you can obtain the following information:
# 1. Request Market Depth

# ### Summary of Market Depth
# 
# | Request Call | Functions Utilised | Data Stored in |
# | --- | --- | --- |
# | reqMktDepth           | updateMktDepth          | self.update_MktDepth |

# In[36]:

contract_info = create.create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')


# In[37]:

tickerId = 7000
tws.reqMktDepth(tickerId, contract_info, 5)


# In[38]:

operation_type = {0 : "Insert",
                  1 : "Update",
                  2 : "Delete",}
side_type = {0 : "Ask",
             1 : "Bid"}


# In[39]:

data_mktdepth = pd.DataFrame(callback.update_MktDepth,
                             columns = ["tickerId", "position", 
                                        "operation", "side", 
                                        "price", "size"])
data_mktdepth["operation_type"] = data_mktdepth["operation"].map(operation_type)
data_mktdepth["side_type"] = data_mktdepth["side"].map(side_type)
data_mktdepth[-10:]


# *****

# # Real Time Bars
# ### Learning Outcomes
# For this section, you will learn how you can obtain the following information:
# 1. Request Real Time Bars
# 
# Note:
# * **barSize**. Only 5 sec bars are supported. 
# * **whatToShow**:
#    * TRADES
#    * BID
#    * ASK
#    * MIDPOINT
# * **useRTH**:
#    * 0 = all data
#    * 1 = only data within **R**egular **T**rading **H**ours

# ### Summary of Real Time Bars
# 
# | Request Call | Functions Utilised | Data Stored in |
# | --- | --- | --- |
# | reqRealTimeBars           | realtimeBar          | self.real_timeBar |

# In[40]:

contract_Details = create.create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')


# In[41]:

tickerId = 10000
tws.reqRealTimeBars(tickerId, 
                    contract_Details, 
                    5, 
                    "MIDPOINT", 
                    0)


# In[43]:

pd.DataFrame(callback.real_timeBar, 
             columns = ["reqId", "time", "open", "high", "low", "close", "volume", "wap", "count"])


# *****

# # Executions
# ### Learning Outcomes
# For this section, you will learn how you can obtain the following information:
# 1. Request Executions

# ### Summary of Executions
# 
# | Request Call | Functions Utilised | Data Stored in |
# | --- | --- | --- |
# | reqExecutions           | execDetails          | self.exec_Details_reqId |
# | | | self.exec_Details_contract |
# | | | self.exec_Details_execution |
# | | execDetailsEnd |self.exec_DetailsEnd_flag |
# | | commissionReport | self.commission_Report |

# In[44]:

tws.reqIds(1)
order_id = callback.next_ValidId + 1
contract_info = create.create_contract(symbol = "ES", secType = "FUT", 
                                       exchange = "GLOBEX", currency = "USD", 
                                       right = None, strike = None,
                                       expiry = "201703", multiplier=None,
                                       tradingClass=None)
order_info = create.create_order(accountName, "MKT", 1, "BUY")
tws.placeOrder(order_id, contract_info, order_info)


# In[45]:

tws.reqExecutions(3050, create.exec_filter(clientId, accountName, contract_info))


# In[46]:

callback.exec_Details_reqId


# In[47]:

callback.exec_Details_contract.__dict__


# In[48]:

callback.exec_Details_execution.__dict__


# In[49]:

pd.DataFrame(callback.commission_Report.__dict__, index=[0])


# In[50]:
"""
tws.eDisconnect()


# 
