import pandas
from datetime import datetime
from darksky import forecast
import os, sys
import requests
import xml.etree.ElementTree
from selenium import webdriver

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'


def save_excel_file(save_file_name, sheet, data_file_name):
    writer = pandas.ExcelWriter(save_file_name, engine='xlsxwriter', date_format='mmm d yyyy')
    data_file_name.to_excel(writer, sheet_name=sheet)
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    writer.save()


calldata = pandas.read_excel(folderpath + "/Excel & CSV Sheets/2017+2018 Data/2018 + 2017 Full Data.xlsx")

# payload = {
#     'UserName': 'JJVPG58',
#     'Password': 'Nashville1',
#     'ok':
# }

driver = webdriver.Firefox()
driver.get("https://e-trims.tdot.tn.gov/Account/Logon")

usr = driver.find_element_by_id("UserName")
pw = driver.find_element_by_id("Password")

usr.send_keys("JJVPG58")
pw.send_keys("Nashville1")
driver.find_element_by_class_name("btn").click()

calldata.Route = calldata.Route.astype(str)

for i, info in enumerate(calldata.values):
    latitude = calldata.Latitude[i]
    longitude = calldata.Longitude[i]

    site = "https://e-trims.tdot.tn.gov/etrimsol/services/applicationservice/roadfinder/lrsforlatlong?latitude=" \
            + str(latitude)+"&longitude=" + str(longitude)+"&d=1538146112919"

    driver.get(site)
    raw = str(driver.page_source)
    milepoint = float(raw[raw.index("<MilePoint>") + len("<MilePoint>"): raw.index("</MilePoint>")])
    routeid = raw[raw.index("<RouteId>") + len("<RouteId>"): raw.index("</RouteId>")]

    print("milepoint={}, routeid={}".format(milepoint, routeid))
    calldata.Route.values[i] = routeid
    calldata.Log_Mile.values[i] = milepoint

calldata.to_csv(folderpath + "Excel & CSV Sheets/Routes and Miles.csv", sep=',', index=False)

