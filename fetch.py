# Import necessary libraries
import requests
from bs4 import BeautifulSoup as soup 
import json
from urllib.request import urlopen
import pandas as pd
import re

# url = "https://www.dst.dk/valg/Valg1684447/xml/fintal.xml"
# data = requests.get(url)
# data = data.content
# soup_data = soup(data,'lxml')
# print(soup_data)

data = pd.read_csv("Valgdata_-_personlige_stemmer.csv",sep='";"',engine="python")
tmp_list = list(data.columns)
tmp_list_2 = tmp_list[0:5]
print(len(tmp_list))
print(data[tmp_list_2])
for i in tmp_list[4:7]:
    election = i[2:6]
    print(election)
    if re.search() :
        print(i)
        party = "Total"
    else:
        party =
        print(i)
    tmp_2 = data[i].to_list()
    print(tmp_2)


