from ib.opt import ibConnection, message
from ib.ext.Contract import Contract
from time import sleep

def my_callback_handler(msg):
    inside_mkt_bid = ''
    inside_mkt_ask = ''

    if msg.field == 1:
        inside_mkt_bid = msg.price
        print( 'bid', inside_mkt_bid)
    elif msg.field == 2:
        inside_mkt_ask = msg.price
        print('ask', inside_mkt_ask)


tws = ibConnection(port = 4001,clientId = 334)
tws.register(my_callback_handler, message.tickSize, message.tickPrice)
tws.connect()

c = Contract()
c.m_symbol = "AAPL"
c.m_secType = "STK"
c.m_exchange = "SMART"
c.m_currency = "USD"
tws.reqMktData(788,c,"",False)
print(c,dir(c))
for ff in dir(c):
	if ff[0]!="_":
		print(ff,eval("c."+ff)) 
sleep(1)
print('All done')

tws.disconnect()