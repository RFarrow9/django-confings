# Requires pandas. For Windows users, I recommend installing the Anaconda Python distirbution.
# Requires the pytrends library. To install, run "pip install pytrends".
from pytrends.request import TrendReq
import time
import os
from random import randint
import pandas as pd

print ("Imports complete")

# Add your Gmail username to the google_username variable and your Gmail password to the google_password variable.
google_username = ""
google_password = ""
connector = TrendReq(google_username, google_password, tz='-360')

# This script downloads a series of CSV files from Google Trends. Please specify a filepath for where you'd like these files to be stored in the below variable.
path = "C:\\Users\\robfa\\Desktop\\0.csv"

# Specify the filename of a CSV with a list of keywords in the variable, keyordcsv. The CSV should be one column, with header equal to Keywords (case sensitive).
keywordcsv = "keywords.csv"
keywords = pd.read_csv(keywordcsv)
#print(keywords)

# Downloads and Calculate Slope:
keywordlist = pd.DataFrame(columns=["keyword","slope","test"])
for index, row in keywords.iterrows():
    path = "C:\\Users\\robfa\\Desktop\\" + row[0] + ".csv"
    print("Downloading Keyword #" + str(index))
    print("")
    print("====" + row[0] + "====")
    print("")
    FullData_DF = pd.read_csv(path,names=['Date', 'Interest', 'Run'],index_col='Date')
    #print(FullData_DF)
    MaximumRun = FullData_DF['Run'].max(axis=0)
    print("Previous Maximum Run:", MaximumRun) #This holds the previous maximum run
    CurrentRun = MaximumRun + 1
    print("Now Running:", CurrentRun) #This holds the run currently being generated
    #print(FullData_DF['Run'].dtype)
    Latest_df = FullData_DF[FullData_DF['Run'] == (MaximumRun)] #This dataframe is to be compared to the generated payload
    print ("Building Payload")
    connector.build_payload(kw_list=[row[0]], timeframe='now 1-H')
    print ("Payload Built")
    time.sleep(randint(2, 5))
    print ("Creating Dataframe")
    interest_over_time_df = connector.interest_over_time()
    print ("Dataframe Created")
    print ("Printing Dataframe")
    
    print(Latest_df)
    print(interest_over_time_df)
   
    print(Latest_df.iloc[:, 0].dtype)
    print(Latest_df.iloc[:,0:].values)
    #== interest_over_time_df['date']
    #print{"twat"}
    #else print("knob")
    
    
    
    
     #for index, row in Latest_df['Date']
    with open(path, 'a') as f:
        interest_over_time_df = interest_over_time_df.assign(Run=CurrentRun)
        interest_over_time_df.to_csv(f, header=False)
    #interest_over_time_df.to_csv(path)
    #connector.save_csv(path, str(index))
    #with open(str(index) + '.csv', 'xt') as f:
        #f.close()
    #print ("created file")
    #c#svname = str(index)+".csv"
    #trenddata = pd.read_csv(csvname, skiprows=0, names=['date', 'values'])
    #keyword = trenddata['values'].loc[[0]][0]
    #trenddata = trenddata.ix[1:]
    #trenddata['keyword'] = keyword
    #trenddata.rename(columns={'values': 'trends'}, inplace=True)
    #trenddata['trends'] = pd.to_numeric(trenddata['trends'], errors='coerce')
    #trenddata['date'] = trenddata['date'].str.extract('(^[0-9]{4}\-[0-9]{2}\-[0-9]{2}) \-.*')
    #trenddata = trenddata.dropna()
    #trenddata['date'] = pd.to_datetime(trenddata['date'])
    #trenddata['year'] = pd.DatetimeIndex(trenddata['date']).year
    #trenddata['month'] = pd.DatetimeIndex(trenddata['date']).month
    #trenddata['day'] = pd.DatetimeIndex(trenddata['date']).day
    #maxyear = trenddata['year'].max()
    #grouped = trenddata.groupby(['year']).mean()
    #def slope_formula(xone, yone, xtwo, ytwo):
    #    return (ytwo-yone)/(xtwo-xone)
    #maxyear = trenddata['year'].max()
    #grouped = trenddata.groupby(['year']).mean()
    #slope = slope_formula(1,float(grouped.loc[grouped.index==maxyear-2]['trends']),
    #                      2,float(grouped.loc[grouped.index==maxyear-1]['trends']))
    #keywordlist = keywordlist.append({'keyword':keyword,'slope':slope}, ignore_index=True)
    #os.remove(csvname)

# Specify a csv filename to output the slope values.
#keywordlist.to_csv("trends_slope.csv", sep=",", encoding="utf-8", index=False)

print("Slope calculation and CSV export complete.")