

import ezibpy
import time

def ibCallback(caller, msg, **kwargs):
    if caller == "handleMarketDepth":
        print(chr(27) + "[2J")
        print( ibConn.marketDepthData[1] )

# initialize ezIBpy
ibConn = ezibpy.ezIBpy()
ibConn.connect(clientId=100, host="localhost", port=4001)

# custom callback to display orderbook
ibConn.ibCallback = ibCallback

# create a contract & request market depth

contractTuple = ("AAPL", 'STK', 'SMART', 'USD', 0.01, 0.0, 'False')
#contractTuple = ('QQQQ', 'OPT', 'SMART', 'USD', '20070921', 47.0, 'CALL')
#contractTuple = ('ES', 'FUT', 'GLOBEX', 'USD', '200709', 0.0, '')
#contractTuple = ('ES', 'FOP', 'GLOBEX', 'USD', '20070920', 1460.0, 'CALL')
#contractTuple = ('EUR', 'CASH', 'IDEALPRO', 'USD', '', 0.0, '')
#stkContract = makeStkContract(contractTuple)

contract = ibConn.createCashContract("AAPL", 'STK', 'SMART', 'USD' )
ibConn.requestMarketDepth()

# wait 30 seconds
time.sleep(1)



# cancel market data request & disconnect
ibConn.cancelMarketData()
ibConn.disconnect()