import requests
from bs4 import BeautifulSoup as soup
import json
from urllib.request import urlopen
import pandas as pd
import time

def kommune(output):
    postnummer_url = "https://dawa.aws.dk/postnumre"
    url_open = urlopen(postnummer_url)
    postnummer_raw = url_open.read()
    json_postnummer = json.loads(postnummer_raw)
    filename_postnummer = output
    f = open(filename_postnummer, "w")
    headers = "Postnummer; Kommuneid \n"
    f.write(headers)
    for postnummer in json_postnummer:
        tmp_string = ""
        tmp_string += postnummer["nr"] + ";"
        tmp_string += postnummer["kommuner"][0]["kode"] + "\n"
        f.write(tmp_string)
    f.close()
    return json_postnummer

def storkreds(output):
    valg_url = "https://dawa.aws.dk/opstillingskredse/"
    url_open = urlopen(valg_url)
    valg_raw = url_open.read()
    json_valg = json.loads(valg_raw)
    filename_opstilling = output
    f = open(filename_opstilling, "w")
    headers = "Kommuneid ; Storkredsid \n"
    f.write(headers)
    dictionary = []
    for kreds in json_valg:
        tmp_string = ""
        storkreds = kreds["storkreds"]
        tmp_string += kreds["kredskommune"]["kode"] + ";"
        tmp_string += kreds["storkreds"]["nummer"] + "\n"
        f.write(tmp_string)
        tmp_dict = {}
        tmp_dict["kommuneid"] = kreds["kredskommune"]["kode"]
        tmp_dict["storkreds"] = kreds["storkreds"]["nummer"]
        dictionary.append(tmp_dict)
    df = pd.DataFrame.from_dict(dictionary)
    print(df)
    f.close()
    return df

def kandidat():
    url = "https://www.dst.dk/valg/Valg1684447/xml/fintal.xml"
    url_open = urlopen(url)
    fintal_raw = url_open.read()
    fintal_soup = soup(fintal_raw, "xml")
    fintal_soup = fintal_soup.findAll("Storkreds", {})
    kandidater = []
    for i in fintal_soup:
        time.sleep(0.5)
        print(i.text)
        url = i["filnavn"]
        url_open = urlopen(url)
        tmp_raw = url_open.read()
        tmp_soup = soup(tmp_raw, "xml")
        tmp_soup_personer = tmp_soup.findAll("Personer", {})[0]
        # print(tmp_soup_personer)
        tmp_soup_personer = tmp_soup.findAll("Parti", {})
        # print(tmp_soup_personer)
        # print(storkreds.text)
        for parti in tmp_soup_personer:
            tmp_one = parti.findAll("Person", {})
            # print(tmp_one)
            for person in tmp_one:
                if person["Navn"] == "Lars Chr. Lilleholt":
                    person["Navn"] = "Lars Christian Lilleholt"
                elif person["Navn"] == "Lisbeth Bech Poulsen":
                    person["Navn"] = "Lisbeth Bech-Nielsen"
                elif person["Navn"] == "Jens Henrik W. Thulesen Dahl":
                    person["Navn"] = "Jens Henrik Thulesen Dahl"
                # print(person)
                kandidater.append({"Navn": person["Navn"], "Parti": parti["Bogstav"], "Storkreds": i.text,
                                   "Storkredsid": i["storkreds_id"],
                                   "Personlige Stemmer": person["PersonligeStemmer"],
                                   "Tildelte Partistemmer": person["TildeltePartiStemmer"],
                                   "Stemmer i alt": person["StemmerIAlt"]})
                # print(person["Navn"])
        # for i in kandidater:
        #     print(i["Navn"] + " fra " + i["Parti"] + " i " + i["Storkreds"])
    return kandidater
# print(kandidater())


def folketing():
    ft_url = "https://oda.ft.dk/api/"
    vote_url = "Afstemning?$inlinecount=allpages"
    tmp_url = ft_url + vote_url
    url_open = urlopen(tmp_url)
    tmp_raw = url_open.read()
    json_raw = json.loads(tmp_raw)
    count_votes = json_raw["odata.count"]
    count_votes = int(count_votes) - 100
    count_votes = str(count_votes)
    new_url = ft_url + "Afstemning(" + count_votes + ")/Stemme?$inlinecount=allpages"
    url_open_new = urlopen(new_url)
    tmp_new = url_open_new.read()
    json_new = json.loads(tmp_new)
    actor_id = []
    while True:
        try:
            next_url = json_new["odata.nextLink"]
            for elem in json_new["value"]:
                actor_id.append(elem["aktørid"])
            url_open_new = urlopen(next_url)
            tmp_new = url_open_new.read()
            json_new = json.loads(tmp_new)
        except KeyError as ke:
            for elem in json_new["value"]:
                actor_id.append(elem["aktørid"])
            break
    # print(len(actor_id))
    print(actor_id)
    actor_url = "Akt%C3%B8r?$filter=id%20eq%20"
    actors_list = []
    for actorid in actor_id:
        # print(actorid)
        print(str(((actor_id.index(actorid)+1)/len(actor_id))*100) + " %")
        url = ft_url + actor_url + str(actorid)
        url_open = urlopen(url)
        tmp_actor = url_open.read()
        tmp_json = json.loads(tmp_actor)
        tmp_json = tmp_json["value"][0]
        # print(tmp_json)
        actors_list.append({"Navn": tmp_json["navn"], "Folketingsid": actorid})
    print(actors_list)
    return actors_list


def folketingsmedlemmer():
    kandidater = kandidat()
    ft = folketing()
    actors_list_two = []
    for actors in ft:
        for person in kandidater:
            if person["Navn"] == actors["Navn"]:
                actors_list_two.append(
                    {"Navn": person["Navn"], "Parti": person["Parti"], "Storkreds": person["Storkreds"],
                     "Personlige Stemmer": person["Personlige Stemmer"], "Stemmer i alt": person["Stemmer i alt"],
                     "Folketingsid": actors["Folketingsid"]})
    actors_list_two = pd.DataFrame.from_dict(actors_list_two)
    filename = "kandidater.csv"
    actors_list_two.to_csv(filename, index=False)
    return actors_list_two


folketingsmedlemmer()