# A file to hold some simple time series graphing code for our accident files
import pandas
import matplotlib.pyplot as plt
from datetime import datetime


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


def incidents_by_year(data):
    """
    This creates graphs to plot incidents according to year, where the x axis is the year and each line is the
        number of incidents per weekday
    :param data: the data you are using
    """
    # Cut the dataframe down to the columns we want
    # data2017cut = data[data['Date'].str.contains('2017')]
    # data2018cut = data[data['Date'].str.contains('2018')]
    # data2019cut = data[data['Date'].str.contains('2019')]
    data2020cut = data[data['Date'].str.contains('2020')]
    # accFreq2017 = data2017cut.Month.value_counts().sort_index()
    # accFreq2018 = data2018cut.Month.value_counts().sort_index()
    # accFreq2019 = data2019cut.Month.value_counts().sort_index()
    accFreq2020 = data2020cut.Month.value_counts().sort_index()

    # x0 = accFreq2017
    # x1 = accFreq2018
    # x2 = accFreq2019
    x3 = accFreq2020
    # plt.plot(x0, label="2017", linewidth=2)
    # plt.plot(x1, label="2018", linewidth=2)
    # plt.plot(x2, label="2019", linewidth=2)
    plt.plot(x3, label="2020", linewidth=2)

    # If graphing months on X axis
    ticks = list(range(1, 13, 1))
    labels = "Jan Feb Mar Apr May Jun July Aug Sep Oct Nov Dec".split()

    plt.xticks(ticks, labels, rotation=45)
    plt.xlabel('Month')
    plt.ylabel('Accidents')
    plt.ylim(0, 3000)
    plt.title("Our Accidents by Year")
    plt.legend()
    # Save the Image
    # plt.savefig("")
    plt.show()


# data = pandas.read_csv("../")
# For some reason, the graphing code won't work on the data unless it's been saved to a file, so create a save file of
# the data you want to use, then read in that data
# reformatData(data)

# If you want to split the data into distinct dataframes per year
# data2017 = formattedData[formattedData['Date'].str.contains('2017')]
# data2018 = formattedData[formattedData['Date'].str.contains('2018')]
# data2019 = formattedData[formattedData['Date'].str.contains('2019')]
# data2020 = formattedData[formattedData['Date'].str.contains('2020')]
# print('Accident entries for 2017: ', len(data2017))
# print('Accident entries for 2018: ', len(data2018))
# print('Accident entries for 2019: ', len(data2019))
# print('Accident entries for 2020: ', len(data2020))

# incidents_by_year(formattedData)
