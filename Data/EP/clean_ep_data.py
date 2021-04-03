import pandas as pd
import os
print(os.getcwd())
data = pd.read_csv("Valgdata_-_personlige_stemmer.csv", sep=";", engine="python")
print(data.columns)