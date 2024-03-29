import pandas as pd 
import numpy as np
for year in range(2020,2023):
    for m in [1,2,3,4,5,6,7,8,9,10,11,12]:
        if m<10:
            month = "0"+str(m)
        else:
            month = str(m)
        file_name ="/disk/homedirs/nber/sc4331/equifax_scratch/equifax/equifax_aws/"+str(year)
        file_name =file_name+month
        file_name=file_name+".csv.gz"
        cols=['CONSUMER_ID', 'TRADE_ID','PAYMENT_FREQUENCY', 'ECOA','ACTIVITY_DESIGNATOR','PRODUCT_CATEGORY','PORTFOLIO_TYPE','PIM_SCORE','CONSUMER_AGE', 'TERMS','STATUS_CATEGORY', 'BALANCE', 'HIGH_CREDIT', 'NARRCODE_1', 'NARRCODE_2', 'NARRCODE_3', 'NARRCODE_4','SCHEDULED_PAYMENT_AMOUNT','ACTUAL_PAYMENT_AMOUNT']
        data = pd.read_csv(file_name, usecols=cols)
        data=data.loc[data.PRODUCT_CATEGORY=="FM"]
        data=data.loc[pd.isnull(data.ACTIVITY_DESIGNATOR)]
        data=data.loc[data.STATUS_CATEGORY!=0]
        data=data.loc[data.BALANCE>0]
        data=data.loc[data.BALANCE<=3000000]
        data["forbear"]=0
        data.loc[((data.NARRCODE_1==300) |(data.NARRCODE_2==300)  | (data.NARRCODE_3==300)  | (data.NARRCODE_4==300)),"forbear"]=1
        data.loc[(data.BALANCE>0)&(data.SCHEDULED_PAYMENT_AMOUNT==0),"forbear"]=1
        data.loc[(data.BALANCE>0)& pd.isnull(data.SCHEDULED_PAYMENT_AMOUNT),"forbear"]=1
        data.loc[((data.NARRCODE_1==162) |(data.NARRCODE_2==162)  | (data.NARRCODE_3==162)  | (data.NARRCODE_4==162)),"forbear"]=1
        data.loc[((data.NARRCODE_1==163) |(data.NARRCODE_2==163)  | (data.NARRCODE_3==163)  | (data.NARRCODE_4==163)),"forbear"]=1
        data.loc[((data.NARRCODE_1==88) |(data.NARRCODE_2==88)  | (data.NARRCODE_3==88)  | (data.NARRCODE_4==88)),"forbear"]=1
        data.loc[((data.NARRCODE_1==49) |(data.NARRCODE_2==49)  | (data.NARRCODE_3==49)  | (data.NARRCODE_4==49)),"forbear"]=1
        data.loc[data.PAYMENT_FREQUENCY=="D","forbear"]=1
        data.loc[data.ACTUAL_PAYMENT_AMOUNT>=data.BALANCE,"forbear"]=np.nan
        data=data.loc[data.forbear==1]
        if ((year ==2020) &( m==1)):
            data.to_csv("updated_fm.csv",index=False,header=True,mode='w')
        else:
            data.to_csv("updated_fm.csv",index=False,header=False,mode='a')







