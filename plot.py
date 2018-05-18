import matplotlib as plt
from mapsplotlib import mapsplot as mplt
import pandas

if __name__ == "__main__":
	mplt.register_api_key('AIzaSyBVSgGHRDKMK5y3n0nCCfju5C5Xo4k6BN8')
	data_frame = pandas.read_csv("./Call_Information.csv", index_col=0, parse_dates=True)
	for index, val in enumerate(data_frame.copy().values):
		val[0] = float(val[0])
		val[1] = float(val[1])
	mplt.density_plot(data_frame[data_frame.columns[0]], data_frame[data_frame.columns[1]])
