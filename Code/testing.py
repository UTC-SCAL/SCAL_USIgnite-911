##  This file is kept empty for testing small chunks of code easily. Please clear this file when you are done working on the code, and put it into
#       whatever file it needs to go in.
 
import pandas

neg1 = pandas.read_csv("../Excel & CSV Sheets/Grid Hex Layout/Negative Sample Data/Total Shift/NS-TS 2017 Master File.csv")
neg2 = pandas.read_csv("../Excel & CSV Sheets/Grid Hex Layout/Negative Sample Data/Total Shift/NS-TS 2018 Master File.csv")
neg3 = pandas.read_csv("../Excel & CSV Sheets/Grid Hex Layout/Negative Sample Data/Total Shift/NS-TS 2019 Master File.csv")

acc1 = pandas.read_csv("../Excel & CSV Sheets/Grid Hex Layout/Accidents/Accident2017 NoHighway.csv")
acc2 = pandas.read_csv("../Excel & CSV Sheets/Grid Hex Layout/Accidents/Accident2018 NoHighway.csv")
acc3 = pandas.read_csv("../Excel & CSV Sheets/Grid Hex Layout/Accidents/Accident2019 NoHighway.csv")

columns = acc1.columns
neg1 = neg1.reindex(columns=columns)
neg2 = neg2.reindex(columns=columns)
neg3 = neg3.reindex(columns=columns)


# Append that shiz
bigBOI = pandas.concat([acc1, neg1, acc2, neg2, acc3, neg3], axis=0, join='outer', ignore_index=False)
print(len(bigBOI))
# Drop duplicates if there are any
bigBOI.drop_duplicates(keep="first", inplace=True)
print(len(bigBOI))

bigBOI.to_csv("../Excel & CSV Sheets/Grid Hex Layout/Negative Sample Data/Total Shift/TS Negatives No Split.csv", index=False)