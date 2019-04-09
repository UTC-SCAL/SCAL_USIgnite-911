import pandas
import matplotlib.pyplot as plt
import numpy as np


##Incidents by Hour of the Day##
def incident_by_hour(file):
    plt.plot(x, y, label=label, color=color, linewidth=4)
    xticks = [0.0, 6.0, 12.0, 18.0, 23.0]
    plt.xticks(xticks)
    plt.xlabel('Hour')
    plt.ylabel('Incidents that Occurred on',day)
    plt.title('Hourly Incident Count')
    plt.legend()
    plt.show()

def by_day_hour(file):
    tab = file.groupby(['Weekday', 'Hour']).size().reset_index()

    tab.columns = ['Weekday', 'Hour', 'Count']
    Monday = tab.loc[tab['Weekday'] == 0]
    Tuesday = tab.loc[tab['Weekday'] == 1]
    Wednesday = tab.loc[tab['Weekday'] == 2]
    Thursday = tab.loc[tab['Weekday'] == 3]
    Friday = tab.loc[tab['Weekday'] == 4]
    Saturday = tab.loc[tab['Weekday'] == 5]
    Sunday = tab.loc[tab['Weekday'] == 6]

    font = {'family': 'serif',
                'weight': 'regular',
                'size': 18}
    plt.rc('font', **font)
    plt.plot(Monday.Hour.values,Monday.Count.values, label='Monday', color='r', linewidth=3)
    plt.plot(Tuesday.Hour.values,Tuesday.Count.values, label='Tuesday', color='Orange', linewidth=3)
    plt.plot(Wednesday.Hour.values,Wednesday.Count.values, label='Wednesday', color='Yellow', linewidth=3)
    plt.plot(Thursday.Hour.values,Thursday.Count.values, label='Thursday', color='Green', linewidth=3)
    plt.plot(Friday.Hour.values,Friday.Count.values, label='Friday', color='blue', linewidth=3)
    plt.plot(Saturday.Hour.values,Saturday.Count.values, label='Saturday', color='indigo', linewidth=3)
    plt.plot(Sunday.Hour.values,Sunday.Count.values, label='Sunday', color='violet', linewidth=3)
    xticks = [0.0, 6.0, 12.0, 18.0, 23.0]
    plt.xticks(xticks)
    plt.grid(color='lightgray', linestyle='-', linewidth=2)
    plt.xlabel('Hour')
    plt.ylabel('Incidents that Occurred')
    plt.title('Hourly Incident Count')
    plt.legend()
    plt.show()

def by_month_hour(file):
    tab = file.groupby(['Month', 'Hour']).size().reset_index()
    tab.columns = ['Month', 'Hour','Count']

    January = tab.loc[tab['Month'] == 1]
    February = tab.loc[tab['Month'] == 2]
    March = tab.loc[tab['Month'] == 3]
    April = tab.loc[tab['Month'] == 4]
    May = tab.loc[tab['Month'] == 5]
    June = tab.loc[tab['Month'] == 6]
    July = tab.loc[tab['Month'] == 7]
    August = tab.loc[tab['Month'] == 8]
    September = tab.loc[tab['Month'] == 9]
    October = tab.loc[tab['Month'] == 10]
    November = tab.loc[tab['Month'] == 11]
    December = tab.loc[tab['Month'] == 12]

    font = {'family': 'serif',
                'weight': 'regular',
                'size': 18}
    plt.rc('font', **font)
    plt.plot(January.Hour.values,January.Count.values, label='January', color='maroon', linewidth=3)
    plt.plot(February.Hour.values,February.Count.values, label='February', color='r', linewidth=3)
    plt.plot(March.Hour.values,March.Count.values, label='March', color='Orange', linewidth=3)
    plt.plot(April.Hour.values,April.Count.values, label='April', color='Yellow', linewidth=3)
    plt.plot(May.Hour.values,May.Count.values, label='May', color='lime', linewidth=3)
    plt.plot(June.Hour.values,June.Count.values, label='June', color='Green', linewidth=3)
    plt.plot(July.Hour.values,July.Count.values, label='July', color='Teal', linewidth=3)
    plt.plot(August.Hour.values,August.Count.values, label='August', color='cyan', linewidth=3)
    plt.plot(September.Hour.values,September.Count.values, label='September', color='blue', linewidth=3)
    plt.plot(October.Hour.values,October.Count.values, label='October', color='purple', linewidth=3)
    plt.plot(November.Hour.values,November.Count.values, label='November', color='fuchsia', linewidth=3)
    plt.plot(December.Hour.values,December.Count.values, label='December', color='pink', linewidth=3)
    xticks = [0.0, 6.0, 12.0, 18.0, 23.0]
    plt.xticks(xticks)
    plt.grid(color='lightgray', linestyle='-', linewidth=2)
    plt.xlabel('Hour')
    plt.ylabel('Incidents that Occurred')
    plt.title('Hourly Incident Count')
    plt.legend()
    plt.show()

def by_month_day(file):
    tab = file.groupby(['Month', 'Weekday']).size().reset_index()
    tab.columns = ['Month', 'Weekday','Count']

    January = tab.loc[tab['Month'] == 1]
    February = tab.loc[tab['Month'] == 2]
    March = tab.loc[tab['Month'] == 3]
    April = tab.loc[tab['Month'] == 4]
    May = tab.loc[tab['Month'] == 5]
    June = tab.loc[tab['Month'] == 6]
    July = tab.loc[tab['Month'] == 7]
    August = tab.loc[tab['Month'] == 8]
    September = tab.loc[tab['Month'] == 9]
    October = tab.loc[tab['Month'] == 10]
    November = tab.loc[tab['Month'] == 11]
    December = tab.loc[tab['Month'] == 12]

    font = {'family': 'serif',
                'weight': 'regular',
                'size': 18}
    plt.rc('font', **font)
    plt.plot(January.Weekday.values,January.Count.values, label='January', color='maroon', linewidth=3)
    plt.plot(February.Weekday.values,February.Count.values, label='February', color='r', linewidth=3)
    plt.plot(March.Weekday.values,March.Count.values, label='March', color='Orange', linewidth=3)
    plt.plot(April.Weekday.values,April.Count.values, label='April', color='Yellow', linewidth=3)
    plt.plot(May.Weekday.values,May.Count.values, label='May', color='lime', linewidth=3)
    plt.plot(June.Weekday.values,June.Count.values, label='June', color='Green', linewidth=3)
    plt.plot(July.Weekday.values,July.Count.values, label='July', color='Teal', linewidth=3)
    plt.plot(August.Weekday.values,August.Count.values, label='August', color='cyan', linewidth=3)
    plt.plot(September.Weekday.values,September.Count.values, label='September', color='blue', linewidth=3)
    plt.plot(October.Weekday.values,October.Count.values, label='October', color='purple', linewidth=3)
    plt.plot(November.Weekday.values,November.Count.values, label='November', color='fuchsia', linewidth=3)
    plt.plot(December.Weekday.values,December.Count.values, label='December', color='pink', linewidth=3)
    days = ["Monday", 'Tuesday', "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    xticks = [0,1,2,3,4,5,6]
    plt.xticks(xticks,days)
    plt.grid(color='lightgray', linestyle='-', linewidth=2)
    plt.ylabel('Incidents that Occurred')
    plt.title('Daily Incident Count')
    plt.legend()
    plt.show()

def by_year_hour(file):

    tab = file.groupby(['Year', 'Hour']).size().reset_index()
    tab.columns = ['Year', 'Hour','Count']
    seventeen = tab.loc[tab['Year'] == 2017]
    eighteen = tab.loc[tab['Year'] == 2018]
    nineteen = tab.loc[tab['Year'] == 2018]

    font = {'family': 'serif',
                'weight': 'regular',
                'size': 18}
    plt.rc('font', **font)
    plt.plot(seventeen.Hour.values,seventeen.Count.values, label='2017', color='red', linewidth=3)
    plt.plot(eighteen.Hour.values,eighteen.Count.values, label='2018', color='green', linewidth=3)
    plt.plot(nineteen.Hour.values,nineteen.Count.values, label='2019', color='blue', linewidth=3)
    xticks = [0.0, 6.0, 12.0, 18.0, 23.0]
    plt.xticks(xticks)
    plt.grid(color='lightgray', linestyle='-', linewidth=2)
    plt.xlabel('Hour')
    plt.ylabel('Incidents that Occurred')
    plt.title('Hourly Incident Count')
    plt.legend()
    plt.show()

def by_year_day(file):

    tab = file.groupby(['Year', 'Weekday']).size().reset_index()
    tab.columns = ['Year', 'Weekday','Count']
    seventeen = tab.loc[tab['Year'] == 2017]
    eighteen = tab.loc[tab['Year'] == 2018]
    print(eighteen)
    nineteen = tab.loc[tab['Year'] == 2018]

    font = {'family': 'serif',
                'weight': 'regular',
                'size': 18}
    plt.rc('font', **font)
    plt.plot(seventeen.Weekday.values,seventeen.Count.values, label='2017', color='red', linewidth=3)
    plt.plot(eighteen.Weekday.values,eighteen.Count.values, label='2018', color='green', linewidth=3)
    plt.plot(nineteen.Weekday.values,nineteen.Count.values, label='2019', color='blue', linewidth=3)
    days = ["Monday", 'Tuesday', "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    xticks = [0,1,2,3,4,5,6]
    plt.xticks(xticks,days)
    plt.grid(color='lightgray', linestyle='-', linewidth=2)
    plt.ylabel('Incidents that Occurred')
    plt.title('Daily Incident Count')
    plt.legend()
    plt.show()

def main():
    data = pandas.read_csv("../Excel & CSV Sheets/Full Data.csv",sep=",")
    data['Year'] = 0
    for k, info in enumerate(data.values):
        doa = data.Date.values[k]
        # print(doa)
        year = (int(doa.split('-')[0]))
        # print(year)
        data.Year.values[k] = year
    # print(data.Year.values[0:10])
    # by_day_hour(data)
    # by_month_hour(data)
    # by_month_day(data)
    by_year_day(data)

    # x, y = np.loadtxt(daysofyear, delimiter=',', unpack=True)
    # plt.plot(x, y, 'rX', label='Daily Incidents')
    # xticks = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
    #           'November', 'December']
    # plt.xticks([31,59,90,120,151,181,212,243,273,304,334,365], xticks)
    # plt.xlabel('Day')
    # plt.ylabel('Incidents that Occurred')
    # plt.title('Incident Count by Day of Year')
    # plt.legend()
    # plt.show()


if __name__ == "__main__":
    main()
