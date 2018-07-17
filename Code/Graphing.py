# import pandas as pd
# import xlrd
# import xlsxwriter
# from datetime import datetime, date
# import csv
# import test.py
import matplotlib.pyplot as plt
import numpy as np


##Incidents by Hour of the Day##
def incident_by_hour(filename, day, color):
    label = (day)
    x, y = np.loadtxt(filename, delimiter=',', unpack=True)
    plt.plot(x, y, label=label, color=color, linewidth=4)
    xticks = [0.0, 6.0, 12.0, 18.0, 23.0]
    plt.xticks(xticks)
    # plt.xlabel('Hour')
    # plt.ylabel('Incidents that Occurred on',day)
    # plt.title('Hourly Incident Count')
    # plt.legend()
    # plt.show()


def by_month(filename):
    # colors = ('r', 'Orange', 'Yellow', 'green','blue', 'Purple', 'r', 'Orange', 'Yellow', 'green','blue', 'Purple',)
    x, y = np.loadtxt(filename, delimiter=',', unpack=True)
    xticks = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    plt.xticks(x, xticks)
    plt.plot(x, y, label='Monthly Incident Count', color='Crimson', linewidth=3)
    plt.xlabel('Month')
    plt.ylabel('Incidents that Occurred')
    plt.title('Monthly Incident Count')
    plt.legend()
    plt.show()


def main():
    hourly_average_data = 'Hourly Count.csv'
    months_data = 'Months Count.csv'
    daily_data = 'Days of Week.csv'
    problem_data = 'Problem_Occurences.csv'
    Monday_path = 'Monday_Hourly_Count.csv'
    Tuesday_path = 'Tuesday_Hourly_Count.csv'
    Wednesday_path = 'Wednesday_Hourly_Count.csv'
    Thursday_path = 'Thursday_Hourly_Count.csv'
    Friday_path = 'Friday_Hourly_Count.csv'
    Saturday_path = 'Saturday_Hourly_Count.csv'
    Sunday_path = 'Sunday_Hourly_Count.csv'
    daysofyear = 'Days of Year.csv'

    # incident_by_hour(Monday_path, 'Monday', 'r' )
    # incident_by_hour(Tuesday_path, 'Tuesday', 'Orange')
    # incident_by_hour(Wednesday_path, 'Wednesday', 'Yellow')
    # incident_by_hour(Thursday_path, 'Thursday', 'Green')
    # incident_by_hour(Friday_path, 'Friday', 'Teal')
    # incident_by_hour(Saturday_path, 'Saturday', 'Purple')
    # incident_by_hour(Sunday_path, 'Sunday', 'Fuchsia')
    # plt.xlabel('Hour')
    # plt.ylabel('Incidents that Occurred')
    # plt.title('Hourly Incident Count')
    # plt.legend()
    # plt.show()

    # by_month(months_data)

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




    ##Incidents by day of the week##
    # x,y = np.loadtxt(daily_data, delimiter=',', unpack=True)
    # plt.bar(x, y, label='Daily Incident Count')
    # slices = y
    # xticks = ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday']
    # colors = ('r', 'Orange', 'Yellow', 'green','Teal', 'Purple', 'Fuchsia')
    # pielist = plt.pie(slices,
    #                   labels=xticks,
    #                   colors=colors,
    #                   startangle=180,
    #                   shadow=False,
    #                   autopct='%1.1f%%')
    #  plt.xticks(x, xticks)
    #  plt.xlabel('Day')
    #  plt.ylabel('Incidents that Occurred')
    # plt.title('Incident Count by Day of Week')
    #  plt.legend()
    # plt.show()

    ##Incidents by type of Occurrence##
    x, y = np.loadtxt(problem_data, delimiter=',', unpack=True)
    slices = y
    colors = ('b', 'g', 'r', 'chartreuse', 'm', 'k')
    colors = ('#fa0012', '#ffa500', '#00b6a3', '#c200fb', '#05e662', 'k')
    occurrence_list = ['Unknown Injuries', 'Delayed', 'No Injuries', 'Injuries', 'Entrapment', 'Mass Casualty']
    pielist = plt.pie(slices,
                      labels=occurrence_list,
                      colors=colors,
                      startangle=180,
                      shadow=False,
                      explode=(0, 0, 0, 0, 0.4, 0.4),
                      autopct='%1.1f%%')

    plt.title('Incident Count by Severity')
    plt.show()

    # calldata = "TemperatureYData.csv"
    # y, x = np.loadtxt(calldata, delimiter=',', unpack=True)
    # plt.plot(x, y, 'rX', label='Temperature Data')
    # plt.title("Temperature Scatterplot")
    # plt.show()


if __name__ == "__main__":
    main()
