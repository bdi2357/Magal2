from time import sleep, strftime, localtime
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message

new_symbolinput = ['AAPL']
newDataList = []
dataDownload = []

def historical_data_handler(msg):
  global newDataList
  #print msg.reqId, msg.date, msg.open, msg.high, msg.low, msg.close, msg.volume
  if ('finished' in str(msg.date)) == False:
    new_symbol = new_symbolinput[msg.reqId]
    dataStr = '%s, %s, %s, %s, %s, %s, %s' % (new_symbol, strftime("%Y-%m-%d %H:%M:%S", localtime(int(msg.date))), msg.open, msg.high, msg.low, msg.close, msg.volume)
    newDataList = newDataList + [dataStr]
  else:
    new_symbol = new_symbolinput[msg.reqId]
    filename = 'minutetrades' + new_symbol + '.csv'
    csvfile = open('csv_day_test/' + filename,'wb')
    for item in newDataList:
      csvfile.write('%s \n' % item)
    csvfile.close()
    newDataList = []
    global dataDownload
    dataDownload.append(new_symbol)

con = ibConnection()
con.register(historical_data_handler, message.historicalData)
con.connect()

symbol_id = 0
for i in new_symbolinput:
  print i
  qqq = Contract()
  qqq.m_symbol = i
  qqq.m_secType = 'STK'
  qqq.m_exchange = 'SMART'
  qqq.m_currency = 'USD'
  con.reqHistoricalData(symbol_id, qqq, '', '1 D', '1 min', 'TRADES', 1, 2)
  symbol_id = symbol_id + 1
  sleep(0.5)

print dataDownload