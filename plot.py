import matplotlib as plt
from mapsplotlib import mapsplot as mplt
import pandas

if __name__ == "__main__":
	mplt.register_api_key('AIzaSyBVSgGHRDKMK5y3n0nCCfju5C5Xo4k6BN8')
	data_frame = pandas.read_csv("./Call_Information.csv", index_col=0, parse_dates=True)



	data_frame[data_frame.columns[0]] = pandas.to_numeric(data_frame[data_frame.columns[0]], errors="coerce")
	data_frame[data_frame.columns[1]] = pandas.to_numeric(data_frame[data_frame.columns[1]], errors="coerce")
	mplt.density_plot(data_frame[data_frame.columns[0]], data_frame[data_frame.columns[1]])
