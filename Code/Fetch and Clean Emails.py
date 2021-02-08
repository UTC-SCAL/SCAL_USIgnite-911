"""
Author: Pete Way and Jin Cho
Editor: Jeremy Roland
Purpose: A combined file of GettingRawData.py and New_Drop_Duplicates.py. This was made to make it easier to have
    the code running each day on the MDRB servers to fetch and clean emails. The way I combined them may not be the
    most efficient, but some of the other methods I tried were having issues.
"""
import pandas
import imaplib
import email
import os
from io import StringIO
from charset_normalizer import detect
from datetime import timedelta, timezone
import geopandas
from geopandas.tools import sjoin
from datetime import datetime
import geopy.distance
import time
from shapely.geometry import Point, Polygon


def clear():
    os.system('clear')


# Match up accidents to their grid numbers
def matchAccidentToGridNum(accDataFile):
    accDataFile['Grid_Num'] = -1
    hexShapeFile = pandas.read_csv("../Main Dir/Shapefiles/HexGrid Shape Data.csv")
    # Iterate over our accidents
    for j, _ in enumerate(accDataFile.values):
        # Our accident GPS coords as a Point object
        accPoint = Point(accDataFile.Longitude.values[j], accDataFile.Latitude.values[j])
        # Iterate over our grid hexes
        for i, _ in enumerate(hexShapeFile.values):
            latList = hexShapeFile.Latitudes.values[i].split(",")
            longList = hexShapeFile.Longitudes.values[i].split(",")
            longList = list(map(lambda x: float(x), longList))
            latList = list(map(lambda x: float(x), latList))
            # A polygon object made of the GPS coords of the hex shape
            gridHex = Polygon(zip(longList, latList))
            # Check if the accident point object is within the hex shape polygon
            if accPoint.within(gridHex):
                accDataFile.Grid_Num.values[j] = hexShapeFile.Grid_Num.values[i]
                break
    return accDataFile


def pull_emails(total, lastday):
    """
    This method was made by Jin to actually fetch the accident files from the email
    """
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login('utcscal2018@gmail.com', 'EMCS 335')
    m.select("INBOX")  # here you a can choose a mail box like INBOX instead
    lookfor = "UNANSWERED SENTSINCE " + str(lastday.strftime("%d-%b-%Y"))
    # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
    _, items = m.search(None, lookfor)
    items = items[0].split()  # getting the mails id
    saveDF = pandas.DataFrame(columns=total.columns)  # dataframe to save our newly fetched accident records

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
                                daypart[['Response Date', _]] = daypart['Response Date'].apply(
                                    lambda x: pandas.Series(str(x).split(".")))
                                daypart['Unix'] = daypart.apply(lambda x: datetime.strptime(
                                    str(x['Response Date']), "%Y-%m-%d %H:%M:%S"), axis=1)
                            except Exception as e:
                                print(e)
                                exit()
                    try:
                        daypart['Unix'] = daypart.apply(lambda x: x.Unix.strftime('%s'), axis=1)
                    except:
                        # This version is for windows machines, since the above methods don't want to work
                        daypart['Unix'] = daypart.apply(lambda x: x.Unix.timestamp(), axis=1)
                    daypart['Latitude'] = daypart["Latitude"] / 1000000
                    daypart['Longitude'] = daypart["Longitude"] / -1000000
                    # daypart['Coords'] = (daypart["Latitude"]).map(str) + " , " + (daypart["Longitude"]).map(str)
                    # total = pandas.concat([total, daypart])
                    saveDF = pandas.concat([saveDF, daypart])
        else:
            clear()
            print("...Looking for new accident reports, ", dateofemail)
    if os.path.exists("tmp.xlsx"):
        os.remove("tmp.xlsx")
    return saveDF


def main():
    """
    Main method for fetching and cleaning accidents. We start off with declaring the two main file paths' we'll need
        for this code to run.
        mainAccidentFile is the file path for the file that has our existing accident list
        newAccidentFile is going to be the savepath for the accident records we'll be getting from the email
    """
    # mainAccidentFile should be the only thing you have to change when fetching new emails
    mainAccidentFile = ''
    newAccidentFile = 'Main Dir/Accident Data/New Fetched Emails/EmailAccidentData_NewFetch.csv'

    # Read in the file that has all of our accident records
    total = pandas.read_csv("../%s" % mainAccidentFile)
    # Get the last day our accident records cover
    lastday = pandas.Timestamp(total['Response Date'].values[-1]).date() + timedelta(days=1)
    # Fetch all of the emails that have accident records that come after the lastday variable we just made
    newFetch = pull_emails(total, lastday)
    newFetch['Response Date'] = newFetch['Response Date'].astype(str)
    newFetch['Date'] = newFetch['Response Date'].apply(lambda x: str(x).split(" ")[0])
    newFetch['Hour'] = newFetch['Response Date'].apply(lambda x: str(x).split(" ")[1].split(":")[0])

    # Save our newly fetched accidents. We'll be formatting them to fit in with our existing data
    # This doubles a a quick check point, in case something goes awry with the cleaning code below
    newFetch.to_csv("../%s" % newAccidentFile, index=False)

    # The file containing the newly fetched accident records
    # This is read in directly instead of just working on the existing dataset, as otherwise we get some errors
    fetchedAccidents = pandas.read_csv("../%s" % newAccidentFile)
    # Create the Date, Hour, and Coords variables for our newly fetched accident records
    fetchedAccidents['Coords'] = fetchedAccidents['Latitude'].astype(str) + " , " + \
                                 fetchedAccidents['Longitude'].astype(str)
    fetchedAccidents['OK'] = 0

    drops = list()
    for i, _ in enumerate(fetchedAccidents.values):
        # Iterate through our new accidents and see if any record is within a certain amount of time and distance
        # from another. At the time of this writing, any accident record that happened within .25 miles and within
        # 4 minutes of each other, we consider that a duplicate call

        # Get a list of all unix timestamps that are within 4 minutes of eachother
        timematches = fetchedAccidents.loc[(fetchedAccidents['Unix'].between(
            (int(fetchedAccidents.Unix[i]) - 900), (int(fetchedAccidents.Unix[i]) + 900)))].index.tolist()
        # Iterate through our list of close enough timestamps and see how close their respective calls were located
        if len(timematches) > 1:
            for j in timematches:
                dist = geopy.distance.distance(fetchedAccidents.Coords[i], fetchedAccidents.Coords[j]).miles
                if dist < .25 and (int(i) != int(j)) and j not in drops and (j > i):
                    drops.append(j)
    keeps = fetchedAccidents.drop(drops)
    keeps = keeps.drop(['Coords', 'OK'], axis=1)
    keeps = keeps.drop_duplicates(subset=['Response Date', 'Grid_Num'])

    # Getting the hour/date combo of the unix time here to avoid any missed duplicates.
    keeps['Unix'] = keeps.apply(lambda x: pandas.datetime.strptime(str(x.Date) + " " +
                                                                   str(x.Hour).zfill(2), "%Y-%m-%d %H"), axis=1)
    # Depending on your OS, one of the following lines would fail
    try:
        keeps['Unix'] = keeps.apply(lambda x: x.Unix.strftime('%s'), axis=1)  # For Unix or Mac
    except:
        keeps['Unix'] = keeps.apply(lambda x: x.Unix.timestamp(), axis=1)  # For Windows

    print("Duplicates Removed: ", int(len(fetchedAccidents.values) - len(keeps.values)))
    keeps = matchAccidentToGridNum(keeps)
    beforeMatch = len(keeps)
    keeps = keeps[keeps['Grid_Num'] > -1]
    print("Records dropped due to no matching Grid Num: ", int(beforeMatch - len(keeps)))
    # Save the dropped duplicates version
    keeps.to_csv("../Main Dir/Accident Data/New Fetched Emails/EmailAccidentData_NewFetchFormatted.csv", index=False)

    # Combine the main dataset of accidents with the newly fetched ones, then save it with an updated date
    keeps = keeps.reindex(columns=total.columns)
    masterSave = pandas.concat([total, keeps], axis=0, join='outer', ignore_index=False)
    thisDate = time.strftime("%Y-%m-%d")
    masterSave.to_csv("../Main Dir/Accident Data/EmailAccidentData_%s.csv" % thisDate, index=False)


if __name__ == "__main__":
    main()
