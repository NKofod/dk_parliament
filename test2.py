# Import necessary libraries
import requests
from bs4 import BeautifulSoup as soup 
import json
from urllib.request import urlopen

# Fetch municipalities
postnummer_url = "https://dawa.aws.dk/postnumre"
url_open = urlopen(postnummer_url)
postnummer_raw = url_open.read()
json_postnummer = json.loads(postnummer_raw)
json_string = json.dumps(json_postnummer)

print(json_postnummer)

# Fetch municipalities
postnummer_url = "https://dawa.aws.dk/postnumre"
url_open = urlopen(postnummer_url)
postnummer_raw = url_open.read()
json_postnummer = json.loads(postnummer_raw)
json_string = json.dumps(json_postnummer)

print(json_postnummer)

# Fetch election circuits
valg_url = "https://dawa.aws.dk/opstillingskredse/"
url_open = urlopen(valg_url)
valg_raw = url_open.read()
json_valg = json.loads(valg_raw)
json_string = json.dumps(json_valg)
# print(json_valg)

filename = "postnummer.csv"
f = open(filename, "w")
headers = "Postnummer ; Kommuneid ; Storkreds \n"
f.write(headers)

for postnummer in json_postnummer:
    kommune = postnummer["kommuner"][0]["kode"]
    for kreds in json_valg:
        if kreds["kredskommune"]["kode"] == kommune:
            storkreds = kreds["storkreds"]["nummer"]
            break
    nummer = postnummer["nr"]
    tmp_string = ""
    tmp_string += nummer + ";"
    tmp_string += kommune + ";"
    tmp_string += storkreds + "\n"
    f.write(tmp_string)

url = "https://www.dst.dk/valg/Valg1684447/xml/fintal.xml"
url_open = urlopen(url)
fintal_raw = url_open.read()
fintal_soup = soup(fintal_raw, "xml")
fintal_soup = fintal_soup.findAll("Storkreds", {})

url = fintal_soup[0]["filnavn"]
url_open = urlopen(url)
test_raw = url_open.read()
test_soup = soup(test_raw, "xml")
test_soup_personer = test_soup.findAll("Personer", {})[0]
test_soup_personer = test_soup_personer.findAll("Parti", {})

#test_soup_personer_parti = test_soup_personer.findAll("Parti", {})
#print(test_soup_personer)
tmp_two = []
# print(test_soup_personer[0].findAll("Person", {})[0]["Navn"])
for parti in test_soup_personer:
    tmp_one = parti.findAll("Person", {})
    for person in tmp_one: 
        #print(person["Navn"])
        tmp_two.append({"Navn": person["Navn"] , "Parti": parti["navn"], "Personlige Stemmer": person["PersonligeStemmer"], "Tildelte Partistemmer": person["TildeltePartiStemmer"], "Stemmer i alt": person["StemmerIAlt"]})
    
    
kandidater = []

for storkreds in fintal_soup: 
    url = storkreds["filnavn"]
    url_open = urlopen(url)
    tmp_raw = url_open.read()
    tmp_soup = soup(tmp_raw, "xml")
    tmp_soup_personer = tmp_soup.findAll("Personer", {})[0]
    tmp_soup_personer = tmp_soup.findAll("Parti", {})
    # print(storkreds.text)
    for parti in tmp_soup_personer:
        tmp_one = parti.findAll("Person", {})
        for person in tmp_one:
            if person["Navn"] == "Lars Chr. Lilleholt":
                person["Navn"] = "Lars Christian Lilleholt"
            elif person["Navn"] == "Lisbeth Bech Poulsen": 
                person["Navn"] = "Lisbeth Bech-Nielsen"
            elif person["Navn"] == "Jens Henrik W. Thulesen Dahl":
                person["Navn"] = "Jens Henrik Thulesen Dahl"
            kandidater.append({"Navn": person["Navn"] , "Parti": parti["Bogstav"], "Storkreds": storkreds.text, "Storkredsid": storkreds["storkreds_id"], "Personlige Stemmer": person["PersonligeStemmer"], "Tildelte Partistemmer": person["TildeltePartiStemmer"], "Stemmer i alt": person["StemmerIAlt"]})
            # print(person["Navn"])
print("Kandidater: " + str(len(kandidater)))
#print(kandidater)


ft_url = "https://oda.ft.dk/api/" 
vote_url = "Afstemning?$inlinecount=allpages"
tmp_url = ft_url + vote_url
print(tmp_url)

url_open = urlopen(tmp_url)
tmp_raw = url_open.read()
json_raw = json.loads(tmp_raw)
count_votes = json_raw["odata.count"]
print(count_votes)
count_votes = int(count_votes) - 100
count_votes = str(count_votes)

new_url = ft_url + "Afstemning(" + count_votes + ")/Stemme?$inlinecount=allpages" 
url_open_new = urlopen(new_url)
tmp_new = url_open_new.read()
json_new = json.loads(tmp_new)
actor_id = []
#print(json_new["odata.count"])
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
# #for i in json_new: 
#    actor_id.append(i["aktørid"])
# print(actor_id)
len(actor_id)
# print(json_new)

actor_url = "Akt%C3%B8r?$filter=id%20eq%20"

actors_list = []
for actorid in actor_id: 
    url = ft_url + actor_url + str(actorid)
    url_open = urlopen(url)
    tmp_actor = url_open.read()
    tmp_json = json.loads(tmp_actor)
    tmp_json = tmp_json["value"][0]
    #print(tmp_json)
    actors_list.append({"Navn": tmp_json["navn"], "Folketingsid": actorid})
    
#print(actors_list)
# len(actors_list)

actors_list_two = []

for actors in actors_list: 
    for person in kandidater:
        if person["Navn"] == actors["Navn"]:
            actors_list_two.append({"Navn": person["Navn"], "Parti": person["Parti"], "Storkreds": person["Storkreds"], "Personlige Stemmer": person["Personlige Stemmer"], "Stemmer i alt": person["Stemmer i alt"], "Folketingsid": actors["Folketingsid"]})
for actors in actors_list:
    count = 0 
    for person in kandidater: 
        if actors["Navn"] == person["Navn"]:
            count = 0
        else:
            count += 1
            # print(count)
    if count == 887: 
        print(actors["Navn"])
        
len(actors_list_two)
