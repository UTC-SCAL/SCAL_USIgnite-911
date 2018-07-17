import email
import imaplib
import os
from datetime import datetime, timedelta, date
from darksky import forecast
import pytz
import pandas
import math
from openpyxl import load_workbook
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows


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
                        sv_path = os.path.join('/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/DailyReports/911_Reports_for_'+ str(daybefore)+'.csv')
                        if not os.path.isfile(sv_path):
                            # print(sv_path)
                            fp = open(sv_path, 'wb')
                            fp.write(part.get_payload(decode=True))
                            fp.close()
    file = '/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/DailyReports/911_Reports_for_' + str(daybefore) + '.csv'
    calllog = pandas.read_csv(file,sep=",")
    return calllog, file


def split_datetime(calldata):

    for i, value in enumerate(calldata.values):
        header_list = ('Response_Date', 'Fixed_Time_CallClosed', 'Address', 'City',
                       'Latitude','Longitude' ,'Problem', 'Date','Time','Hour' )
        calldata = calldata.reindex(columns=header_list)
        # next three lines are a necessary workaround due to pandas error
        calldata.Date = calldata.Date.astype(str)
        calldata.Time = calldata.Time.astype(str)
        calldata.Hour = calldata.Hour.astype(str)

        # date = datetime.strptime(calldata.Response_Date.values[i], '%m/%d/%Y %I:%M:%S %p')
        dateof = datetime.strptime(calldata.Response_Date.values[i], '%m/%d/%Y %H:%M:%S %p')


        calldata.Date.values[i] = str(dateof.date())
        calldata.Time.values[i] = str(dateof.time())
        calldata.Hour.values[i] = dateof.hour
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
    print(calldata.values[0:5])
    datafile = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/DailyReports/ToRemoveFile.xlsx")
    listing = list(datafile.Index.values)
    for i in listing:
        print(i)
    calldata.drop(calldata.index[listing], inplace=True)
    print(calldata.values[0:5])
    return calldata


def find_Duplicates(data_file_name, occurrence_list):
    count_doubles = 0
    data_file_copy = data_file_name.copy()
    remove = pandas.DataFrame(columns= data_file_copy.columns)
    # id1 = 0
    # id2 = data_file_copy.index[id1 + 1]
    for id1, id in enumerate(data_file_copy.values):
        if id1 + 1 >= len(data_file_copy)-1:
            print("There were :", count_doubles, "occurrences of duplicate calls.")
            save_excel_file('/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/DailyReports/ToRemoveFile.xlsx',
                            'Call Info', remove)
            break
        else:
            id2 = data_file_copy.index[id1 + 1]
            # print(id1, id2)
            # print(data_file_copy.Time[id1])
            time1 = datetime.strptime(data_file_copy.Time.values[id1], '%H:%M:%S').time()
            time2 = datetime.strptime(data_file_copy.Time.values[id2], '%H:%M:%S').time()
            duration = datetime.combine(date.min, time2) - datetime.combine(date.min, time1)
            duration = duration.total_seconds()
            minutes = math.fabs(duration / 60.0)
            if minutes < 4:
                lat1= (int(data_file_copy.Latitude[id1]) / 1000000)
                long1 = (int(data_file_copy.Longitude[id1]) / 1000000)
                lat2 = (int(data_file_copy.Latitude[id2]) / 1000000)
                long2 = (int(data_file_copy.Longitude[id2]) / 1000000)
                latChange = math.fabs(lat1 - lat2)
                longChange = math.fabs(long1 - long2)
                if latChange < 0.0001 and longChange < 0.0001:
                    count_doubles += 1
                    problem1 = data_file_copy.Problem[id1].lstrip()
                    problem2 = data_file_copy.Problem[id2].lstrip()
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
    og_calldata = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/2018 Accident Report List.xlsx")
    frames = [og_calldata, calldata]
    results = pandas.concat(frames)

    save_excel_file("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/2018 Accident Report List.xlsx",
                    "DarkSky Weather", results)



def main():
    # Run this line each morning
    calldata, file = get_Email()
    #
    # # Reading file directly for testing.
    # # file = ""
    # # calldata = pandas.read_csv(file, sep=",")
    #
    # dayname_csv = file.split("/")[-1]
    # dayname_xlsx = dayname_csv.split(".")[0]
    #
    # # Removing the excess text from the problem column.
    # calldata = clean_problems(calldata)
    #
    # # Splitting and tidying the Response Date to the accident.
    # calldata = split_datetime(calldata)
    #
    # # calldata = calldata.drop(['Response_Date', 'Fixed_Time_CallClosed'], axis=1)
    # header_list = ("Y", 'Latitude', 'Longitude', 'Date', 'Time', 'Problem', 'Address', 'City', 'Event', 'Conditions',
    #                'Hour', 'Temperature', 'Dewpoint', 'Humidity', 'Visibility')
    #
    # calldata.index.name = "Index"
    # calldata = calldata.reindex(columns=header_list)
    #
    # calldata.Event = calldata.Temperature.astype(str)
    # calldata.Conditions = calldata.Dewpoint.astype(str)
    #
    # key = 'c9f5b49eab51e5a3a98bae35a9bcbb88'
    #
    # for k, info in enumerate(calldata.values):
    #     # All variables are blank-of-accident, thus year is yoa.
    #     hoa = int(calldata.Hour.values[k])
    #     toa = calldata.Time.values[k]
    #     moa = int(toa.split(':')[1])
    #     soa = int(toa.split(':')[2])
    #     doa = calldata.Date.values[k]
    #     yoa = int(doa.split('-')[0])
    #     moa = int(doa.split('-')[1])
    #     doa = int(doa.split('-')[2])
    #     lat = (calldata.Latitude.values[k] / 1000000)
    #     long = (calldata.Longitude.values[k] / -1000000)
    #
    #     # The following line needs to have this format:
    #     t = datetime(yoa, moa, doa, hoa, moa, soa).isoformat()
    #     call = key, lat, long
    #     # print(call)
    #     forecastcall = forecast(*call, time=t)
    #     # print(forecastcall)
    #     try:
    #         for i, value in enumerate(forecastcall.hourly):
    #             if i == hoa:
    #                 # These two lines take in unix time and make it readable by peoplefolk
    #                 # tz = pytz.timezone('America/New_York')
    #                 # dt = datetime.fromtimestamp(value.time, tz)
    #                 calldata.Temperature.values[k] = value.temperature
    #                 calldata.Dewpoint.values[k] = value.dewPoint
    #                 calldata.Event.values[k] = value.icon
    #                 calldata.Humidity.values[k] = value.humidity
    #                 calldata.Visibility.values[k] = value.visibility
    #                 calldata.Conditions.values[k] = value.summary
    #     except:
    #         pass
    # save_excel_file("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/" + dayname_xlsx + ".xlsx",
    #                 "DarkSky Weather", calldata)
    #
    # # Here, run the above code first, then run the below code after adjusting placement of index in the xlsx file #
    #
    # occurrence_list = ['Unknown Injuries', 'Delayed', 'No Injuries', 'Injuries', 'Entrapment', 'Mass Casualty']
    #
    # calldata = pandas.read_excel(
    #     "/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/"
    #     + dayname_xlsx + ".xlsx",
    #     dtypes={"Index": int, "Y": int, 'Latitude': float, 'Longitude': float, 'Date': datetime,
    #             'Time': datetime.time, 'Problem': str, 'Hour': int, 'Address': str, 'City': str,
    #             'Temperature': float, 'Dewpoint': float, 'Event': str, 'Humidity': float,
    #             'Visibility': float, 'Conditions': str})
    #
    # find_Duplicates(calldata, occurrence_list)
    # calldata = drop_duplicates(calldata)
    #
    # save_excel_file("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/"
    #                 + dayname_xlsx + "_Dropped_Dupes.xlsx",
    #                 "DarkSky Weather", calldata)
    #
    # calldata = pandas.read_excel(
    #     "/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/"
    #     + dayname_xlsx + "_Dropped_Dupes.xlsx",
    #     dtypes={"Index": int, "Y": int, 'Latitude': float, 'Longitude': float, 'Date': datetime,
    #             'Time': datetime.time, 'Problem': str, 'Hour': int, 'Address': str, 'City': str,
    #             'Temperature': float, 'Dewpoint': float, 'Event': str, 'Humidity': float,
    #             'Visibility': float, 'Conditions': str})
    #
    # calldata = pandas.read_excel("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/"
    #                              + dayname_xlsx + "_Dropped_Dupes.xlsx")
    # calldata = find_y(calldata)
    #
    # save_excel_file("/home/admin/PycharmProjects/RolandProjects/Excel & CSV Sheets/2018 Data/"
    #                 + dayname_xlsx + "_FinalForm.xlsx", "DarkSky Weather", calldata)
    #
    # # Use this calldata for reading in 1 specific file for appending
    # # calldata = pandas.read_excel("")
    # for k, info in enumerate(calldata.values):
    #     calldata.Latitude.values[k] = (calldata.Latitude.values[k] / 1000000)
    #     calldata.Longitude.values[k] = (calldata.Longitude.values[k] / -1000000)
    # append_data(calldata)

if __name__ == "__main__":
    main()