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
from datetime import timedelta
import geopandas
from geopandas.tools import sjoin
from datetime import datetime
import geopy.distance
import time


def clear():
    os.system('clear')


def pull_emails(total, lastday):
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login('utcscal2018@gmail.com', 'EMCS 335')
    m.select("INBOX")  # here you a can choose a mail box like INBOX instead
    lookfor = "UNANSWERED SENTSINCE " + str(lastday.strftime("%d-%b-%Y"))
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
                                daypart[['Response Date', _]] = daypart['Response Date'].apply(
                                    lambda x: pandas.Series(str(x).split(".")))
                                daypart['Unix'] = daypart.apply(lambda x: datetime.strptime(
                                    str(x['Response Date']), "%Y-%m-%d %H:%M:%S"), axis=1)
                            except Exception as e:
                                print(e)
                                exit()
                    daypart['Unix'] = daypart.apply(lambda x: x.Unix.strftime('%s'), axis=1)
                    daypart['Latitude'] = daypart["Latitude"] / 1000000
                    daypart['Longitude'] = daypart["Longitude"] / -1000000
                    # daypart['Coords'] = (daypart["Latitude"]).map(str) + " , " + (daypart["Longitude"]).map(str)
                    total = pandas.concat([total, daypart])
        else:
            clear()
            print("...Looking for new accident reports, ", dateofemail)
    if os.path.exists("tmp.xlsx"):
        os.remove("tmp.xlsx")
    return total


def main():
    # This is the beginning of the fetching emails code lines #

    # Read in the file that has all of our accident records
    total = pandas.read_csv("../Pre Thesis/Grid Hex Layout/Accidents/RawAccidentData_11-19-20.csv")
    # Get the last day our accident records cover
    lastday = pandas.Timestamp(total['Response Date'].values[-1]).date() + timedelta(days=1)

    total = pull_emails(total, lastday)
    total.to_csv("../Excel & CSV Sheets/Grid Hex Layout/Accidents/RawAccidentData_NewFetch.csv", index=False)

    # This is the beginning of the cleaning of the fetched emails code lines #
    # I get it may not be the best way to combine these files, but this method works
    # The file containing the newly fetched accident records
    fetchedAccidents = pandas.read_csv("../Pre Thesis/Grid Hex Layout/Accidents/RawAccidentData_NewFetch.csv")
    # The file containing our cleaned list of raw accident records
    cleanedAccidents = pandas.read_csv("../Pre Thesis/Grid Hex Layout/Accidents/RawAccidentData_11-19-20.csv")
    # Gets the date of the last record in our raw accident data
    lastcleaned = pandas.Timestamp(cleanedAccidents['Response Date'].values[-1]).date()

    fetchedAccidents['Date'] = fetchedAccidents.apply(lambda x: pandas.Timestamp(x['Response Date']).date(), axis=1)
    fetchedAccidents['Hour'] = fetchedAccidents.apply(lambda x: pandas.Timestamp(x['Response Date']).hour, axis=1)
    fetchedAccidents['Coords'] = fetchedAccidents['Latitude'].astype(str) + " , " + fetchedAccidents[
        'Longitude'].astype(str)
    fetchedAccidents['OK'] = 0

    drops = list()
    for i, _ in enumerate(fetchedAccidents.values):
        if fetchedAccidents.Date.values[i] >= lastcleaned:
            timematches = fetchedAccidents.loc[(fetchedAccidents['Unix'].between((int(fetchedAccidents.Unix[i]) - 900),
                                                                                 (int(fetchedAccidents.Unix[i]) +
                                                                                  900)))].index.tolist()
            if len(timematches) > 1:
                for j in timematches:
                    dist = geopy.distance.distance(fetchedAccidents.Coords[i], fetchedAccidents.Coords[j]).miles
                    if dist < .25 and (int(i) != int(j)) and j not in drops and (j > i):
                        drops.append(j)
    keeps = fetchedAccidents.drop(drops)
    keeps = keeps.drop(['Coords', 'OK'], axis=1)

    # Getting the hour/date combo of the unix time here to avoid any missed duplicates.
    keeps['Unix'] = keeps.apply(lambda x: pandas.datetime.strptime(str(x.Date) + " " +
                                                                   str(x.Hour).zfill(2), "%Y-%m-%d %H"), axis=1)
    # Depending on your OS, choose one of the following lines
    # keeps['Unix'] = keeps.apply(lambda x: x.Unix.strftime('%s'), axis=1)  # For Unix or Mac
    keeps['Unix'] = keeps.apply(lambda x: x.Unix.timestamp(), axis=1)  # For Windows

    print("Duplicates Removed:", int(len(fetchedAccidents.values) - len(keeps.values)))
    # Save the dropped duplicates version
    thisDate = time.strftime("%m-%d-%y")
    keeps.to_csv("../Excel & CSV Sheets/Grid Hex Layout/Accidents/RawAccidentData_%s.csv" % thisDate, index=False)


if __name__ == "__main__":
    main()
