import geolocator as geolocator
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
import base64
import geopandas
from geopandas.tools import sjoin
from datetime import datetime


def clear():
    os.system( 'clear' )


def pull_emails(total, lastday):
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login('utcscal2018@gmail.com', 'EMCS 335')
    m.select("INBOX")  # here you a can choose a mail box like INBOX instead
    lookfor = "UNANSWERED SENTSINCE "+str(lastday.strftime("%d-%b-%Y"))
    # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
    _, items = m.search(None, lookfor)
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
                    try: 
                        daypart['Unix'] = daypart.apply(lambda x: datetime.strptime(
                            str(x['Response Date']), "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S"), axis=1)

                    except: 
                        try:
                            daypart['Unix'] = daypart.apply(lambda x: datetime.strptime(
                            str(x['Response Date']), "%Y-%m-%d %H:%M:%S"), axis=1)
                        except: 
                            try: 
                                daypart[['Response Date', _]] = daypart['Response Date'].apply(lambda x: pandas.Series(str(x).split(".")))
                                daypart['Unix'] = daypart.apply(lambda x: datetime.strptime(
                                    str(x['Response Date']), "%Y-%m-%d %H:%M:%S"), axis=1)
                            except Exception as e:
                                print(e)
                                exit()


                        
                    daypart['Unix'] = daypart.apply(
                        lambda x: x.Unix.strftime('%s'), axis=1)
                    daypart['Latitude'] = daypart["Latitude"]/1000000
                    daypart['Longitude'] = daypart["Longitude"]/-1000000
                    # daypart['Coords'] = (daypart["Latitude"]).map(str) + " , " + (daypart["Longitude"]).map(str)
                    total = pandas.concat([total, daypart])
        else:
            clear()
            print("...Looking for new accident reports, ", dateofemail)
    if os.path.exists("tmp.xlsx"):
        os.remove("tmp.xlsx")
    return total


# def fill_empty_latlongs(x):
#     i = x[0]
#     try:
#         location = geolocator.geocode(x.Address)
#         add.Latitude.values[i] = location.latitude
#         add.Longitude.values[i] = location.longitude
#         print(i, add.Latitude[i], add.Longitude[i])
#     # exit()
#     # return add
#     except:
#         print(i)
#         pass


# This requires a shapefile. Different than the previous process, but requires less work beforehand


def add_grid_to_accidents_sf(accpath, hexpath, savepath):
    point = geopandas.GeoDataFrame.from_file(accpath) 
    poly = geopandas.GeoDataFrame.from_file(hexpath)
    pointInPolys = sjoin(point, poly)
    del pointInPolys['index_right']
    gridinfo = pandas.read_csv("Excel & CSV Sheets/Hamilton County Accident System Hex/Hex_Grid/HexGridInfoComplete.csv")
    newdata = pandas.merge(pointInPolys, gridinfo,
                           on=['GRID_ID', 'Join_Count'])
    newdata.to_csv(savepath, index=False)


def main():
    start = time.time()

    total = pandas.read_csv(
        "Excel & CSV Sheets/Grid Hex Layout/Accidents/RawAccidentData.csv")
    lastday = pandas.Timestamp(
        total['Response Date'].values[-1]).date() + timedelta(days=1)

    total = pull_emails(total, lastday)
    total.to_csv(
        "Excel & CSV Sheets/Grid Hex Layout/Accidents/RawAccidentData_Test.csv", index=False)


    # hexpath = '/Users/peteway/Documents/GitHub/SCAL_USIgnite-911/Excel & CSV Sheets/Shapefiles/Rework_HexGridpoint2sqmi/HexGrid.shp'
    # accpath = 'Excel & CSV Sheets/Shapefiles/New 911 Accident Shapefiles/Accidents_Full.shp'
    # savepath = 'Excel & CSV Sheets/Hamilton County Accident System Hex/Accidents/AccidentHex.csv'
    # add_grid_to_accidents_sf(accpath, hexpath, savepath)

    print("Total Process time:", time.time() - start)


if __name__ == "__main__":
    main()
