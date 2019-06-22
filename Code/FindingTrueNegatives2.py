import pandas
import os, sys
import random

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'


negatives = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/NS Master List 2.csv",index_col=False)
# negative_samples = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/NS Master List.csv",index_col=False)
negative_samples = pandas.DataFrame(columns=negatives.columns.values)
accidents = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/GOD 2017+2018 Accidents.csv",index_col=False)
neg_loc=0

for i, info in enumerate(negatives.values):
    print(i)
    no_matches=True
    for j, stuff in enumerate(accidents.values):
        if (negatives.DayFrame.values[i] == accidents.DayFrame.values[j]) and (negatives.WeekDay.values[i] == accidents.WeekDay.values[j]) and \
            (negatives.Grid_Block.values[i] == accidents.Grid_Block.values[j]):
            no_matches = False
            break
    if no_matches is True:
        negative_samples.loc[neg_loc] = negatives.values[i]
        neg_loc += 1
    if i % 500 == 0:
        negative_samples.to_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/NS True Master List 2.csv", index=False)
print("True Negatives found :", neg_loc+1)
negative_samples.to_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/NS True Master List 2.csv", index=False)
exit()


# def find_cred(service):
    # file = "../Excel & CSV Sheets/login.csv"
    # if os.path.exists(file):
    #     with open(file, "r") as file:
    #         lines = file.readlines()
    #         if service in lines[0]:
    #             cred = lines[0].split(",")[1]
    #             # print(cred)
    #         if service in lines[1]:
    #             cred = str(lines[1].split(",")[1]) + "," + str(lines[1].split(",")[2])
    #             # print(cred)
    #             # logins[username] = password
    # return cred
