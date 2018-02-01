import pandas as pd
import glob
import re
from collections import OrderedDict
import numpy as np
from time import sleep
import os
from datetime import datetime
from copy import deepcopy
def convert_str_to_num(st):
    aa = st.split(" ")
    return sum([int(x) for x in aa])

def convert_to_np_vec(a1):
    return np.array([int(x) for x in a1])
def from_prefix(pref="bid_ask_out/f_bid_ask_2017-12-21-19-4*"):
    L= glob.glob(pref)
    dc_tpN = {"ticker":"","bid":{"amount":0,"maximal_bid":0.0},"ask":{"amount":0,"minimal_ask":10.0**6}}
    L.sort()
    print(L)
    M=[]
    DLL = OrderedDict()
    for ll in L:
        
        f2 = open(ll,"r")
        r2 = f2.read()
        rt2 = r2.replace("\n","\t")
        rexp2 = re.findall(r'[A-Z]+,[a-z]+: ?[0-9]+\.[0-9]+[\t0-9]+',rt2)
        D = OrderedDict()
        for ii in rexp2:
            k = ii.split(",")[0]
            if k in list(D.keys()):
                ba = ii.split(",")[1].split(":")[0]
                if ba in list(D[k].keys()):
                    prs = ii.split(":")[1].split("\t")[0].replace(" ","")
                    if prs in list(D[k][ba].keys()):
                        D[k][ba][prs] = np.append(D[k][ba][prs],convert_to_np_vec(ii.split("\t")[1:-1]))
                    else:
                        D[k][ba][prs] = convert_to_np_vec(ii.split("\t")[1:-1])
                else:
                    D[k][ba] = OrderedDict()                
                    D[k][ba][ii.split(":")[1].split("\t")[0].replace(" ","")] = convert_to_np_vec(ii.split("\t")[1:-1])
            else:
                M1 = OrderedDict()
                M1[ii.split(":")[1].split("\t")[0].replace(" ","")] = convert_to_np_vec(ii.split("\t")[1:-1])
                M2 =OrderedDict()
                M2[ii.split(",")[1].split(":")[0]] = M1
                D[k] = M2
        """
        for k in D.keys():
            print k
            for kk in D[k].keys():
                print kk,D[k][kk].items()
        """
        M.append(D)
    o = open("out_diff.txt","w")
    D_pcs =OrderedDict()
    D_pcs["price_changes_counter"] = 0
    D_pcs["positive_changes_counter"] = 0
    D_pcs["negative_changes_counter"] = 0
    D_pcs["unchanged_counter"] = 0
    A_chg = OrderedDict()
    A_chg["changes"] = 0
    price_changes = OrderedDict()
    amount_changes = OrderedDict()
    for ij in range(len(M)):
        for k in list(M[ij].keys()):
            for kk in list(M[ij][k].keys()):
                price_changes[k+"_"+kk]=D_pcs.copy()
                amount_changes[k+"_"+kk] = A_chg.copy()
            
    for ind in range(1,len(M)):
        
        mm = M[ind]
        mb = M[ind-1]
        dc_tp = deepcopy(dc_tpN)
        for k in list(mm.keys()):
            if k in mb:
                o.write("..............................\n")
                for kk in list(mm[k].keys()):
                    o.write("%s,%s"%(k,kk))
                    
                    dc_tp["ticker"] = k 
                    dc_tp[kk]["amount"] = sum([sum(mm[k][kk][kbb]) for kbb in mm[k][kk].keys()])
                    if kk =="bid":
                        dc_tp[kk]["maximal_bid"] = max([float(kbb) for kbb in mm[k][kk].keys()])
                    elif kk =="ask":
                        dc_tp[kk]["minimal_ask"] = min([float(kbb) for kbb in mm[k][kk].keys()])

                


                    


                    o.write(("*"*50)+"\n")
                    o.write("before\t%s%s%s%s%s"%(mb[k][kk],"\nafter\t",mm[k][kk],"\n",("-"*50)+"\n"))

                    x1 = round(float(list(mm[k][kk].keys())[0]),2)
                    amount_a = sum([sum(mm[k][kk][kbb]) for kbb in mm[k][kk].keys()])
                    amount_b = sum([sum(mb[k][kk][kbb]) for kbb in mb[k][kk].keys()])

                    x2 = round(float(list(mb[k][kk].keys())[0]),2)
                    if x1>x2:
                        price_changes[k+"_"+kk]["positive_changes_counter"]+=1
                    elif x1<x2:
                        price_changes[k+"_"+kk]["negative_changes_counter"]+=1
                    else:
                        price_changes[k+"_"+kk]["unchanged_counter"]+=1
                    if x1!=x2:
                        price_changes[k+"_"+kk]["price_changes_counter"]+=1
                    if amount_b != amount_a:
                        amount_changes[k+"_"+kk]["changes"] +=1
        DLL[L[ind]] = dc_tp
    #print("positive_changes_counter:%d"%positive_changes_counter)
    #print("negative_changes_counter:%d"%negative_changes_counter)
    #print("price_changes_counter:%d"%price_changes_counter)
    #print("unchanged_counter:%d"%unchanged_counter)
    #print(price_changes)
    t1 = open(os.path.basename(pref.replace("*","_final_res.csv")),"w")
    cols = "Ticker,bid/ask,price_changes_counter,positive_changes_counter,negative_changes_counter,unchanged_counter,amount_changes"
    t1.write(cols+"\n")
    keys = cols.split(",")[2:]

    for ii in list(price_changes.keys()):
        print(ii)
        tba = ii.split("_")
        t1.write(tba[0]+","+tba[1])
        for jj in list(price_changes[ii].keys()):
            print(jj,price_changes[ii][jj])
            t1.write(","+str(price_changes[ii][jj]))
        t1.write(","+str((amount_changes[ii]["changes"])))
        t1.write("\n")
    t1.close()
    return (DLL)

if __name__ == "__main__":
    mint = datetime.now().strftime("%Y-%m-%d-%H-%M")
    
    for i in range(30):
        os.system("python mkt_data.py")
        sleep(0.5)
    
    mint2 = datetime.now().strftime("%Y-%m-%d-%H-%M")
    mint_mid = mint[:max ([k for k in range(len(mint)) if mint[:k] == mint2[:k]])]
    #from_prefix(os.path.join("bid_ask_out","f_bid_ask_2017-11-27-22-59*"))
    from_prefix(os.path.join("bid_ask_out","f_bid_ask_%s*"%mint))
