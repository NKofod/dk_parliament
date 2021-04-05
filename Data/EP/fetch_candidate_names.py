import pandas as pd

data = pd.read_csv("Kandidater_stamdata.csv",sep=";",engine="python")
# print(data.columns)
outdata = data[data.columns[0:5]]
print(outdata)
for infile in ["Kandidater_stamdata (1).csv",
          "Kandidater_stamdata (2).csv",
          "Kandidater_stamdata (3).csv",
          "Kandidater_stamdata (4).csv"]:
    data = pd.read_csv(infile,sep=";",engine="python")
    tmp_data = data[data.columns[0:5]]
    outdata = outdata.append(tmp_data)
print(outdata)