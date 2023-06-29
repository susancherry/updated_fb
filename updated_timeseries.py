import pandas as pd 
import numpy as np
for year in range(2013,2021):
	for m in [3,6,9,12]:
		if m<10:
			month = "0"+str(m)
		else:
			month = str(m)
		file_name ="/disk/homedirs/nber/cre2114/equifax/data/ORIG/nber_onefile_cat_analytic_dataset_"+str(year)
		file_name =file_name+month
		file_name=file_name+".csv.gz"
		data = pd.read_csv(file_name,usecols=["consumer_id","zip_code","number_of_accounts","age_oldest_account"])
    ind = pd.DataFrame(data.groupby("consumer_id").first())
    ind.loc[pd.isnull(ind.small_business_owner_flag),"small_business_owner_flag"]=0
    num=pd.DataFrame(ind.groupby("zip_code")["consumer_id"].count().reset_index())
		num.columns = ['zip_code', 'num_consumers']
    bus=pd.DataFrame(ind.groupby("zip_code")["small_business_owner_flag"].sum().reset_index())
		bus.columns = ['zip_code', 'num_bus_owner']
		data=num.merge(bus, on="zip_code",how="outer")
		data=data.merge(other, on="zip_code",how="outer")
		data["month"]=m
		data["year"]=year
		if ((year ==2013) &( m==3)):
			data.to_csv("zip_bus.csv.gz",index=False,header=True,mode='w')
		else:
			data.to_csv("zip_bus.csv.gz",index=False,header=False,mode='a')




