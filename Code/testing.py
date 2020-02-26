##  This file is kept empty for testing small chunks of code easily. Please clear this file when you are done working on the code, and put it into
#       whatever file it needs to go in.
import pandas
import glob
import feather
from datetime import datetime


# Set empty DataFrame
frame = pandas.DataFrame()

test = pandas.read_csv("/home/jeremy/Downloads/2020 Weather/2020 Weather 1-25.csv")
columns = test.columns
# Use glob to collect all files into one DataFrame
for f in glob.glob("/home/jeremy/Downloads/2020 Weather/*.csv"):
	df = pandas.read_csv(f, usecols = columns, dtype = object)
	frame = frame.append(df, ignore_index = True)
	print(f, len(frame))
frame.Unix = frame.time
frame.sort_values(by=["Grid_Num", "Unix"])
print(frame.head)
feather.write_dataframe(frame, "../Ignore/2020 Weather Feb 24.feather")