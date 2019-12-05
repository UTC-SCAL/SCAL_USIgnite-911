##  This file is kept empty for testing small chunks of code easily. Please clear this file when you are done working on the code, and put it into
#       whatever file it needs to go in.

import pandas

acc = pandas.read_csv("Excel & CSV Sheets/Accidents/RawAccidentData_DropDupsTest.csv")
print(acc.columns)

for i,info in enumerate(acc.values):
    if acc.Latitude.values[i] > 36: 
        acc.Latitude.values[i] = acc.Latitude.values[i]/1000000
        acc.Longitude.values[i] = acc.Latitude.values[i]/-1000000
acc.to_csv("Excel & CSV Sheets/Accidents/RawAccidentData_DropDupsTest2.csv", index=False)


HCS-length(x,y):
    m = x.length
    n = y.length
    let b[1...m,1..n] and c[0...m,0...n] be new tables
    for i=1 to m:
        c[i,0] = 0
    for j=0 to n:
        c[0,j] = 0
    for i=1 to m:
        for j=1 to n: 
            if xi == y:
                if (xi == A) or (xi == B)
                    c[i,j] = c[i-1,j-1]+2;b[i,j]=" "



