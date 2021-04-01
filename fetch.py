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
print(tmp_list)
with open("test_2.txt", "w") as f:
    for i in tmp_list:
        f.write(i+"\n")

outdata = pd.DataFrame(columns=["Gruppe", "KredsNr", "StorKredsNr", "LandsdelsNr","Stemmer", "Valg", "Parti", "Rang"])
print(outdata)
for i in tmp_list:
    if re.search("^FV\d{4} - personlige stemmer i alt$", i, re.IGNORECASE) != None:
        print("Parti: Total, Rank: Total")
        tmp_data = pd.DataFrame(data[list(data.columns)[0:4]])
        tmp_data["Stemmer"] = list(data[i])
        tmp_data["Parti"] = ["Total"]*92
        tmp_data["Rang"] = ["Total"]*92
        tmp_data["Valg"] = [i[2:6]]*92
        outdata = outdata.append(tmp_data,ignore_index=True)
        # print(outdata)
        #print(election)
    elif re.search("^FV\d{4} - \w{1} - personlige stemmer i alt$", i, re.IGNORECASE) != None:
        #print("Parti fundet, Rank: Total")
        tmp_data = pd.DataFrame(data[list(data.columns)[0:4]])
        tmp_data["Stemmer"] = list(data[i])
        tmp_data["Parti"] = [i[9:10]] * 92
        tmp_data["Rang"] = ["Total"] * 92
        tmp_data["Valg"] = [i[2:6]] * 92
        outdata = outdata.append(tmp_data, ignore_index=True)
        # print(outdata)
    elif re.search("^FV\d{4} - \w{2} - personlige stemmer i alt$", i, re.IGNORECASE) != None:
        #print("Parti fundet, Rank: Total")
        tmp_data = pd.DataFrame(data[list(data.columns)[0:4]])
        tmp_data["Stemmer"] = list(data[i])
        tmp_data["Parti"] = [i[9:11]] * 92
        tmp_data["Rang"] = ["Total"] * 92
        tmp_data["Valg"] = [i[2:6]] * 92
        outdata = outdata.append(tmp_data, ignore_index=True)
        # print(outdata)
    elif re.search("^FV\d{4} - .{1} - personlige stemmer i alt$", i, re.IGNORECASE) != None:
        # print("Parti: Enhedslisten, Rank: Total")
        tmp_data = pd.DataFrame(data[list(data.columns)[0:4]])
        tmp_data["Stemmer"] = list(data[i])
        tmp_data["Parti"] = ["Ø"] * 92
        tmp_data["Rang"] = ["Total"] * 92
        tmp_data["Valg"] = [i[2:6]] * 92
        outdata = outdata.append(tmp_data, ignore_index=True)
        # print(outdata)
    elif re.search("^FV\d{4} - .{1} - personlige stemmer i alt.1$", i, re.IGNORECASE) != None:
        # print("Parti: Alternativet, Rank: Total")
        tmp_data = pd.DataFrame(data[list(data.columns)[0:4]])
        tmp_data["Stemmer"] = list(data[i])
        tmp_data["Parti"] = ["Å"] * 92
        tmp_data["Rang"] = ["Total"] * 92
        tmp_data["Valg"] = [i[2:6]] * 92
        outdata = outdata.append(tmp_data, ignore_index=True)
        # print(outdata)
    elif re.search("^FV\d{4}\s-\s\w{1}-\d{2}$",i) != None:
        # print("Rank og parti fundet.")
        tmp_data = pd.DataFrame(data[list(data.columns)[0:4]])
        tmp_data["Stemmer"] = list(data[i])
        tmp_data["Parti"] = [i[9:10]] * 92
        tmp_data["Rang"] = [i[11:13]] * 92
        tmp_data["Valg"] = [i[2:6]] * 92
        outdata = outdata.append(tmp_data, ignore_index=True)
        # print(outdata)
    elif re.search("^FV\d{4}\s-\s\w{2}-\d{2}$",i) != None:
        # print("Rank og parti fundet.")
        tmp_data = pd.DataFrame(data[list(data.columns)[0:4]])
        tmp_data["Stemmer"] = list(data[i])
        tmp_data["Parti"] = [i[9:11]] * 92
        tmp_data["Rang"] = [i[12:14]] * 92
        tmp_data["Valg"] = [i[2:6]] * 92
        outdata = outdata.append(tmp_data, ignore_index=True)
        #print(outdata)
    elif re.search("^FV\d{4}\s-\s.-\d{2}$",i) != None:
        # print("Rank og Enhedslisten fundet.")
        tmp_data = pd.DataFrame(data[list(data.columns)[0:4]])
        tmp_data["Stemmer"] = list(data[i])
        tmp_data["Parti"] = ["Ø"] * 92
        tmp_data["Rang"] = [i[11:13]] * 92
        tmp_data["Valg"] = [i[2:6]] * 92
        outdata = outdata.append(tmp_data, ignore_index=True)
        #print(outdata)
    elif re.search("^FV\d{4}\s-\s.-\d{2}.1$",i) != None:
        # print("Rank og Alternativet fundet.")
        tmp_data = pd.DataFrame(data[list(data.columns)[0:4]])
        tmp_data["Stemmer"] = list(data[i])
        tmp_data["Parti"] = ["Å"] * 92
        tmp_data["Rang"] = [i[12:14]] * 92
        tmp_data["Valg"] = [i[2:6]] * 92
        outdata = outdata.append(tmp_data, ignore_index=True)
        #print(outdata)
tmp_list_2 = tmp_list[0:5]
tmp_db = data[tmp_list_2]
tmp_db = tmp_db.append(tmp_db)
outdata.to_csv("out.csv",sep=";")
print(outdata)
print(len(tmp_list))
#print(data[tmp_list_2])
# for i in tmp_list[4:7]:
#     election = i[2:6]
#     print(election)
#     if re.search() :
#         print(i)
#         party = "Total"
#     else:
#         party =
#         print(i)
#     tmp_2 = data[i].to_list()
#     print(tmp_2)


