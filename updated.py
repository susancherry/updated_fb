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
        cols=['CONSUMER_ID', 'TRADE_ID', 'PRODUCT_CATEGORY','PIM_SCORE','CONSUMER_AGE', 'TERMS','STATUS_CATEGORY', 'BALANCE', 'HIGH_CREDIT', 'NARRCODE_1', 'NARRCODE_2', 'NARRCODE_3', 'NARRCODE_4','SCHEDULED_PAYMENT_AMOUNT','ACTUAL_PAYMENT_AMOUNT']
        data = pd.read_csv(file_name, usecols=cols)
        #revolv
        data.loc[data.PRODUCT_CATEGORY=="BC","categories"]="Rev"
        data.loc[data.PRODUCT_CATEGORY=="CFR","categories"]="Rev"
        data.loc[(((data.PRODUCT_CATEGORY=="RT") | (data.PRODUCT_CATEGORY=="OT1"))& (data.PORTFOLIO_TYPE=="R")),"categories"]="Rev"
        #student
        data.loc[data.PRODUCT_CATEGORY=="SL1","categories"]="Student"
        data.loc[data.PRODUCT_CATEGORY=="SL2","categories"]="Student"
        #auto
        data.loc[data.PRODUCT_CATEGORY=="AF1","categories"]="Auto"
        data.loc[data.PRODUCT_CATEGORY=="AF2","categories"]="Auto"
        data.loc[data.PRODUCT_CATEGORY=="AB1","categories"]="Auto"
        data.loc[data.PRODUCT_CATEGORY=="AB2","categories"]="Auto"
        #FM
        data.loc[data.PRODUCT_CATEGORY=="FM","categories"]="FM"
        data["forbear"]=0
        data.loc[((data.NARRCODE_1==300) |(data.NARRCODE_2==300)  | (data.NARRCODE_3==300)  | (data.NARRCODE_4==300)),"forbear"]=1
        data.loc[(data.BALANCE>0)&(data.SCHEDULED_PAYMENT_AMOUNT==0),"forbear"]=1
        data.loc[((data.NARRCODE_1==162) |(data.NARRCODE_2==162)  | (data.NARRCODE_3==162)  | (data.NARRCODE_4==162)),"forbear"]=1
        data.loc[((data.NARRCODE_1==163) |(data.NARRCODE_2==163)  | (data.NARRCODE_3==163)  | (data.NARRCODE_4==163)),"forbear"]=1
        data.loc[((data.NARRCODE_1==88) |(data.NARRCODE_2==88)  | (data.NARRCODE_3==88)  | (data.NARRCODE_4==88)),"forbear"]=1
        data.loc[((data.NARRCODE_1==49) |(data.NARRCODE_2==49)  | (data.NARRCODE_3==49)  | (data.NARRCODE_4==49)),"forbear"]=1
        data.loc[data.PAYMENT_FREQUENCY=="D","forbear"]=1
        #data.loc[data.STATUS_CATEGORY==7,"forbear"]=np.nan
        data.loc[data.ACTUAL_PAYMENT_AMOUNT>=data.BALANCE,"forbear"]=np.nan
        data["delin60"]=0
        data.loc[((data.STATUS_CATEGORY==3) | (data.STATUS_CATEGORY==4)  | (data.STATUS_CATEGORY==5)  | (data.STATUS_CATEGORY==6)| (data.STATUS_CATEGORY==8)| (data.STATUS_CATEGORY==9)),"delin60"]=1
        data["delin30"]=0
        data.loc[((data.STATUS_CATEGORY==2) | (data.STATUS_CATEGORY==3) | (data.STATUS_CATEGORY==4)  | (data.STATUS_CATEGORY==5)  | (data.STATUS_CATEGORY==6)| (data.STATUS_CATEGORY==8)| (data.STATUS_CATEGORY==9)),"delin30"]=1
        data["month"]=m
        data["year"]=year
        fm=data.loc[data.categories=="FM"]
        auto=data.loc[data.categories=="Auto"]
        student=data.loc[data.categories=="Student"]
        rev=data.loc[data.categories=="Rev"]
        data=pd.DataFrame(pd.groupby(["year","month","categories"])[["forbear","delin60","delin30"]]).reset_index()
        if ((year ==2020) &( m==1)):
            fm.to_csv("fm_data3.csv.gz",index=False,header=True,mode='w')
            data.to_csv("forbear.csv.gz",index=False,header=True,mode='w')

        else:
            fm.to_csv("fm_data3.csv.gz",index=False,header=False,mode='a')
            data.to_csv("forbear.csv.gz",index=False,header=False,mode='a')

