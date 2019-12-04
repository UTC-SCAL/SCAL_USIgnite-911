##  This file is kept empty for testing small chunks of code easily. Please clear this file when you are done working on the code, and put it into
#       whatever file it needs to go in.

import pandas
import numpy
import time
import math
import geopy.distance
import imaplib
import email
from io import StringIO
import chardet


total = pandas.read_csv("Excel & CSV Sheets/Accidents/RawAccidentData.csv")
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
        print(mail["Subject"], len(total))
        encode = chardet.detect(part.get_payload(decode=True))['encoding']
        # print(encode)
        # print(type(part.get_payload(decode=True)))
        try:
            s=str(part.get_payload(decode=True),encode)
            data = StringIO(s)
            daypart=pandas.read_csv(data)
            total = pandas.concat([total, daypart])
        except:
            total.to_csv("Excel & CSV Sheets/Accidents/RawAccidentDataComplete.csv")
            print("In Except")
            print(str(part.get_payload(decode=True)))
            exit()
            s=str(part.get_payload(decode=False))
total.to_csv("Excel & CSV Sheets/Accidents/RawAccidentDataComplete.csv")