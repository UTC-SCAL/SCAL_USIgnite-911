import os, sys

def find_cred(self, service):
    if os.path.exists(self):
        with open(self, "r") as file:
            lines = file.readlines()
            if service in lines[0]:
                cred = lines[0].split(",")[1]
                # print(cred)
            if service in lines[1]:
                cred = lines[1].split(",")[1], lines[1].split(",")[2]
                # print(cred)
                    # logins[username] = password
    return cred

cred = find_cred("/Users/pete/Documents/GitHub/SCAL_USIgnite-911/Excel & CSV Sheets/Login.csv", 'darksky')
print(cred)

cred = find_cred("/Users/pete/Documents/GitHub/SCAL_USIgnite-911/Excel & CSV Sheets/Login.csv", 'etrims')
print(cred)
