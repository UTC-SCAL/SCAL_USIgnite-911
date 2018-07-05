import pandas


station_matches = pandas.DataFrame(columns=["KTNBAKEW3", "KTNCHATT121", "KTNCHATT88", "KTNHARRI26", "KTNSODDY29",
                                            "KTNCHATT103", "KTNCHATT112", "KTNCOLLE5", "KTNSODDY6"])


station_matches.ix[:"KTNBAKEW3"] = "testing"

print(station_matches.head())
