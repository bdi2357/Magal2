import warnings
from time import sleep
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import sys
sys.path.insert(0,'ib')
warnings.filterwarnings('ignore')
print("---0----")
import pandas as pd
import numpy as np
import time
from datetime import datetime
from IBWrapper import IBWrapper, contract
from ib.ext.EClientSocket import EClientSocket
print("---0.5----")
from ib.ext.ScannerSubscription import ScannerSubscription
accountName = "mgdl1000"
print("---1----")
callback = IBWrapper()             # Instantiate IBWrapper. callback 
print("---2----")
tws = EClientSocket(callback)      # Instantiate EClientSocket and return data to callback
host = ""
port = 4001
clientId = 334
print("---3----")
tws.eConnect(host, port, clientId) 
sleep(1)
tws.setServerLogLevel(5)  
sleep(1)
create = contract()
print("---4----")# Instantiate contract class
callback.initiate_variables()
sleep(1)
print("---5----")
tws.reqAccountUpdates(1, accountName)
sleep(1)
df_ac = pd.DataFrame(callback.update_AccountValue, columns = ['key', 'value', 'currency', 'accountName'])[:3]
print(df_ac)
df_ac.to_csv("real_account2.csv")
df_portfolio = pd.DataFrame(callback.update_Portfolio, 
             columns=['Contract ID','Currency',
                      'Expiry','Include Expired',
                      'Local Symbol','Multiplier',
                      'Primary Exchange','Right',
                      'Security Type','Strike',
                      'Symbol','Trading Class',
                      'Position','Market Price','Market Value',
                      'Average Cost', 'Unrealised PnL', 'Realised PnL', 
                      'Account Name'])[:]
print("df_portfolio",df_portfolio)

contract_info = create.create_contract("SPY", "STK", "SMART", "USD")
#print(help(tws.reqMktData))
#client.reqMktData(1005, ContractSamples.USStock(), "", false, true, null);
print("MKT DATA",tws.reqMktData(334, contract_info, "", True))
#print("price is",tws.tick_Price)
tick_data = pd.DataFrame(callback.tick_Price, columns = ['tickerId', 'field', 'price', 'canAutoExecute'])
print("tick data",tick_data)
exit(0)
contract_info = create.create_contract("SPY", "STK", "SMART", "USD")
tickedId = 1002
print(ContractSamples.USStock())
tws.reqMktData(1004, ContractSamples.USStock(), "233,236,258", false, false, null);
#tws.reqMktData(tickedId, contract_info, "", False)