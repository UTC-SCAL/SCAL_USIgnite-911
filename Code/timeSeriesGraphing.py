# A file to hold some simple time series graphing code for our accident files
import pandas
import matplotlib.pyplot as plt
from datetime import datetime


def incidents_by_year(data):
    """
    This creates graphs to plot incidents according to year, where the x axis is the year and each line is the
        number of incidents per weekday
    :param data: the data you are using
    """
    # Cut the dataframe down to the columns we want
    incSplice = data[["Year", "Month"]]
    # incSplice = data[['Year', 'WeekDay']]

    # Based on what you want to graph, use the different inFreq values
    incidents2017 = incSplice[incSplice['Year'] == 2017]
    incFreq2017 = incidents2017.Month.value_counts().sort_index()
    # incFreq2017 = incidents2017.WeekDay.value_counts().sort_index()

    incidents2018 = incSplice[incSplice['Year'] == 2018]
    incFreq2018 = incidents2018.Month.value_counts().sort_index()
    # incFreq2018 = incidents2018.WeekDay.value_counts().sort_index()

    incidents2019 = incSplice[incSplice['Year'] == 2019]
    incFreq2019 = incidents2019.Month.value_counts().sort_index()
    # incFreq2019 = incidents2019.WeekDay.value_counts().sort_index()

    incidents2020 = incSplice[incSplice['Year'] == 2020]
    incFreq2020 = incidents2020.Month.value_counts().sort_index()
    # incFreq2020 = incidents2020.WeekDay.value_counts().sort_index()

    x0 = incFreq2017
    x1 = incFreq2018
    x2 = incFreq2019
    x3 = incFreq2020
    plt.plot(x0, label="2017", linewidth=2)
    plt.plot(x1, label="2018", linewidth=2)
    plt.plot(x2, label="2019", linewidth=2)
    plt.plot(x3, label="2020", linewidth=2)

    # If graphing months on X axis
    ticks = list(range(1, 13, 1))
    labels = "Jan Feb Mar Apr May Jun July Aug Sep Oct Nov Dec".split()
    # If graphing weekday on X axis
    # ticks = list(range(0, 7, 1))
    # labels = "Mon Tue Wed Thu Fri Sat Sun".split()

    plt.xticks(ticks, labels, rotation=45)
    plt.xlabel('Month')
    plt.ylabel('Accidents')
    plt.title("Accidents by Year")
    plt.legend()
    # Save the Image
    # plt.savefig("")
    plt.show()


def reformatData(data):
    # Get the columns we could need
    graphCols = ['Date', 'DayOfWeek', 'Hour', 'Latitude', 'Longitude', 'Unix', 'WeekDay', 'Year', 'Month']
    data = data.reindex(columns=graphCols)
    # Add in missing data
    data.Year = data.Date.apply(lambda x: x.split("/")[2])
    data.Month = data.Date.apply(lambda x: x.split('/')[0])
    for i, _ in enumerate(data.values):
        timestamp = str(data.Date.values[i]) + " " + str(data.Hour.values[i])
        thisDate = datetime.strptime(timestamp, "%m/%d/%Y %H")
        data.DayOfWeek.values[i] = thisDate.weekday()

    data.WeekDay = data.DayOfWeek.apply(lambda x: 0 if x >= 5 else 1)
    # Needs to be independently saved
    data.to_csv("../", index=False)

# data = pandas.read_csv("../")
# For some reason, the graphing code won't work on the data unless it's been saved to a file, so create a save file of
# the data you want to use, then read in that data
# reformatData(data)

# formattedData = pandas.read_csv("../")
# If you want to split the data into distinct dataframes per year
# data2017 = formattedData[formattedData['Date'].str.contains('2017')]
# data2018 = formattedData[formattedData['Date'].str.contains('2018')]
# data2019 = formattedData[formattedData['Date'].str.contains('2019')]
# data2020 = formattedData[formattedData['Date'].str.contains('2020')]

# incidents_by_year(formattedData)
