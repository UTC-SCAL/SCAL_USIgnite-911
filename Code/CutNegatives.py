import pandas

##This file takes in a positive and negative set of data, and reduces 
# the negatives of the file to 1/3, then saves the reduced dataset. 
calldata = pandas.read_csv("",sep=",")
print(len(calldata))
accidents = calldata[calldata['Accident'] == 1]
print(len(accidents))
noaccidents = calldata[calldata['Accident'] == 0]
print(len(noaccidents))

reduced = noaccidents.copy()

listing = []
for i, info in enumerate(noaccidents.values):
    if i % 3 == 0:
        pass
    else:
        listing.append(i)
reduced.drop(reduced.index[listing], inplace=True)
frames = [accidents, reduced]
fulldata = pandas.concat(frames)
fulldata = fulldata.sort_values(by=['Date', 'Time'])
print(len(fulldata), (len(fulldata)/2))
fulldata.to_csv("", sep=",")