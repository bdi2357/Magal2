from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
from time import sleep
import pandas as pd
from datetime import datetime
import os
from ib.ext.TickType import TickType as tt
sep_str = ("^"*40)
# print all messages from TWS
now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
today = datetime.now().strftime("%Y-%m-%d")
target_dir = os.path.join("bid_ask_out",today)
if not os.path.isdir(target_dir):
    os.makedirs(target_dir)

f_w = open(os.path.join(target_dir,"f_bid_ask_"+now+".txt"),"w")
f_w_n = open(os.path.join(target_dir,"Nbid_ask_"+now+".txt"),"w")
f_w_n.write("START\n")
def my_callback_handler(msg):
    print("INNNN")
    print(msg,msg.field)
    if msg.field in [tt.BID,tt.ASK,tt.LAST]:
        #now we can just store the response in the data frame
        print(str(msg.items()))
        print(">"*100)
        print(str(msg))
        if str(msg).lower().find("error") == -1:
            print("No Error!!")
            f_w_n.write(str(msg)+"\n")


def watcher(msg):
    try:
        print("Watcher\n")
        #('tickerId', 1002), ('position', 6), ('marketMaker', 'NSDQ'), ('operation', 0), ('side', 0), ('price', 170.26), ('size', 3)
        #print(msg.items())
        msg = dict(msg.items())
        print("position:%d\n"%msg["position"])
        if msg['side'] == 0:
            ba = "ask"
        else:
            ba = "bid"
        print("bid/ask:%s\n"%ba)
        print("price:%0.2f\n"%msg["price"])
        print("size:%d\n"%msg["size"])
        print("*"*10 +"\n")
    except Exception as e:
        print(str(e))
        print("msg:",msg)
    if str(msg).lower().find("error") == -1:
        f_w_n.write(str(msg)+"\n")
    #print(dir(msg))

# show Bid and Ask quotes
def my_BidAsk2(msg):#,msg2):
    print("BA2")
    print(msg.items())
    #print(str(msg2))
def my_BidAsk(msg):
    #print("dir",dir(msg))
    print("BidAsk")
    K = [m for m in dir(msg) if m[0]!="_"]
    """
    for ii in K:
        print(ii,eval("msg."+ii))
    """
    print ("keys",msg.keys())
    print ("values",msg.values())
    print ("items",msg.items())

    if msg.field == 1:
        print (('*'*50)+ '\n%s, bid: %s' % (contractTuple[0], msg.price))
        f_w.write('%s,bid: %s\n' % (contractTuple[0], msg.price))
    elif msg.field == 2:
        print ('%s: ask: %s' % (contractTuple[0],msg.price))
        f_w.write('%s,ask:%s\n' % (contractTuple[0], msg.price))
    if msg.field == 3:
        print ('%s:%s: bid/ask: %s %S' % (contractTuple[0], contractTuple[6],msg.price,msg.size))
        f_w.write('%s:%s: bid/ask: %s %S\n' % (contractTuple[0], contractTuple[6],msg.price,msg.size))
    print ('%s,%s:%s: pcs: %s' % (msg.field,contractTuple[0], contractTuple[6],msg.price))
    if str(msg).lower().find("error") == -1:
        f_w_n.write(str(msg)+"\n")
def my_W(msg):
    #print("dir",dir(msg))
    print("Size")
    K = [m for m in dir(msg) if m[0]!="_"]
    """
    for ii in K:
        print(ii,eval("msg."+ii))
    """
    
    print ("items",msg.items())
    f_w.write(str(msg.items()[-1][1])+"\n")
    #f_w.write("\nSize","values",msg.values(),"items",msg.items())

    

def makeStkContract(contractTuple):
    newContract = Contract()
    newContract.m_symbol = contractTuple[0]
    newContract.m_secType = contractTuple[1]
    newContract.m_exchange = contractTuple[2]
    newContract.m_currency = contractTuple[3]
    newContract.m_expiry = contractTuple[4]
    newContract.m_strike = contractTuple[5]
    newContract.m_right = contractTuple[6]
    print ('Contract Values:%s,%s,%s,%s,%s,%s,%s:' % contractTuple)
    return newContract


if __name__ == '__main__':
    con = ibConnection(port = 4002, clientId = 335)
    con.registerAll(watcher)
    for sec in ["QQQ","AAPL"]: #["BSX","BA"]:#,'BSX','JNJ','CAT','BAC']:
        #showBidAskOnly = True  # set False to see the raw messages
        showBidAskOnly = True
        if showBidAskOnly:
            """
            con.unregister(watcher, message.tickSize, message.tickPrice,
                           message.tickString, message.tickOptionComputation)
            """
            print("nothing")
            #con.register(my_BidAsk, message.tickPrice)
            #con.register(my_W, message.tickSize)
            
        f_w_n.write(sep_str+"\n>>%s<<\n"%sec)
            #con.register()
        #con.register(print_all,'ticks')
        con.connect()
        sleep(0.02)
        tickId =1002 #321

    
        # Note: Option quotes will give an error if they aren't shown in TWS
        contractTuple = (sec, 'STK', 'ISLAND', 'USD', sec, 0.0, 'False')
        #contractTuple = ('QQQQ', 'OPT', 'SMART', 'USD', '20070921', 47.0, 'CALL')
        #contractTuple = ('ES', 'FUT', 'GLOBEX', 'USD', '200709', 0.0, '')
        #contractTuple = ('ES', 'FOP', 'GLOBEX', 'USD', '20070920', 1460.0, 'CALL')
        #contractTuple = ('EUR', 'CASH', 'IDEALPRO', 'USD', '', 0.0, '')
        stkContract = makeStkContract(contractTuple)
        print ('* * * * REQUESTING MARKET DATA * * * *')
        #con.reqMktData(tickId, stkContract, '', False)
        con.reqMktDepth(tickId, stkContract, 7)
        sleep(2)
        print(stkContract)

        #print("con.tickPrice",dir(con.tickPrice))
        #tick_data = pd.DataFrame(con.tickPrice, columns = ["tickerId", "field", "size"])
        #print(tick_data)
        
        
        print ('* * * * CANCELING MARKET DATA * * * *')
        
        #con.cancelMktData(tickId)
        #con.disconnect()
        
        con.unregister(watcher)
        #con.registerAll(my_BidAsk2)
        con.register(my_callback_handler, message.tickPrice, message.tickSize)
        if showBidAskOnly:
            print("Nothing")
            #con.unregister(watcher)
            #con.register(my_BidAsk2,message)# message.tickPrice,message.tickSize)
            #con.register(my_W, message.tickSize)
            #con.register()
        #con.register(print_all,'ticks')
        #con.connect()


        con.reqMktData(tickId, stkContract, '', False)
        sleep(1)
        print ('* * * * CANCELING MARKET DATA222222 * * * *')
        con.cancelMktData(tickId)
        sleep(0.01)
        con.disconnect()
f_w_n.close()        
        