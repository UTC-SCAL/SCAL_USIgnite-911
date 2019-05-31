import numpy
import pandas

roadfile = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/GridCountRoads.csv")
highwayfile = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/Highway.csv")
blockstodrop = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/BlocksToDrop.csv")
gridinfo = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/GridInfo.csv")
# print(roadfile.head())
# print(highwayfile.head())
# print(blockstodrop.head())\
def droppingGridblocks(blockstodrop, gridblocks):
    gridblockscopy = gridblocks.copy()
    for i, info in enumerate(gridblocks.values):
        for k, thing in enumerate(blockstodrop.values):
            if blockstodrop.Grid_Block.values[k] == gridblocks.Grid_Block.values[i]:
                # print("Dropping : ", blockstodrop.Grid_Block.values[k], gridblocks.Grid_Block.values[i])
                gridblockscopy = gridblockscopy.drop([i],axis=0)
    return gridblockscopy


# print(len(highwayfile))
# cuthighway = droppingGridblocks(blockstodrop, highwayfile)
# print(len(cuthighway))

# print(len(roadfile))
# cutroad = droppingGridblocks(blockstodrop, roadfile)
# print(len(cutroad))

# print(len(gridinfo))
# gridinfocut = droppingGridblocks(blockstodrop, gridinfo)
# print(len(gridinfocut))


for j, info in enumerate(gridinfo.values): 
    print(j)
    for i, stuff in enumerate(roadfile.values):
        if gridinfo.Grid_Block.values[j] == roadfile.Grid_Block.values[i]:
            gridinfo.Road_Count.values[j] = int(roadfile.Road_Count.values[i])

print(gridinfo.head())
gridinfocut = droppingGridblocks(blockstodrop, gridinfo)
gridinfocut.to_csv('../Excel & CSV Sheets/Grid Layout Test Files/GridInfoCutandUpdated.csv')
