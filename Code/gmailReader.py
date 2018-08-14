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
    count_doubles = 0
    data_file_copy = data_file_name.copy()
    remove = pandas.DataFrame(columns= data_file_copy.columns)
    # id1 = 0
    # id2 = data_file_copy.index[id1 + 1]
    for id1, id in enumerate(data_file_copy.values):
        print(id1)
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


# Getting the y for the incidents
def find_y(calldata):
    for i, value in enumerate(calldata.values):
        # if 'No Injuries' in calldata.loc[i, 'Problem'] or 'Unknown Injuries' in calldata.loc[
        #     i, 'Problem'] or 'Delayed' in calldata.loc[i, 'Problem']:
        if 'No Injuries' in calldata.Problem.values[i] or 'Unknown Injuries' in calldata.Problem.values[i] or\
                        'Delayed' in calldata.Problem.values[i]:
            calldata.Y.values[i] = 0
        else:
            calldata.Y.values[i] = 1
    return calldata


def append_data(calldata):
    # Appending new data to 2018+2017 File #
    calldata = calldata.iloc[::-1]
    og_calldata = pandas.read_excel(
        folderpath + "Excel & CSV Sheets/2017+2018 Data/2018 + 2017 Full Data.xlsx",
        dtypes={"Index": int, "Y": int, 'Latitude': float, 'Longitude': float, 'Date': datetime,
                'Time': datetime.time, 'Problem': str, 'Hour': int, 'Address': str, 'City': str,
                'Temperature': float, "Temp_Max": float, "Temp_Min": float, 'Dewpoint': float, 'Event': str,
                'Humidity': float, 'Month': int, 'Visibility': float, 'Conditions': str, "Cloud_Coverage": float,
                "Precipitation_Type": str, "Precipitation_Intensity": float, "Precip_Intensity_Max": float,
                "Precip_Intensity_Time": float, "EventBefore": str, "ConditionBefore": str})
    frames = [og_calldata, calldata]
    results = pandas.concat(frames)
    header_list = ("Y", 'Latitude', 'Longitude', 'Date', 'Time', 'Problem', 'Address', 'City', 'Event', 'Conditions',
                   "EventBefore", "ConditionBefore", 'Hour', 'Temperature', "Temp_Max", "Temp_Min", 'Dewpoint',
                   'Humidity', 'Month', 'Visibility', "Cloud_Coverage", "Precipitation_Type", "Precipitation_Intensity",
                   "Precip_Intensity_Max", "Precip_Intensity_Time")
    results = results.reindex(columns=header_list)
    # # Saving new data to 2018+2017 File #
    save_excel_file(folderpath + "Excel & CSV Sheets/2017+2018 Data/2018 + 2017 Full Data.xlsx",
                    "DarkSky Weather", results)



def main():

    # Run this line each morning
    # calldata, file = get_Email()

    # Reading file directly for testing
    file = folderpath + "Excel & CSV Sheets/2018 Data/DailyReports/911_Reports_for_2018-08-13.csv"
    calldata = pandas.read_csv(file, sep=",")
    # calldata = pandas.read_excel(file)

    # Use for reading csv versions of calldata #
    # calldata = pandas.read_csv(file, sep=",", dtype={"Index": int, "Y": int, 'Latitude': float, 'Longitude': float,
    #                                                  'Date': str, 'Time': str, 'Problem': str, 'Hour': int,
    #                                                  'Address': str, 'City': str, 'Temperature': float,
    #                                                  'Dewpoint': float, 'Event': str, 'Humidity': float, 'Month': int,
    #                                                  'Visibility': float, 'Conditions': str, "EventBefore": str,
    #                                                  "ConditionBefore": str})

    # Use for reading xlsx versions of calldata #
    # calldata = pandas.read_excel(file, dtypes={"Index": int, "Y": int, 'Latitude': float, 'Longitude': float,
    #                                            'Date': datetime, 'Time': datetime.time, 'Problem': str, 'Hour': int,
    #                                            'Address': str, 'City': str, 'Temperature': float, "Temp_Max": float,
    #                                            "Temp_Min": float, 'Dewpoint': float, 'Event': str, 'Humidity': float,
    #                                            'Month': int, 'Visibility': float, 'Conditions': str,
    #                                            "Cloud_Coverage": float, "Precipitation_Type": str,
    #                                            "Precipitation_Intensity": float, "Precip_Intensity_Max": float,
    #                                            "Precip_Intensity_Time": datetime.time, "EventBefore": str,
    #                                            "ConditionBefore": str})

    dayname_csv = file.split("/")[-1]
    dayname_xlsx = dayname_csv.split(".")[0]

    # Removing the excess text from the problem column.
    calldata = clean_problems(calldata)

    # Splitting and tidying the Response Date to the accident.
    calldata = split_datetime(calldata)

    calldata = calldata.drop(['Response_Date', 'Fixed_Time_CallClosed'], axis=1)

    header_list = ("Y", 'Latitude', 'Longitude', 'Date', 'Time', 'Problem', 'Address', 'City', 'Event', 'Conditions',
                   'Hour', 'Temperature', "Temp_Max", "Temp_Min", 'Dewpoint', 'Humidity', 'Month', 'Visibility',
                   "Cloud_Coverage", "Precipitation_Type", "Precipitation_Intensity", "Precip_Intensity_Max",
                   "Precip_Intensity_Time", "EventBefore", "ConditionBefore")

    calldata.index.name = "Index"
    calldata = calldata.reindex(columns=header_list)

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
    calldata.Date = calldata.Date.astype(str)
    calldata.Time = calldata.Time.astype(str)
    calldata.Latitude = calldata.Latitude.astype(float)
    calldata.Longitude = calldata.Longitude.astype(float)
    calldata.EventBefore = calldata.EventBefore.astype(str)
    calldata.ConditionBefore = calldata.ConditionBefore.astype(str)

    for k, info in enumerate(calldata.values):
        if calldata.Latitude.values[k] > 40:
            calldata.Latitude.values[k] = (calldata.Latitude.values[k] / 1000000)
            calldata.Longitude.values[k] = (calldata.Longitude.values[k] / -1000000)

    key = 'c9f5b49eab51e5a3a98bae35a9bcbb88'

    for k, info in enumerate(calldata.values):
        print(k)
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

        try:
            forecastcall = forecast(*call, time=t)
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
                    calldata.Precipitation_Intensity_Time.values[k] = -1000
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
        except:
            print("There was an exception")
            pass

    save_excel_file(folderpath + "Excel & CSV Sheets/2018 Data/" + dayname_xlsx + ".xlsx",
                    "DarkSky Weather", calldata)

    occurrence_list = ['Unknown Injuries', 'Delayed', 'No Injuries', 'Injuries', 'Entrapment', 'Mass Casualty']

    calldata = pandas.read_excel(folderpath + "Excel & CSV Sheets/2018 Data/"+ dayname_xlsx + ".xlsx",
        dtypes={"Index": int, "Y": int, 'Latitude': float, 'Longitude': float, 'Date': datetime,
                'Time': datetime.time, 'Problem': str, 'Hour': int, 'Address': str, 'City': str,
                'Temperature': float, "Temp_Max": float, "Temp_Min": float, 'Dewpoint': float, 'Event': str,
                'Humidity': float, 'Month': int, 'Visibility': float, 'Conditions': str, "Cloud_Coverage": float,
                "Precipitation_Type": str, "Precipitation_Intensity": float, "Precip_Intensity_Max": float,
                "Precip_Intensity_Time": float, "EventBefore": str, "ConditionBefore": str})

    find_Duplicates(calldata, occurrence_list)
    calldata = drop_duplicates(calldata)

    save_excel_file(folderpath + "Excel & CSV Sheets/2018 Data/"+ dayname_xlsx + "_Dropped_Dupes.xlsx",
                    "DarkSky Weather", calldata)

    calldata = pandas.read_excel(folderpath + "Excel & CSV Sheets/2018 Data/"
        + dayname_xlsx + "_Dropped_Dupes.xlsx",
        dtypes={"Index": int, "Y": int, 'Latitude': float, 'Longitude': float, 'Date': datetime,
                'Time': datetime.time, 'Problem': str, 'Hour': int, 'Address': str, 'City': str,
                'Temperature': float, "Temp_Max": float, "Temp_Min": float, 'Dewpoint': float, 'Event': str,
                'Humidity': float, 'Month': int, 'Visibility': float, 'Conditions': str, "Cloud_Coverage": float,
                "Precipitation_Type": str, "Precipitation_Intensity": float, "Precip_Intensity_Max": float,
                "Precip_Intensity_Time": float, "EventBefore": str, "ConditionBefore": str})

    calldata = find_y(calldata)

    save_excel_file(folderpath + "Excel & CSV Sheets/2018 Data/"
                    + dayname_xlsx + "_FinalForm.xlsx", "DarkSky Weather", calldata)

    # Use this calldata for reading in 1 specific file for appending
    # calldata = pandas.read_excel(folderpath + "")

    append_data(calldata)

if __name__ == "__main__":
    main()