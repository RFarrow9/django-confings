# Requires pandas. For Windows users it would be best to use the anaconda distro
# Requires the pytrends library
from pytrends.request import TrendReq
import time
import numpy
from random import randint
import pandas as pd
import nma

print ("Imports complete")

# Add your Gmail username to the google_username variable and your Gmail password to the google_password variable.
# Be sure to amend the tz variable for your timezone.
# https://github.com/GeneralMills/pytrends
google_username = ""
google_password = ""
connector = TrendReq(google_username, google_password, tz='-360')

# This script downloads a series of CSV files. Please specify your working directory.
path = "C:\\Users\\robfa\\Desktop\\0.csv"

# Specify the filename of a CSV with a list of keywords in the variable, keywordcsv. The CSV should be one column, with header equal to Keywords (case sensitive).
keywordcsv = "keywords.csv"
keywords = pd.read_csv(keywordcsv)

# Downloads the new data, and compares this to the previous.
keywordlist = pd.DataFrame(columns=["keyword","slope","test"])
for index, row in keywords.iterrows():
    path = "C:\\Users\\robfa\\Desktop\\" + row[0] + ".csv"
    print("Downloading Keyword #" + str(index))
    print("")
    print("====" + row[0] + "====")
    print("")
    FullData_DF = pd.read_csv(path,
                              names=['index', 'date', row[0], 'Run', 'Average Ratio', 'AbsoluteValue'],
                              index_col='date')
    MaximumRun = FullData_DF['Run'].max(axis=0)
    if numpy.isnan(MaximumRun):
        MaximumRun = 0
    print("Previous Maximum Run:", MaximumRun)                                                                          #This holds the previous maximum run
    CurrentRun = MaximumRun + 1
    print("Now Running:", CurrentRun)                                                                                   #This holds the run currently being generated
    Latest_df = FullData_DF[FullData_DF['Run'] == (MaximumRun)]                                                         #This dataframe is to be compared to the generated payload
    print ("Building Payload")
    connector.build_payload(kw_list = [row[0]], timeframe = 'now 1-H')
    time.sleep(randint(2, 5))
    print("Creating Dataframe")
    interest_over_time_df = connector.interest_over_time()
    interest_over_time_df = interest_over_time_df.assign(Run=CurrentRun)
    Latest_df.reset_index(inplace=True)
    interest_over_time_df.reset_index(inplace=True)
    Latest_df = Latest_df.copy()
    Latest_df['date'] = Latest_df['date'].astype('datetime64[ns]')
    s1 = pd.merge(interest_over_time_df, Latest_df, how='inner', on=['date'])
    execution = 's1 = s1.assign(Ratio = (s1.' + row[0] + '_x) / (s1.' + row[0] + '_y))'
    exec(execution) #This is definitely not ideal! Come back to this to find a better way
    s1 = s1.head(-12)                                                                                                   #Most recent data is not fully trustworthy - last 12 minutes seem to vary
    Average_Ratio = s1["Ratio"].mean()
    print("Average Ratio:", round(Average_Ratio, 4))
    interest_over_time_df = interest_over_time_df.assign(Average_Ratio=Average_Ratio)
    interest_over_time_df = interest_over_time_df.assign(Absolute_Value=interest_over_time_df[row[0]] * Average_Ratio)
    with open(path, 'a') as f:
        interest_over_time_df.to_csv(f, header=False)
    print("CSV export complete.")
    def file_len(path):
        with open(path) as f:
            for i, l in enumerate(f):
                pass
        return i + 1
    #print(file_len(path))
    Peak_detect_short_DF = pd.read_csv(path,
                              names=['index', 'date', row[0], 'Run', 'Average Ratio', 'AbsoluteValue'],
                              index_col='date', skiprows=file_len(path) - 59 * 4)
    #print(Peak_detect_short_DF) #Looks over the last 2 hours or so
    #pd.rolling_std(Peak_detect_short_DF[['AbsoluteValue']], 5)
    print(Peak_detect_short_DF[['AbsoluteValue']].rolling(window=5, center=False).std())
    #print(Peak_detect_short_DF[['AbsoluteValue']])
print("Slope calculation and CSV export complete.")

#USE NOTIFYMYANDROID
#Take the last 4 or so (as an arbitrary starting point) runs data and calculate a rolling standard distribution.
#Do twice - one for long long range, one for very short peaks - perhaps this one could use a larger window? 10 runs?
#Once this value exceeds a certain value - set threshold then you have either a peak or a trough
#Then the notification method?




# Specify a csv filename to output the slope values.
#keywordlist.to_csv("trends_slope.csv", sep=",", encoding="utf-8", index=False)