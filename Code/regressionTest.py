import pandas
import statsmodels
import pylab
import numpy

def easy_import_excel_file(file_name):
    data_file_name = pandas.read_excel(file_name)
    return data_file_name

def main():
    file = "testCorrelationData.xlsx"
    test_file = easy_import_excel_file(file)
    print(test_file.head())
    print(list(test_file.columns))
