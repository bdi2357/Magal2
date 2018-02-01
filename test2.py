from ib.opt import ibConnection, message
from ib.ext.Contract import Contract
from time import sleep
import pandas as pd
import create

def my_callback_handler(msg):
    inside_mkt_bid = ''
    inside_mkt_ask = ''

    if msg.field == 1:
        inside_mkt_bid = msg.price
        print('bid', inside_mkt_bid)
    elif msg.field == 2:
        inside_mkt_ask = msg.price
        print('ask', inside_mkt_ask)


tws = ibConnection(port=4001,clientId=334)
tws.register(my_callback_handler, message.tickSize, message.tickPrice)
tws.connect()

contract_info = create.create_contract('AAPL', 'STK', 'SMART', 'USD')
tickedId = 334
print("contract_info",contract_info)
tws.reqMktData(tickedId, message, "", False)

c = Contract()
c.m_symbol = "AAPL"
c.m_secType = "STK"
c.m_exchange = "SMART"
c.m_currency = "USD"

print(tws.reqMktData(788,c,"",False))
sleep(1)
print(message.tickSize())
#tick_data = pd.DataFrame(message.tickSize, columns = ["tickerId", "field", "size"])
#tick_data["Type"] = tick_data["field"].map(tick_type)
#tick_data[-10:]
#print("price",tws.tickPrice,"size",tws.tickSize)
print('All done')


tws.disconnect()