import pandas

# Read in the files you want to append together
acc1 = pandas.read_csv("../")
acc2 = pandas.read_csv("../")
acc3 = pandas.read_csv("../")

# append the files together
bigBOI = pandas.concat([acc1, acc2, acc3], axis=0, join='outer', ignore_index=False)

# printing before and after lengths to see if we dropped any duplicate values
print(len(bigBOI))
bigBOI.drop_duplicates(keep="first", inplace=True)
print(len(bigBOI))

# Save the concatenated files
bigBOI.to_csv("../")

# Splitting the date into year, day, and month values
# Depending on how the date is formatted, you'll need to change the split value and position
# Ex: if the date is formatted as yyyy-mm-dd, the split value will be split("-")[0] for year
data = pandas.read_csv("../")
data['Year'] = data.apply(lambda x : x.Date.split("-")[0], axis=1)
data['Day'] = data.apply(lambda x : x.Date.split("-")[2], axis=1)
data['Month'] = data.apply(lambda x : x.Date.split("-")[1], axis=1)
data.to_csv("../")