import pandas


def find_gridblocks(date):
    date = str(date)
    accidents = pandas.read_csv("../Excel & CSV Sheets/Accident Only Files/2017+2018 Accidents.csv")
    accidents.Date = accidents.Date.astype(str)

    name = "gridLocations_" + date
    print(name)
    name = []

    for i, values in enumerate(accidents.values):
        if accidents.Date.values[i] == date:
            name.append(accidents.Grid_Block.values[i])

    # We have our list of grid blocks with accidents for a given day, but there my be duplicates
    # We create a dictionary, using the list of grid blocks as keys
    # This automatically removes any duplicate values since dictionaries can't have duplicate keys
    # Then, we convert it back to a list, and wham! No more dupes
    name = list(dict.fromkeys(name))
    print(name)

find_gridblocks("2017-02-12")
