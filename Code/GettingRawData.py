
import pandas
import numpy
import time
import math
import geopy.distance
import imaplib
import email
import os
from io import StringIO
from charset_normalizer import detect
from geopy.geocoders import Nominatim
from datetime import timedelta
import swifter
import base64


def pull_emails(total, lastday):
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login('utcscal2018@gmail.com', 'EMCS 335')
    m.select("INBOX")  # here you a can choose a mail box like INBOX instead

    # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
    _, items = m.search(None, "ALL")
    items = items[0].split()  # getting the mails id

    for emailid in items:
        # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
        _, data = m.fetch(emailid, "(RFC822)")
        email_body = data[0][1]  # getting the mail content
        mail = email.message_from_bytes(email_body)
    # Check if any attachments at all
        dateofemail = mail["Date"]
        dateofemail = (email.utils.parsedate_to_datetime(dateofemail)).date()
        if dateofemail > lastday:
            if mail["From"] == '<reports@hc911.org>' and 'Accident Report was executed for HC911' in mail["Subject"]:
                if mail.get_content_maintype() != 'multipart':
                    continue
                # we use walk to create a generator so we can iterate on the parts and forget about the recursive headache
                for part in mail.walk():
                    # multipart are just containers, so we skip them
                    if part.get_content_maintype() == 'multipart':
                        continue

                    # # is this part an attachment ?
                    if part.get('Content-Disposition') is None:
                        continue
                    try:
                        encode = detect(part.get_payload(decode=True))[
                            'encoding']
                        data = str(part.get_payload(decode=True), encode)
                        data = StringIO(data)
                        daypart = pandas.read_csv(data)
                        print("CSV File:", dateofemail, lastday,
                              mail["Subject"], len(total))
                    except:
                        print("Excel File:", dateofemail, lastday,
                              mail["Subject"], len(total))
                        
                        # Clean up the old tmp file from disk:
                        filename = "tmp.xlsx"
                        if os.path.exists(filename):
                            os.remove(filename)

                        with open(filename, "wb") as file:
                            file.write(part.get_payload(decode=True))

                        daypart = pandas.read_excel(filename)

                    daypart['Unix'] = daypart.apply(lambda x: pandas.datetime.strptime(
                        str(x['Response Date']), "%Y-%m-%d %H:%M:%S"), axis=1)
                    daypart['Unix'] = daypart.apply(
                        lambda x: x.Unix.strftime('%s'), axis=1)
                    daypart['Latitude'] = daypart["Latitude"]/1000000
                    daypart['Longitude'] = daypart["Longitude"]/-1000000
                    daypart['Coords'] = (daypart["Latitude"]).map(str) + " , " + (daypart["Longitude"]/).map(str)
                    total = pandas.concat([total, daypart])
        else:
            print("...Looking for new accident reports")
    return total


def fill_empty_latlongs(x):
    i = x[0]
    try:
        location = geolocator.geocode(x.Address)
        add.Latitude.values[i] = location.latitude
        add.Longitude.values[i] = location.longitude
        print(i, add.Latitude[i], add.Longitude[i])
    # exit()
    # return add
    except:
        print(i)
        pass


def main():
    start = time.time()

    total = pandas.read_csv(
        "Excel & CSV Sheets/Accidents/RawAccidentDataTest.csv", parse_dates=['Response Date'])
    lastday = pandas.Timestamp(
        total['Response Date'].values[-1]).date() + timedelta(days=1)

    total = pull_emails(total, lastday)
    total.to_csv(
        "Excel & CSV Sheets/Accidents/RawAccidentDataTest.csv", index=False)


if __name__ == "__main__":
    main()
