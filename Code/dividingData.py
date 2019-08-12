import pandas
import feather




def dividing_data(accidents, negatives, accident_percent):
    num_accidents = len(accidents)
    currentNeg = len(negatives)

    wantNeg = round((((num_accidents*100)/accident_percent)-num_accidents))
    divisionInt = round((currentNeg/wantNeg))

    cutNegatives = negatives.iloc[::divisionInt, :]
    data = cutNegatives.append(accidents)
    data = data.sort_values(["Unix", "Grid_Block"])
    return data


# calldata = pandas.read_csv("../Excel & CSV Sheets/Accident Only Files/2017+2018 Accidents.csv")
# main_df = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/Randoms/NS Random Master List.csv")

dataset = pandas.read_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/NegativeSampling/GridFixed/NS True GridFix MMR.csv")
# file = "/media/pete/USB DISK/2019 Grid Data Spatial Master List MMR.feather"
# dataset = feather.read_dataframe(file)
accidents = dataset.loc[dataset['Accident'] == 1]
negatives = dataset.loc[dataset['Accident'] == 0]
# main_df = main_df.append(calldata)
# print(main_df.columns)

main_df = dividing_data(accidents, negatives, 50)

# exit()
main_df.to_csv("../Excel & CSV Sheets/Grid Oriented Layout Test Files/True Gridfix 50-50.csv")