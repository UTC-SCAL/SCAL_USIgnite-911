import pandas
from selenium import webdriver

segments = pandas.read_csv("../Excel & CSV Sheets/ETRIMS/Roadway_Geometrics_New.csv", sep=",")

driver = webdriver.Firefox(executable_path=r"/home/admin/PycharmProjects/911Project/geckodriver")
driver.get("https://e-trims.tdot.tn.gov/Account/Logon")

usr = driver.find_element_by_id("UserName")
pw = driver.find_element_by_id("Password")

usr.send_keys("JJVPG56")
pw.send_keys("Saturn71")  # updated 2/26/2019
driver.find_element_by_class_name("btn").click()

for i, info in enumerate(segments.values):
    routeID = segments.ID_NUMBER.values[i]
    logmile = segments.BLM.values[i]
    siteRoute = 'https://e-trims.tdot.tn.gov/etrimsol/services/applicationservice/roadfinder/latlongforlrs?idnumber=' \
                + str(routeID) + '&logmile=' + str(logmile) + '&subroute='

    driver.get(siteRoute)
    raw = str(driver.page_source)
    X = float(raw[raw.index("<X>") + len("<X>"): raw.index("</X>")])
    Y = raw[raw.index("<Y>") + len("<Y>"): raw.index("</Y>")]
    segments.BLM_Lat.values[i] = Y
    segments.BLM_Long.values[i] = X

    logmile = segments.ELM.values[i]
    siteRoute = 'https://e-trims.tdot.tn.gov/etrimsol/services/applicationservice/roadfinder/latlongforlrs?idnumber=' \
                + str(routeID) + '&logmile=' + str(logmile) + '&subroute='

    driver.get(siteRoute)
    raw = str(driver.page_source)
    X = float(raw[raw.index("<X>") + len("<X>"): raw.index("</X>")])
    Y = raw[raw.index("<Y>") + len("<Y>"): raw.index("</Y>")]
    segments.ELM_Lat.values[i] = Y
    segments.ELM_Long.values[i] = X
segments.to_csv("../Excel & CSV Sheets/ETRIMS/Roadway_Geometrics_Connor.csv",sep=",")