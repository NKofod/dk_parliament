import pandas as pd
import re

outdata = pd.DataFrame(columns=["Gruppe", "ValgstedId", "KredsNr", "StorKredsNr", "LandsdelsNr","Stemmer", "Valg", "Parti", "Rang"])

read_list = ["Valgdata_-_personlige_stemmer.csv",
             "Valgdata_-_personlige_stemmer (1).csv",
             "Valgdata_-_personlige_stemmer (2).csv",
             "Valgdata_-_personlige_stemmer (3).csv",
             "Valgdata_-_personlige_stemmer (4).csv"]

for infile in read_list:
    data = pd.read_csv(infile,sep='";"',engine="python")
    print(data)
    tmp_list = list(data.columns)
    length = len(data["Gruppe"])
    #print(tmp_list)
    # with open("test_2.txt", "w") as f:
    #     for i in tmp_list:
    #         f.write(i+"\n")

    for i in tmp_list:
        if re.search("^EV\d{4} - personlige stemmer i alt$", i, re.IGNORECASE) != None:
            #print("Parti: Total, Rank: Total")
            tmp_data = pd.DataFrame(data[list(data.columns)[0:5]])
            tmp_data["Stemmer"] = list(data[i])
            tmp_data["Parti"] = ["Total"]*length
            tmp_data["Rang"] = ["Total"]*length
            tmp_data["Valg"] = [i[2:6]]*length
            outdata = outdata.append(tmp_data,ignore_index=True)
            # print(outdata)
            #print(election)
        elif re.search("^EV\d{4} - \w{1} - personlige stemmer i alt$", i, re.IGNORECASE) != None:
            #print("Parti fundet, Rank: Total")
            tmp_data = pd.DataFrame(data[list(data.columns)[0:5]])
            tmp_data["Stemmer"] = list(data[i])
            tmp_data["Parti"] = [i[9:10]] * length
            tmp_data["Rang"] = ["Total"] * length
            tmp_data["Valg"] = [i[2:6]] * length
            outdata = outdata.append(tmp_data, ignore_index=True)
            # print(outdata)
        elif re.search("^EV\d{4} - \w{2} - personlige stemmer i alt$", i, re.IGNORECASE) != None:
            #print("Parti fundet, Rank: Total")
            tmp_data = pd.DataFrame(data[list(data.columns)[0:5]])
            tmp_data["Stemmer"] = list(data[i])
            tmp_data["Parti"] = [i[9:11]] * length
            tmp_data["Rang"] = ["Total"] * length
            tmp_data["Valg"] = [i[2:6]] * length
            outdata = outdata.append(tmp_data, ignore_index=True)
            # print(outdata)
        elif re.search("^EV\d{4} - .{1} - personlige stemmer i alt$", i, re.IGNORECASE) != None:
            # print("Parti: Enhedslisten, Rank: Total")
            tmp_data = pd.DataFrame(data[list(data.columns)[0:5]])
            tmp_data["Stemmer"] = list(data[i])
            tmp_data["Parti"] = ["Ø"] * length
            tmp_data["Rang"] = ["Total"] * length
            tmp_data["Valg"] = [i[2:6]] * length
            outdata = outdata.append(tmp_data, ignore_index=True)
            # print(outdata)
        elif re.search("^EV\d{4} - .{1} - personlige stemmer i alt.1$", i, re.IGNORECASE) != None:
            # print("Parti: Alternativet, Rank: Total")
            tmp_data = pd.DataFrame(data[list(data.columns)[0:5]])
            tmp_data["Stemmer"] = list(data[i])
            tmp_data["Parti"] = ["Å"] * length
            tmp_data["Rang"] = ["Total"] * length
            tmp_data["Valg"] = [i[2:6]] * length
            outdata = outdata.append(tmp_data, ignore_index=True)
            # print(outdata)
        elif re.search("^EV\d{4}\s-\s\w{1}-\d{2}$",i) != None:
            # print("Rank og parti fundet.")
            tmp_data = pd.DataFrame(data[list(data.columns)[0:5]])
            tmp_data["Stemmer"] = list(data[i])
            tmp_data["Parti"] = [i[9:10]] * length
            tmp_data["Rang"] = [i[11:13]] * length
            tmp_data["Valg"] = [i[2:6]] * length
            outdata = outdata.append(tmp_data, ignore_index=True)
            # print(outdata)
        elif re.search("^EV\d{4}\s-\s\w{2}-\d{2}$",i) != None:
            # print("Rank og parti fundet.")
            tmp_data = pd.DataFrame(data[list(data.columns)[0:5]])
            tmp_data["Stemmer"] = list(data[i])
            tmp_data["Parti"] = [i[9:11]] * length
            tmp_data["Rang"] = [i[12:14]] * length
            tmp_data["Valg"] = [i[2:6]] * length
            outdata = outdata.append(tmp_data, ignore_index=True)
            #print(outdata)
        elif re.search("^EV\d{4}\s-\s.-\d{2}$",i) != None:
            # print("Rank og Enhedslisten fundet.")
            tmp_data = pd.DataFrame(data[list(data.columns)[0:5]])
            tmp_data["Stemmer"] = list(data[i])
            tmp_data["Parti"] = ["Ø"] * length
            tmp_data["Rang"] = [i[11:13]] * length
            tmp_data["Valg"] = [i[2:6]] * length
            outdata = outdata.append(tmp_data, ignore_index=True)
            #print(outdata)
        elif re.search("^EV\d{4}\s-\s.-\d{2}.1$",i) != None:
            # print("Rank og Alternativet fundet.")
            tmp_data = pd.DataFrame(data[list(data.columns)[0:5]])
            tmp_data["Stemmer"] = list(data[i])
            tmp_data["Parti"] = ["Å"] * length
            tmp_data["Rang"] = [i[12:14]] * length
            tmp_data["Valg"] = [i[2:6]] * length
            outdata = outdata.append(tmp_data, ignore_index=True)
            #print(outdata)
# tmp_list_2 = tmp_list[0:5]
# tmp_db = data[tmp_list_2]
# tmp_db = tmp_db.append(tmp_db)
print(outdata)
outdata.to_csv("out.csv",sep=";")
