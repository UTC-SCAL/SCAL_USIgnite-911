import pandas
import os, sys

path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'

grid_data = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/Grid Data 2017+2018.csv")
grid_info = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/GridInfoCutandUpdated.csv")
grid_data.Grid_Block = grid_data.Grid_Block.astype(str)
grid_info.Grid_Block = grid_info.Grid_Block.astype(str)

def find_road_data():
    for i, value in enumerate(grid_data.values):
        print(i)
        grid_block = grid_data.Grid_Block.values[i]
        # this is the row of the grid section file
        # this gets the row number based on the value passed to it, which is the date from the current accident
        # print("grid info: ", grid_data.Grid_Block.values[i])
        try:
            row_num = grid_info.loc[grid_info['Grid_Block'] == grid_data.Grid_Block.values[i]].index[0]
            grid_data.Highway.values[i] = grid_info.loc[row_num, "Highway"]
            grid_data.Land_Use_Mode.values[i] = grid_info.loc[row_num, "Land_Use_Mode"]
            grid_data.Road_Count.values[i] = grid_info.loc[row_num, "Road_Count"]
        except:
            print("no grid block match")


grid_data.to_csv("../Excel & CSV Sheets/Grid Layout Test Files/Grid Data 2017+2018.csv")
