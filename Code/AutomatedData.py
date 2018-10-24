import email
import imaplib
import os
from datetime import datetime, timedelta, date, time
import time
from darksky import forecast
import pytz
import pandas
import math
import os, sys
import random
from selenium import webdriver

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'


def get_Email():
    # connecting to the gmail imap server
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login('utcscal2018@gmail.com', 'EMCS 335')
    m.select("INBOX")  # here you a can choose a mail box like INBOX instead
    # use m.list() to get all the mailboxes

    resp, items = m.search(None,"ALL")  # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
    items = items[0].split()  # getting the mails id

    #This is the number of emails in the inbox.
    # print(len(items))

    for emailid in items:
        resp, data = m.fetch(emailid, "(RFC822)")  # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
        email_body = data[0][1]  # getting the mail content
        mail = email.message_from_bytes(email_body)


        today = (datetime.now()).date()
        dateofemail = mail["Date"]
        dateofemail = (email.utils.parsedate_to_datetime(dateofemail)).date() #What time the email was sent, first just from the email, then transformed into something we can work with.
        day = timedelta(1) #one day in timedelta format. So, exactly 24 hours ago.
        daybefore = (dateofemail - day)#this is yesterday, which helps in labelling for the file itself.


        if dateofemail == today:    #So, if the email is from today.
            if mail["From"] == '<reports@hc911.org>' and 'Accident Report was executed for HC911' in mail["Subject"]:   #Selecting only the emails that pertain to call records.

                # Check if any attachments at all
                if mail.get_content_maintype() != 'multipart':
                    continue
                # we use walk to create a generator so we can iterate on the parts and forget about the recursive headache
                for part in mail.walk():
                    # multipart are just containers, so we skip them
                    if part.get_content_maintype() == 'multipart':
                        continue

                    # is this part an attachment ?
                    if part.get('Content-Disposition') is None:
                        continue

                    filename = part.get_filename()
                    # print("Downloading this email: ", mail["Subject"])

                    if filename is not None:    #Saves the attachment in the daily record folder with a tidy name.
                        sv_path = os.path.join(folderpath + 'Excel & CSV Sheets/2018 Data/DailyReports/911_Reports_for_'+ str(daybefore)+'.csv')
                        if not os.path.isfile(sv_path):
                            # print(sv_path)
                            fp = open(sv_path, 'wb')
                            fp.write(part.get_payload(decode=True))
                            fp.close()
    file = folderpath + 'Excel & CSV Sheets/2018 Data/DailyReports/911_Reports_for_' + str(daybefore) + '.csv'
    calllog = pandas.read_csv(file,sep=",")
    return calllog, file


def split_datetime(calldata):

    for i, value in enumerate(calldata.values):
        header_list = ('Response_Date', 'Fixed_Time_CallClosed', 'Address', 'City',
                       'Latitude','Longitude' ,'Problem', 'Date','Time','Hour', 'Month')

        calldata = calldata.reindex(columns=header_list)
        # next three lines are a necessary workaround due to pandas error
        calldata.Date = calldata.Date.astype(str)
        calldata.Time = calldata.Time.astype(str)
        calldata.Hour = calldata.Hour.astype(str)

        dateof = datetime.strptime(calldata.Response_Date.values[i], '%m/%d/%Y %I:%M:%S %p')
        moa = int(calldata.Response_Date.values[i].split('/')[0])
        calldata.Date.values[i] = dateof.date()
        calldata.Time.values[i] = dateof.time()
        calldata.Hour.values[i] = dateof.hour
        calldata.Month.values[i] = moa

    print('Time/Date Split complete.')
    return calldata


def clean_problems(calldata):
    # To drop the excess data from the problem column in python instead of manually.
    for i, value in enumerate(calldata.Problem.values):
        value = str(value)
        problem = str(value.split(None, 1)[1])
        problem = problem.split('\'',1)[0]
        calldata.Problem.values[i] = problem
    return calldata


def save_excel_file(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    writer.save()


def drop_duplicates(calldata):
    datafile = pandas.read_excel(folderpath + "Excel & CSV Sheets/2018 Data/DailyReports/ToRemoveFile.xlsx")
    listing = list(datafile.index.values)
    calldata.drop(calldata.index[listing], inplace=True)
    return calldata


def find_Duplicates(data_file_name, occurrence_list):
    for k, info in enumerate(data_file_name.values):
        if data_file_name.Latitude.values[k] > 40:
            data_file_name.Latitude.values[k] = (data_file_name.Latitude.values[k] / 1000000)
            data_file_name.Longitude.values[k] = (data_file_name.Longitude.values[k] / -1000000)
    count_doubles = 0
    data_file_copy = data_file_name.copy()
    remove = pandas.DataFrame(columns= data_file_copy.columns)
    # id1 = 0
    # id2 = data_file_copy.index[id1 + 1]
    for id1, id in enumerate(data_file_copy.values):
        if id1 + 1 >= len(data_file_copy)-1:
            print("There were :", count_doubles, "occurrences of duplicate calls.")
            save_excel_file(folderpath + 'Excel & CSV Sheets/2018 Data/DailyReports/ToRemoveFile.xlsx',
                            'Call Info', remove)
            break
        else:
            id2 = data_file_copy.index[id1 + 1]
            time1 = datetime.strptime(data_file_copy.Time.values[id1],"%H:%M:%S").time()
            time2 = datetime.strptime(data_file_copy.Time.values[id2],"%H:%M:%S").time()
            duration = datetime.combine(date.min, time2) - datetime.combine(date.min, time1)
            duration = duration.total_seconds()
            minutes = math.fabs(duration / 60.0)
            if minutes < 4:
                lat1= data_file_copy.Latitude.values[id1]
                long1 = data_file_copy.Longitude.values[id1]
                lat2 = data_file_copy.Latitude.values[id2]
                long2 = data_file_copy.Longitude.values[id2]
                latChange = math.fabs(lat1 - lat2)
                longChange = math.fabs(long1 - long2)
                if latChange < 0.0001 and longChange < 0.0001:
                    count_doubles += 1
                    problem1 = data_file_copy.Problem.values[id1].lstrip()
                    problem2 = data_file_copy.Problem.values[id2].lstrip()
                    if occurrence_list.index(problem1) >= occurrence_list.index(problem2):
                        #print("Dropping id at: ", id2)
                        remove = remove.append(data_file_copy.iloc[[id2]], ignore_index=False)
                        #data_file_name = data_file_name.drop(index=id2, inplace=False)
                    else:
                        # print("Dropping first id at: ", id1)
                        #print(data_file_copy.iloc[[id1]])
                        remove = remove.append(data_file_copy.iloc[[id1]], ignore_index=False)
                        #data_file_name = data_file_name.drop(index=id1, inplace=False)
                # return remove


def data_cleaning(calldata):
    # The next for loops are used to fill in blank values in the corresponding columns
    # (just so I don't have to do it by hand)
    for n, value4 in enumerate(calldata.values):
        if pandas.isnull(calldata.Precip_Intensity_Max.values[n]) is True:
            calldata.Precip_Intensity_Max.values[n] = -1000
    for c, value5 in enumerate(calldata.values):
        if pandas.isnull(calldata.Cloud_Coverage.values[c]) is True:
            calldata.Cloud_Coverage.values[c] = -1000

    return calldata


def add_data(calldata, save_name):
    # Getting the weekday
    calldata['Date'] = pandas.to_datetime(calldata['Date'])
    calldata['Weekday'] = calldata['Date'].dt.dayofweek
    calldata.Date = calldata.Date.astype(str)

    print("Getting Accident Weather Data")
    calldata = get_weather_data(calldata)
    print("Getting Accident Road Geometrics")
    driver = webdriver.Firefox(executable_path=r"/home/admin/PycharmProjects/RolandProjects/geckodriver")
    driver.get("https://e-trims.tdot.tn.gov/Account/Logon")

    usr = driver.find_element_by_id("UserName")
    pw = driver.find_element_by_id("Password")

    usr.send_keys("JJVPG58")
    pw.send_keys("Nashville1")
    driver.find_element_by_class_name("btn").click()

    calldata.Route = calldata.Route.astype(str)

    for i, info in enumerate(calldata.values):
        latitude = calldata.Latitude.values[i]
        longitude = calldata.Longitude.values[i]

        site = "https://e-trims.tdot.tn.gov/etrimsol/services/applicationservice/roadfinder/lrsforlatlong?latitude=" \
               + str(latitude) + "&longitude=" + str(longitude) + "&d=1538146112919"

        driver.get(site)
        raw = str(driver.page_source)
        milepoint = float(raw[raw.index("<MilePoint>") + len("<MilePoint>"): raw.index("</MilePoint>")])
        routeid = raw[raw.index("<RouteId>") + len("<RouteId>"): raw.index("</RouteId>")]

        calldata.Route.values[i] = routeid
        calldata.Log_Mile.values[i] = milepoint

    geometrics = pandas.read_csv(
        "/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/ETRIMS/Roadway_Geometrics_New.csv",
        sep=",")
    segments = pandas.read_csv(
        "/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/ETRIMS/Road_Segment_County_Raw.csv",
        sep=",")
    descriptions = pandas.read_csv(
        "/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/ETRIMS/Roadway_Description_County_HAMILTON RAW.csv",
        sep=",")
    traffic = pandas.read_csv(
        "/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/ETRIMS/Traffic_Count.csv",
        sep=",")
    for k, info in enumerate(calldata.values):
        for i, value in enumerate(geometrics.values):
            if calldata.Route.values[k] == geometrics.ID_NUMBER.values[i]:
                if geometrics.ELM.values[i] > calldata.Log_Mile.values[k] > geometrics.BLM.values[i]:
                    calldata.Num_Lanes.values[k] = geometrics.Num_Lns.values[i]
                    calldata.Thru_Lanes.values[k] = geometrics.Thru_Lanes.values[i]
        for l, value in enumerate(segments.values):
            if calldata.Route.values[k] == segments.ID_NUMBER.values[l]:
                if segments.ELM.values[l] > calldata.Log_Mile.values[k] > segments.BLM.values[l]:
                    calldata.Ad_Sys.values[k] = segments.Ad_Sys.values[l]
                    calldata.Gov_Cont.values[k] = segments.Gov_Cont.values[l]
                    calldata.Func_Class.values[k] = segments.Func_Class.values[l]
        for m, value in enumerate(traffic.values):
            if calldata.Route.values[k] == traffic.ID_NUMBER.values[m]:
                if traffic.ELM.values[m] > calldata.Log_Mile.values[k] > traffic.BLM.values[m]:
                    calldata.AADT.values[k] = traffic.AADT.values[m]
                    calldata.DHV.values[k] = traffic.DHV.values[m]
        for n, value in enumerate(descriptions.values):
            if calldata.Route.values[k] == descriptions.ID_NUMBER.values[n]:
                if descriptions.ELM.values[n] > calldata.Log_Mile.values[k] > descriptions.BLM.values[n]:
                    if descriptions.Feature_Type[n] == 19:
                        calldata.Pavement_Width.values[k] = descriptions.Feat_Width.values[n]
                        calldata.Pavement_Type.values[k] = descriptions.Feature_Composition.values[n]
        for i, value in enumerate(geometrics.values):
            if calldata.Route.values[k] == geometrics.ID_NUMBER.values[i]:
                if geometrics.ELM.values[i] > calldata.Log_Mile.values[k] > geometrics.BLM.values[i]:
                    calldata.Terrain.values[k] = geometrics.Terrain.values[i]
                    calldata.Land_Use.values[k] = geometrics.Land_Use.values[i]
                    calldata.Access_Control.values[k] = geometrics.Acc_Ctrl.values[i]
                    calldata.Illumination.values[k] = geometrics.Illum.values[i]
                    calldata.Speed_Limit.values[k] = geometrics.Spd_Limit.values[i]
                    calldata.Operation.values[k] = geometrics.Operation.values[i]
    return calldata


def append_data(calldata):
    # Appending new data to the New Data file #
    print("Appending Accident Data")
    calldata = calldata.iloc[::-1]
    og_calldata = pandas.read_csv(
        folderpath + "Excel & CSV Sheets/New Data Files/New Accident Data.csv", sep=",")
    frames = [og_calldata, calldata]
    results = pandas.concat(frames)
    header_list = ("Accident", 'Latitude', 'Longitude', 'Date', 'Time', 'Address', "Route", "Log_Mile", 'City', 'Event',
                   'Conditions', "EventBefore", "ConditionBefore", 'Hour', 'Temperature', "Temp_Max", "Temp_Min",
                   "Monthly_Avg_Temp", "Daily_Avg_Temp", "Relative_Temp", 'Dewpoint', 'Humidity', 'Month', "Weekday",
                   'Visibility', "Cloud_Coverage", "Precipitation_Type", "Precipitation_Intensity",
                   "Precip_Intensity_Max", "Precip_Intensity_Time", "Clear", "Cloudy", "Rain", "Fog", "Snow", "RainBefore",
                   "Terrain", "Land_Use", "Access_Control", "Illumination", "Operation", "Speed_Limit", "Thru_Lanes",
                   "Num_Lanes", "Ad_Sys", "Gov_Cont", "Func_Class", "AADT", "DHV", "Pavement_Width", "Pavement_Type")
    results = results.reindex(columns=header_list)
    results.to_csv("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/New Data Files/New Accident Data.csv")


def get_hour_negatives(calldata):
    # Hour Negative Sampling #
    # Make a negative samples dataframe to hold the negative samples from calldata
    # By default, this file is empty
    negative_samples = pandas.read_csv(
        "/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/NegativeSamples.csv", sep=",")

    neg_loc = 0  # Used for positioning
    calldata.Time = calldata.Time.astype(str)
    calldata.Date = calldata.Date.astype(str)
    # For selecting a random hour, use random.choice on a list while excluding the particular hour from the range
    for i, info in enumerate(calldata.values):
        # Get the hour
        n = calldata.Hour.values[i]  # Number to remove from list of hours
        hours = range(0, 24)
        r = [x for x in hours if x != n]  # A list of numbers without n
        # Replace hour in calldata with a random hour
        calldata.Hour.values[i] = random.choice(r)
        # Check other entries if there's a match
        for n, checks in enumerate(calldata.values):  # Iterates through calldata checking for a match with i
            if calldata.Hour.values[n] == calldata.Hour.values[i] and \
                            calldata.Date.values[n] is calldata.Date.values[i]:
                # If match, skip
                pass
            else:
                new_hour = str(calldata.Hour.values[i])
                toa = calldata.Time.values[i]
                mioa = str(toa.split(':')[1])
                soa = str(toa.split(':')[2])
                new_time = new_hour + ":" + mioa + ":" + soa
                calldata.Date = calldata.Date.astype(datetime)
                # These values stay the same between calldata and the negative samples
                negative_samples.loc[neg_loc, "Latitude"] = calldata.Latitude.values[i]
                negative_samples.loc[neg_loc, "Longitude"] = calldata.Longitude.values[i]
                negative_samples.loc[neg_loc, "Date"] = calldata.Date.values[i]
                negative_samples.loc[neg_loc, "Time"] = new_time
                negative_samples.loc[neg_loc, "Hour"] = calldata.Hour.values[i]
                negative_samples.loc[neg_loc, "Address"] = calldata.Address.values[i]
                negative_samples.loc[neg_loc, "City"] = calldata.City.values[i]
                negative_samples.loc[neg_loc, "Route"] = calldata.Route.values[i]
                negative_samples.loc[neg_loc, "Log_Mile"] = calldata.Log_Mile.values[i]
                negative_samples.loc[neg_loc, "Terrain"] = calldata.Terrain.values[i]
                negative_samples.loc[neg_loc, "Land_Use"] = calldata.Land_Use.values[i]
                negative_samples.loc[neg_loc, "Access_Control"] = calldata.Access_Control.values[i]
                negative_samples.loc[neg_loc, "Illumination"] = calldata.Illumination.values[i]
                negative_samples.loc[neg_loc, "Operation"] = calldata.Operation.values[i]
                negative_samples.loc[neg_loc, "Speed_Limit"] = calldata.Speed_Limit.values[i]
                negative_samples.loc[neg_loc, "Thru_Lanes"] = calldata.Thru_Lanes.values[i]
                negative_samples.loc[neg_loc, "Num_Lanes"] = calldata.Num_Lanes.values[i]
                negative_samples.loc[neg_loc, "Ad_Sys"] = calldata.Ad_Sys.values[i]
                negative_samples.loc[neg_loc, "Gov_Cont"] = calldata.Gov_Cont.values[i]
                negative_samples.loc[neg_loc, "Func_Class"] = calldata.Func_Class.values[i]
                negative_samples.loc[neg_loc, "AADT"] = calldata.AADT.values[i]
                negative_samples.loc[neg_loc, "DHV"] = calldata.DHV.values[i]
                negative_samples.loc[neg_loc, "Pavement_Width"] = calldata.Pavement_Width.values[i]
                negative_samples.loc[neg_loc, "Pavement_Type"] = calldata.Pavement_Type.values[i]
                neg_loc = neg_loc + 1
                break
    traffic = pandas.read_csv(
        "/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/ETRIMS/Traffic_Count.csv",
        sep=",")

    print("Getting Hour NS Road Geometrics")
    for k, info in enumerate(negative_samples.values):
        for m, value in enumerate(traffic.values):
            if negative_samples.Route.values[k] == traffic.ID_NUMBER.values[m]:
                if traffic.ELM.values[m] > negative_samples.Log_Mile.values[k] > traffic.BLM.values[m]:
                    # negative_samples.AADT.values[k] = traffic.AADT.values[m]
                    negative_samples.DHV.values[k] = traffic.DHV.values[m]
    # Getting the weekday
    negative_samples['Date'] = pandas.to_datetime(negative_samples['Date'])
    negative_samples['Weekday'] = negative_samples['Date'].dt.dayofweek
    negative_samples.Date = negative_samples.Date.astype(str)

    print("Getting NS Hour Weather Data")
    negative_samples = get_weather_data(negative_samples)
    # Appending new data to the New Data file #
    print("Appending NS Hour Data")
    negative_samples = negative_samples.iloc[::-1]
    og_calldata = pandas.read_csv(
        folderpath + "Excel & CSV Sheets/New Data Files/New Negative Samples (Hour).csv", sep=",")
    frames = [og_calldata, negative_samples]
    results = pandas.concat(frames)
    header_list = (
        "Accident", 'Latitude', 'Longitude', 'Date', 'Time', 'Address', "Route", "Log_Mile", 'City', 'Event',
        'Conditions', "EventBefore", "ConditionBefore", 'Hour', 'Temperature', "Temp_Max", "Temp_Min",
        "Monthly_Avg_Temp", "Daily_Avg_Temp", "Relative_Temp", 'Dewpoint', 'Humidity', 'Month', "Weekday",
        'Visibility', "Cloud_Coverage", "Precipitation_Type", "Precipitation_Intensity",
        "Precip_Intensity_Max", "Precip_Intensity_Time", "Clear", "Cloudy", "Rain", "Fog", "Snow", "RainBefore",
        "Terrain", "Land_Use", "Access_Control", "Illumination", "Operation", "Speed_Limit", "Thru_Lanes",
        "Num_Lanes", "Ad_Sys", "Gov_Cont", "Func_Class", "AADT", "DHV", "Pavement_Width", "Pavement_Type")
    results = results.reindex(columns=header_list)
    results.to_csv(
        "/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/New Data Files/New Negative Samples (Hour).csv")


def get_date_negatives(calldata):
    # Get the Negative Samples for Date #
    # This file needs to be updated every day, and should have the date up until the day before the current day
    # so, if today is 10/18/2018, the last date in the file should be 10/17/2018
    day_holder2018 = pandas.read_excel(
        "/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/Day Holder 2018.xlsx")

    # Make a negative samples dataframe to hold the negative samples from calldata
    # By default, this file is empty
    negative_samples = pandas.read_csv(
        "/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/NegativeSamples.csv", sep=",")

    neg_loc = 0  # Used for positioning
    calldata.Date = calldata.Date.astype(str)
    day_holder2018.Date = day_holder2018.Date.astype(str)
    # For selecting a random day, use random.choice on a list while excluding the particular day from the range
    for i, info in enumerate(calldata.values):
        # Get the day
        doa = calldata.Date.values[i]  # Date of a 911 call
        day_num = pandas.to_datetime(doa).strftime('%-j')
        day_num = int(day_num) + 1
        # Note: When selecting the corresponding date from the excel file, it's the Day_Num value - 1 #
        # So, for the ranges, have them be from 0 to max Day_Num value + 1
        days_2017 = range(0, 365)
        # This variable needs to be updated for the current day, since 2018 is still going on
        days_2018 = range(0, 269)

        r_2017 = [x for x in days_2017 if x != day_num]  # A list of numbers without dayoa, covering the days in 2017
        r_2018 = [y for y in days_2018 if y != day_num]  # A list of numbers without dayoa, covering the days in 2018
        # Check to see what the year is; based on this, you use one of the above variables
        yoa = int(doa.split('-')[0])  # Get the year
        if yoa == 2018:
            calldata.Date.values[i] = day_holder2018.Date.values[random.choice(r_2018)]
        # Check other entries if there's a match
        for k, checks in enumerate(calldata.values):  # Iterates through calldata checking for a match with i
            if calldata.Date.values[k] == calldata.Date.values[i]:
                # If match, skip
                pass
            else:
                # print("No match found, negative sample added to new dataframe")
                calldata.Date = calldata.Date.astype(datetime)
                negative_samples.loc[neg_loc, "Latitude"] = calldata.Latitude.values[i]
                negative_samples.loc[neg_loc, "Longitude"] = calldata.Longitude.values[i]
                negative_samples.loc[neg_loc, "Date"] = calldata.Date.values[i]
                negative_samples.loc[neg_loc, "Time"] = calldata.Time.values[i]
                negative_samples.loc[neg_loc, "Hour"] = calldata.Hour.values[i]
                negative_samples.loc[neg_loc, "Address"] = calldata.Address.values[i]
                negative_samples.loc[neg_loc, "City"] = calldata.City.values[i]
                negative_samples.loc[neg_loc, "Route"] = calldata.Route.values[i]
                negative_samples.loc[neg_loc, "Log_Mile"] = calldata.Log_Mile.values[i]
                negative_samples.loc[neg_loc, "Terrain"] = calldata.Terrain.values[i]
                negative_samples.loc[neg_loc, "Land_Use"] = calldata.Land_Use.values[i]
                negative_samples.loc[neg_loc, "Access_Control"] = calldata.Access_Control.values[i]
                negative_samples.loc[neg_loc, "Illumination"] = calldata.Illumination.values[i]
                negative_samples.loc[neg_loc, "Operation"] = calldata.Operation.values[i]
                negative_samples.loc[neg_loc, "Speed_Limit"] = calldata.Speed_Limit.values[i]
                negative_samples.loc[neg_loc, "Thru_Lanes"] = calldata.Thru_Lanes.values[i]
                negative_samples.loc[neg_loc, "Num_Lanes"] = calldata.Num_Lanes.values[i]
                negative_samples.loc[neg_loc, "Ad_Sys"] = calldata.Ad_Sys.values[i]
                negative_samples.loc[neg_loc, "Gov_Cont"] = calldata.Gov_Cont.values[i]
                negative_samples.loc[neg_loc, "Func_Class"] = calldata.Func_Class.values[i]
                negative_samples.loc[neg_loc, "DHV"] = calldata.DHV.values[i]
                negative_samples.loc[neg_loc, "Pavement_Width"] = calldata.Pavement_Width.values[i]
                negative_samples.loc[neg_loc, "Pavement_Type"] = calldata.Pavement_Type.values[i]
                neg_loc = neg_loc + 1
                break
    traffic = pandas.read_csv(
        "/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/ETRIMS/Traffic_Count.csv",
        sep=",")
    print("Getting Date NS Road Geometrics")
    for k, info in enumerate(negative_samples.values):
        for m, value in enumerate(traffic.values):
            if negative_samples.Route.values[k] == traffic.ID_NUMBER.values[m]:
                if traffic.ELM.values[m] > negative_samples.Log_Mile.values[k] > traffic.BLM.values[m]:
                    negative_samples.AADT.values[k] = traffic.AADT.values[m]
                    negative_samples.DHV.values[k] = traffic.DHV.values[m]
    print("Getting Date NS Weather Data")
    negative_samples = get_weather_data(negative_samples)

    # Getting the weekday
    negative_samples['Date'] = pandas.to_datetime(negative_samples['Date'])
    negative_samples['Weekday'] = negative_samples['Date'].dt.dayofweek
    negative_samples.Date = negative_samples.Date.astype(str)

    # Appending new data to the New Data file #
    print("Appending Date NS Data")
    negative_samples = negative_samples.iloc[::-1]
    og_calldata = pandas.read_csv(
        folderpath + "Excel & CSV Sheets/New Data Files/New Negative Samples (Date).csv", sep=",")
    frames = [og_calldata, negative_samples]
    results = pandas.concat(frames)
    header_list = ("Accident", 'Latitude', 'Longitude', 'Date', 'Time', 'Address', "Route", "Log_Mile", 'City', 'Event',
                   'Conditions', "EventBefore", "ConditionBefore", 'Hour', 'Temperature', "Temp_Max", "Temp_Min",
                   "Monthly_Avg_Temp", "Daily_Avg_Temp", "Relative_Temp", 'Dewpoint', 'Humidity', 'Month', "Weekday",
                   'Visibility', "Cloud_Coverage", "Precipitation_Type", "Precipitation_Intensity",
                   "Precip_Intensity_Max", "Precip_Intensity_Time", "Clear", "Cloudy", "Rain", "Fog", "Snow",
                   "RainBefore",
                   "Terrain", "Land_Use", "Access_Control", "Illumination", "Operation", "Speed_Limit", "Thru_Lanes",
                   "Num_Lanes", "Ad_Sys", "Gov_Cont", "Func_Class", "AADT", "DHV", "Pavement_Width", "Pavement_Type")
    results = results.reindex(columns=header_list)
    results.to_csv(
        "/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/New Data Files/New Negative Samples (Date).csv")


# currently, the relative temperature variable has been dropped
def update_temp_avgs(day_holder2018):
    lat_coords = [35.421081, 35.153381, 35.006039, 35.150392, 35.301703, 35.185536]
    long_coords = [-85.121603, -85.121603, -85.175549, -85.047341, -84.998361, -85.158404]
    hour_times = [0, 6, 12, 18]
    coord_avgs = []
    # The key for using DarkSky API
    key = 'c9f5b49eab51e5a3a98bae35a9bcbb88'
    day_holder2018.Date = day_holder2018.Date.astype(str)

    print("Adding in DarkSky Weather")
    # Iterate through calldata and assign weather data for each incident
    for k, info in enumerate(day_holder2018.values):
        print(k)
        lat_iterator = 0
        hour_iterator = 0
        temp_avg = 0
        for j in range(0, 6):
            lat = lat_coords[lat_iterator]
            long = long_coords[lat_iterator]
            temp_avg = 0
            hour_iterator = 0
            for o in range(0, 4):
                hoa = hour_times[hour_iterator]
                mioa = 0
                soa = 0
                doa = day_holder2018.Date.values[k]
                yoa = int(doa.split('-')[0])
                moa = int(doa.split('-')[1])
                dayoa = int(doa.split('-')[2])
                # The following line needs to have this format:
                t = datetime(yoa, moa, dayoa, hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    # Hourly data
                    for i, value in enumerate(forecastcall.hourly):
                        if i == hoa:
                            temp_avg = temp_avg + value.temperature
                except:
                    print("Hourly Lookup Failed")
                hour_iterator = hour_iterator + 1
            lat_iterator = lat_iterator + 1
            temp_avg = temp_avg / 4
            coord_avgs.append(temp_avg)
            day_average = sum(coord_avgs) / len(coord_avgs)
            day_holder2018.Daily_Average.values[k] = day_average
    save_excel_file("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2017+2018 Data/Day Holder 2018.xlsx",
                    "Time and Temp", day_holder2018)


def get_weather_data(calldata):
    calldata.Event = calldata.Event.astype(str)
    calldata.Conditions = calldata.Conditions.astype(str)
    calldata.Precipitation_Type = calldata.Precipitation_Type.astype(str)
    calldata.Precipitation_Intensity = calldata.Precipitation_Intensity.astype(float)
    calldata.Precip_Intensity_Max = calldata.Precip_Intensity_Max.astype(float)
    calldata.Temp_Max = calldata.Temp_Max.astype(float)
    calldata.Temp_Min = calldata.Temp_Min.astype(float)
    calldata.Precip_Intensity_Time = calldata.Precip_Intensity_Time.astype(datetime)
    calldata.Latitude = calldata.Latitude.astype(float)
    calldata.Longitude = calldata.Longitude.astype(float)
    calldata.Time = calldata.Time.astype(str)
    calldata.Latitude = calldata.Latitude.astype(float)
    calldata.Longitude = calldata.Longitude.astype(float)
    calldata.EventBefore = calldata.EventBefore.astype(str)
    calldata.ConditionBefore = calldata.ConditionBefore.astype(str)
    # The key for using DarkSky API
    key = 'c9f5b49eab51e5a3a98bae35a9bcbb88'
    # Iterate through negative_samples and assign weather data for each incident
    for k, info in enumerate(calldata.values):
        # All variables are blank-of-accident, thus year is yoa.
        hoa = int(calldata.Hour.values[k])
        toa = calldata.Time.values[k]
        mioa = int(toa.split(':')[1])
        soa = int(toa.split(':')[2])
        doa = calldata.Date.values[k]
        yoa = int(doa.split('-')[0])
        moa = int(doa.split('-')[1])
        dayoa = int(doa.split('-')[2])
        lat = calldata.Latitude.values[k]
        long = calldata.Longitude.values[k]

        # The following line needs to have this format:
        t = datetime(yoa, moa, dayoa, hoa, mioa, soa).isoformat()
        call = key, lat, long

        # Retrieve the previous hour's weather event and conditions for each incident
        # A series of if statements to see what day of the year it is
        # If it is the first of the month, then we call the weather data for the last day of the previous month
        if hoa == 0 and dayoa == 1:  # If 1/1, get weather data from 12/31, reduce year by 1
            if moa == 1:
                new_hoa = 23
                new_dayoa = 31
                new_moa = 12
                new_yoa = yoa - 1
                # Get weather data
                # The following line needs to have this format:
                t = datetime(new_yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        calldata.EventBefore.values[k] = value.icon
                        calldata.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 2:  # If 2/1, get weather data from 1/31, same year
                new_hoa = 23
                new_dayoa = 31
                new_moa = 1
                # Get weather data
                # The following line needs to have this format:
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        calldata.EventBefore.values[k] = value.icon
                        calldata.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 3:  # If 3/1, get weather data from 2/28, same year
                new_hoa = 23
                new_dayoa = 28
                new_moa = 2
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        calldata.EventBefore.values[k] = value.icon
                        calldata.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 4:  # If 4/1, get weather data from 3/31, same year
                new_hoa = 23
                new_dayoa = 31
                new_moa = 3
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        calldata.EventBefore.values[k] = value.icon
                        calldata.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 5:  # If 5/1, get weather data from 4/30, same year
                new_hoa = 23
                new_dayoa = 30
                new_moa = 4
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        calldata.EventBefore.values[k] = value.icon
                        calldata.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 6:  # If 6/1, get weather data from 5/31, same year
                new_hoa = 23
                new_dayoa = 31
                new_moa = 5
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        calldata.EventBefore.values[k] = value.icon
                        calldata.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 7:  # If 7/1, get weather data from 6/30, same year
                new_hoa = 23
                new_dayoa = 30
                new_moa = 6
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        calldata.EventBefore.values[k] = value.icon
                        calldata.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 8:  # If 8/1, get weather data from 7/31, same year
                new_hoa = 23
                new_dayoa = 31
                new_moa = 7
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        calldata.EventBefore.values[k] = value.icon
                        calldata.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 9:  # If 9/1, get weather data from 8/31, same year
                new_hoa = 23
                new_dayoa = 31
                new_moa = 8
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        calldata.EventBefore.values[k] = value.icon
                        calldata.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 10:  # If 10/1, get weather data from 9/30, same year
                new_hoa = 23
                new_dayoa = 30
                new_moa = 9
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        calldata.EventBefore.values[k] = value.icon
                        calldata.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 11:  # If 11/1, get weather data from 10/31, same year
                new_hoa = 23
                new_dayoa = 31
                new_moa = 10
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        calldata.EventBefore.values[k] = value.icon
                        calldata.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            elif moa == 12:  # If 12/1, get weather data from 11/30, same year
                new_hoa = 23
                new_dayoa = 30
                new_moa = 11
                # Get weather data
                t = datetime(yoa, new_moa, new_dayoa, new_hoa, mioa, soa).isoformat()
                call = key, lat, long
                try:
                    forecastcall = forecast(*call, time=t)
                    for i, value in enumerate(forecastcall.hourly):
                        calldata.EventBefore.values[k] = value.icon
                        calldata.ConditionBefore.values[k] = value.summary
                except:
                    print("Error in finding previous hour")
            else:
                print("Error in calculating previous day")
        elif hoa == 0 and dayoa != 1:
            new_dayoa = dayoa - 1
            new_hoa = 23
            # Get weather data
            t = datetime(yoa, moa, new_dayoa, new_hoa, mioa, soa).isoformat()
            call = key, lat, long
            try:
                forecastcall = forecast(*call, time=t)
                for i, value in enumerate(forecastcall.hourly):
                    calldata.EventBefore.values[k] = value.icon
                    calldata.ConditionBefore.values[k] = value.summary
            except:
                print("Error in finding previous hour")
        elif hoa > 0:
            new_hoa = hoa - 1
            # Get weather data
            t = datetime(yoa, moa, dayoa, new_hoa, mioa, soa).isoformat()
            call = key, lat, long
            try:
                forecastcall = forecast(*call, time=t)
                for i, value in enumerate(forecastcall.hourly):
                    calldata.EventBefore.values[k] = value.icon
                    calldata.ConditionBefore.values[k] = value.summary
            except:
                print("Error in finding previous hour")
        else:
            print("One of the hours was 0 and didn't register")

        # Retrieve the main weather data
        try:
            forecastcall = forecast(*call, time=t)
            # Hourly data
            for i, value in enumerate(forecastcall.hourly):
                # Retrieving weather for previous weather
                if i == hoa:
                    calldata.Temperature.values[k] = value.temperature
                    calldata.Dewpoint.values[k] = value.dewPoint
                    calldata.Event.values[k] = value.icon
                    calldata.Humidity.values[k] = value.humidity
                    calldata.Month.values[k] = moa
                    calldata.Visibility.values[k] = value.visibility
                    calldata.Conditions.values[k] = value.summary
        except:
            print("Hourly Lookup Failed")
            # try:
            # Daily data, which requires individual try/except statements, otherwise the code crashes for some reason
        for j, value2 in enumerate(forecastcall.daily):
            try:
                calldata.Precipitation_Type.values[k] = value2.precipType
            except:
                calldata.Precipitation_Type.values[k] = "NA"
            try:
                calldata.Precipitation_Intensity.values[k] = value2.precipIntensity
            except:
                calldata.Precipitation_Intensity.values[k] = -1000
            try:
                calldata.Precip_Intensity_Max.values[k] = value2.precipIntensityMax
            except:
                calldata.Precip_Intensity_Max.values[k] = -1000
            try:
                calldata.Precip_Intensity_Time.values[k] = value2.precipIntensityMaxTime
            except:
                calldata.Precip_Intensity_Time.values[k] = -1000
            try:
                calldata.Temp_Max.values[k] = value2.temperatureMax
            except:
                calldata.Temp_Max.values[k] = -1000
            try:
                calldata.Temp_Min.values[k] = value2.temperatureMin
            except:
                calldata.Temp_Min.values[k] = -1000
            try:
                calldata.Cloud_Coverage.values[k] = value2.cloudCover
            except:
                calldata.Cloud_Coverage.values[k] = -1000

    for i, value in enumerate(calldata.values):
        if "clear" in calldata.Event.values[i] or "clear" in calldata.Conditions.values[
            i] \
                or "Clear" in calldata.Event.values[i] or "Clear" in \
                calldata.Conditions.values[i]:
            calldata.Clear.values[i] = 1
        else:
            calldata.Clear.values[i] = 0

        if "rain" in calldata.Event.values[i] or "rain" in calldata.Conditions.values[i] \
                or "Rain" in calldata.Event.values[i] or "Rain" in \
                calldata.Conditions.values[i] \
                or "Drizzle" in calldata.Event.values[i] or "Drizzle" in \
                calldata.Conditions.values[i] \
                or "drizzle" in calldata.Event.values[i] or "drizzle" in \
                calldata.Conditions.values[i]:
            calldata.Rain.values[i] = 1
        else:
            calldata.Rain.values[i] = 0

        if "snow" in calldata.Event.values[i] or "snow" in calldata.Conditions.values[i] \
                or "Snow" in calldata.Event.values[i] or "Snow" in \
                calldata.Conditions.values[i]:
            calldata.Snow.values[i] = 1
        else:
            calldata.Snow.values[i] = 0

        if "cloudy" in calldata.Event.values[i] or "cloudy" in \
                calldata.Conditions.values[i] \
                or "Cloudy" in calldata.Event.values[i] or "Cloudy" in \
                calldata.Conditions.values[i] \
                or "overcast" in calldata.Event.values[i] or "overcast" in \
                calldata.Conditions.values[i] \
                or "Overcast" in calldata.Event.values[i] or "Overcast" in \
                calldata.Conditions.values[
                    i]:
            calldata.Cloudy.values[i] = 1
        else:
            calldata.Cloudy.values[i] = 0

        if "fog" in calldata.Event.values[i] or "foggy" in calldata.Conditions.values[i] \
                or "Fog" in calldata.Event.values[i] or "Foggy" in \
                calldata.Conditions.values[i]:
            calldata.Fog.values[i] = 1
        else:
            calldata.Fog.values[i] = 0
        if "rain" in calldata.EventBefore.values[i] or "rain" in \
                calldata.ConditionBefore.values[i] \
                or "Rain" in calldata.EventBefore.values[i] or "Rain" in \
                calldata.ConditionBefore.values[i]:
            calldata.RainBefore.values[i] = 1
        else:
            calldata.RainBefore.values[i] = 0
    return calldata


def main():
    # This line should be run each morning around 9:10 AM
    calldata, file = get_Email()

    # Here are the current dtypes for reading in a file #
    # calldata = pandas.read_excel(folderpath + "Excel & CSV Sheets/2018 Data/911_Reports_for_2018-09-26_FinalForm.xlsx",
    #         dtypes={"Accident": int, "Problem": str, "Latitude": float, "Longitude": float, 'Date': datetime,
    #                 'Time': datetime.time, "Address": str, "Route": str, "Log_Mile": float, "City": str, 'Event': str,
    #                 'Conditions': str, "EventBefore": str, "ConditionBefore": str, 'Hour': int, 'Temperature': float,
    #                 "Temp_Max": float, "Temp_Min": float, "Monthly_Avg_Temp": float, "Daily_Avg_Temp": str,
    #                 "Relative_Temp": float, "Dewpoint": float, 'Humidity': float, "Month": int, "Weekday": int,
    #                 'Visibility': float, "Cloud_Coverage": float, "Precipitation_Type": str,
    #                 "Precipitation_Intensity": float, "Precip_Intensity_Max": float, "Precip_Intensity_Time": float,
    #                 "Clear": int, "Cloudy": int, "Rain": int, "Fog": int, "Snow": int, "RainBefore": int,
    #                 "Terrain": int, "Land_Use": int, "Access_Control": int, "Illumination": int, "Operation": int,
    #                 "Speed_Limit": int, "Thru_Lanes": int, "Num_Lanes": int, "Ad_Sys": int, "Gov_Cont": int,
    #                 "Func_Class": int, "AADT": int, "DHV": int, "Pavement_Width": int, "Pavement_Type": str})

    # Reading file directly for testing
    # file = folderpath + ""
    # calldata = pandas.read_csv(file, sep=",")

    calldata.Latitude = calldata.Latitude.astype(float)
    calldata.Longitude = calldata.Longitude.astype(float)
    print("Fixing These Stupid Lat and Long Coordinates")
    for k, info in enumerate(calldata.values):
        if calldata.Latitude.values[k] > 40:
            calldata.Latitude.values[k] = float(calldata.Latitude.values[k] / 1000000)
            calldata.Longitude.values[k] = float(calldata.Longitude.values[k] / -1000000)

    # Specific save names for files
    # This makes the saving process less tedious since we don't have to change the name of the file we're saving
    # every time we read a new file
    # We save the file multiple times throughout the process of working with it so if an error occurs, we don't have to
    # start from the very beginning
    dayname_csv = file.split("/")[-1]
    dayname_xlsx = dayname_csv.split(".")[0]

    # Removing the excess text from the problem column
    calldata = clean_problems(calldata)

    # Splitting and tidying the Response Date to the accident.
    calldata = split_datetime(calldata)

    # Reset the Column names for the data
    calldata = calldata.drop(['Response_Date', 'Fixed_Time_CallClosed'], axis=1)

    header_list = ("Accident", "Problem", 'Latitude', 'Longitude', 'Date', 'Time', 'Address', "Route", "Log_Mile", 'City', 'Event',
                   'Conditions', "EventBefore", "ConditionBefore", 'Hour', 'Temperature', "Temp_Max", "Temp_Min",
                   "Monthly_Avg_Temp", "Daily_Avg_Temp", "Relative_Temp", 'Dewpoint', 'Humidity', 'Month', "Weekday",
                   'Visibility', "Cloud_Coverage", "Precipitation_Type", "Precipitation_Intensity",
                   "Precip_Intensity_Max", "Precip_Intensity_Time", "Clear", "Cloudy", "Rain", "Fog", "Snow", "RainBefore",
                   "Terrain", "Land_Use", "Access_Control", "Illumination", "Operation", "Speed_Limit", "Thru_Lanes",
                   "Num_Lanes", "Ad_Sys", "Gov_Cont", "Func_Class", "AADT", "DHV", "Pavement_Width", "Pavement_Type")

    calldata.index.name = "Index"
    calldata = calldata.reindex(columns=header_list)

    # Create a list of different accident types for finding Y
    occurrence_list = ['Unknown Injuries', 'Delayed', 'No Injuries', 'Injuries', 'Entrapment', 'Mass Casualty']
    # Find the duplicate calls and drop them
    find_Duplicates(calldata, occurrence_list)
    calldata = drop_duplicates(calldata)

    # Add weather and road geometric data to calldata
    calldata = add_data(calldata, dayname_xlsx)

    # Save the calldata in its final form, just in case the appending goes wrong
    # save_excel_file(folderpath + "Excel & CSV Sheets/2018 Data/" + dayname_xlsx + "_FinalForm.xlsx",
    #                 "FinalSave", calldata)

    # Append the new data
    append_data(calldata)
    # Get the negative samples of the calldata
    # Each of these methods also gets the updated weather information
    get_hour_negatives(calldata)
    get_date_negatives(calldata)

if __name__ == "__main__":
    main()