import pandas
import os, sys
from datetime import datetime
from darksky import forecast


path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'


def find_cred(service):
    file = "../Excel & CSV Sheets/login.csv"
    if os.path.exists(file):
        with open(file, "r") as file:
            lines = file.readlines()
            if service in lines[0]:
                cred = lines[0].split(",")[1]
                # print(cred)
            if service in lines[1]:
                cred = str(lines[1].split(",")[1]) + "," + str(lines[1].split(",")[2])
                # print(cred)
                    # logins[username] = password
    return cred

data = pandas.read_csv("../Excel & CSV Sheets/2019 Data/2019 Systematic Negatives Section 3.csv")
data.Date = data.Date.astype(str)
data.Hour = data.Hour.astype(str)
for i, values in enumerate(data.values):
    print(i)
    year = int(data.Date.values[i].split("-")[0])
    month = int(data.Date.values[i].split("-")[1])
    day = int(data.Date.values[i].split("-")[2])
    date = datetime(year, month, day, int(data.Hour.values[i]), 0, 0)
    unixtime = date.strftime('%s')
    data.UnixTime.values[i] = unixtime
data.to_csv("../Excel & CSV Sheets/2019 Data/2019 Systematic Negatives Section 3 Time.csv")