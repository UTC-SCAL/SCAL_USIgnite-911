##  This file is kept empty for testing small chunks of code easily. Please clear this file when you are done working on the code, and put it into 
#       whatever file it needs to go in. 


# import arcpy
# import pandas as pd

# #Call the file you want to manipulate
# grids = r'/home/pete/Downloads/Python Help/Grid_Accident_Times_1.shp'


# #Assign a variable to the field attributes
# field_list = arcpy.ListFields(grids)
# list_field = []

# #Print out the name and type of the fields in the file
# for x in field_list:
#     print(x.name)
#     print(x.type)


# #Call specific fields for manipulation
# with arcpy.da.UpdateCursor(grids, ['Accident', 'Hour', 'Grid_Count']) as grid_cursor:
#     for x in grid_cursor:
#         x['Grid_Count'] = dataframe.groupby(['Accident', 'Hour']).transform('Grid_Count')
#     grid_cursor.updateRow(x)

