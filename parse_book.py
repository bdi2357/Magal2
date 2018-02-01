import pandas as pd
import re
import os
from datetime import datetime
home_dir = ""
sep_str = ("^"*40)
#
def find_all(st,sub):
	#return [m.start() for m in re.finditer(sub, st)]
	return [i for i in range(len(st)) if st.startswith(sub, i)]
def unif(lst):
    kk = set(x[0] for x in lst)
    dk = { lk : sum([x[1] for x in lst if x[0] == lk]) for lk in kk}
    return list(dk.items())
def parse_book_f(f_name,output_dir = "Book"):
	if not os.path.isdir(output_dir):
		os.mkdir(output_dir)
	ff =open(f_name,"r")

	tme = re.findall(r'[0-9]+-[0-9]+-[0-9]+-[0-9]+-[0-9]+-[0-9]+',f_name)[0]
	rrd = ff.read()
	print(sep_str)
	all_tickers_inds = find_all(rrd,sep_str)+[-1]
	print("all indexes:",all_tickers_inds)
	for kk in range(len(all_tickers_inds)-1):

		r = rrd[all_tickers_inds[kk]:all_tickers_inds[kk+1]]
		print(r[:100])
		ticker = re.findall(">>[A-Z]+<<",r)[0][2:-2]
		print("ticker|| : %s"%ticker)
		lines = r.split("\n")
		lines[:4]
		lines = [l for l in lines[:-1] if l[:1] =='{']
		DD = [eval(l) for l in lines]
		
		DD2 = [d for d in DD if not 'side' in d.keys()]
		DDR = [d for d in DD if 'side' in d.keys()]
		ask = [(d['price'],d['size']) for d in DDR if d["side"] == 0]
		bid = [(d['price'],d['size']) for d in DDR if d["side"] == 1]
		ask = unif(ask)
		bid = unif(bid)

		ask.sort(key = lambda x : x[0])
		ask[:3]
		bid.sort(key = lambda x : x[0],reverse=True)
		bid[:3]
		
		Ask = pd.DataFrame(ask,columns=["Price","size"])
		Bid = pd.DataFrame(bid,columns=["Price","size"])
		Ask.to_csv(os.path.join(output_dir,ticker+"_ask_"+tme+".csv"),index=False)
		Bid.to_csv(os.path.join(output_dir,ticker+"_bid_"+tme+".csv"),index=False)
		#print("Ask\n")
		#print(Ask)
		#print("Bid\n")
		#print(Bid)

import glob

if __name__ == "__main__":
	today = datetime.now().strftime("%Y-%m-%d")
	#ticker = "QQQ" 
	target_dir = os.path.join(home_dir,"bid_ask_out",today)
	target_out = os.path.join(home_dir,"Book",today)#,ticker)
	if not os.path.isdir(target_out):
		os.makedirs(target_out)
	#f_name = "bid_ask_out/Nbid_ask_2017-12-28-19-18-10.txt"
	#LL = ["Nbid_ask_2017-12-28-20-01-12.txt","Nbid_ask_2017-12-28-20-02-04.txt","Nbid_ask_2017-12-28-20-01-58.txt"]
	LL = glob.glob(os.path.join(target_dir,"Nbid_ask*txt"))
	LL.sort()

	for x in LL[:]:
		parse_book_f(x,output_dir=target_out)

