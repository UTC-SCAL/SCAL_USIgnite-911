import matplotlib as plt
from mapsplotlib import mapsplot as mplt
import pandas
import re


if __name__ == "__main__":
	mplt.register_api_key('AIzaSyBXBus27V_niwl70utmPD75puZTauyR0Ic')
	with open ('./Call_Information.csv', 'r' ) as f:
		content = f.read()
	content_new = re.sub(r'.*\.,.*\n', '', content, flags = re.M)
	output = open('./Call_Information_No_Empties.csv', 'w')
	output.write(content_new)
	output.close()
	data_frame = pandas.read_csv('./Call_Information_No_Empties.csv', index_col=0, parse_dates=True)
	# We have to cast the lat and lon row to floats; it isn't already D:
	for index, val in enumerate(data_frame.copy().values):
		# Convert them to float:
		val[0] = float(val[0])
		val[1] = float(val[1])
	data_frame.columns = ['latitude', 'longitude', 'date', 'time', 'type', 'hour']
	mplt.heatmap(data_frame['latitude'], data_frame['longitude'], data_frame['hour'])
	# mplt.scatter(data_frame['latitude'], data_frame['longitude'], colors=data_frame['hour'])

