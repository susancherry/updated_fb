import pandas as pd 
import numpy as np
for year in range(2020,20223):
    for m in [1,2,3,4,5,6,7,8,9,10,11,12]:
        if m<10:
            month = "0"+str(m)
        else:
            month = str(m)
        file_name ="/disk/homedirs/nber/sc4331/equifax_scratch/equifax/equifax_aws/"+str(year)
        file_name =file_name+month
        file_name=file_name+".csv.gz"
        cols=['CONSUMER_ID', 'TRADE_ID', 'ECOA','PRODUCT_CATEGORY','PIM_SCORE','CONSUMER_AGE', 'TERMS','STATUS_CATEGORY', 'BALANCE', 'HIGH_CREDIT', 'NARRCODE_1', 'NARRCODE_2', 'NARRCODE_3', 'NARRCODE_4','SCHEDULED_PAYMENT_AMOUNT','ACTUAL_PAYMENT_AMOUNT']
        data = pd.read_csv(file_name, usecols=cols)
        data=data.loc[data.PRODUCT_CATEGORY=="FM"]
        joint=data.loc[data.ECOA=="J"]
        nonjoint =data.loc[data.ECOA!="J"]
        joint = joint.sample(frac=0.5)
        data=joint.append(nonjoint)
        if ((year ==2020) &( m==1)):
            data.to_csv("fm_data3.csv.gz",index=False,header=True,mode='w')
        else:
            data.to_csv("fm_data3.csv.gz",index=False,header=False,mode='a')

