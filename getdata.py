import requests as rq
import json
import pandas as pd

url = "https://oda.ft.dk/api/Afstemning?$inlinecount=allpages&$skip=0"

def make_pd_frame(filename="personer.txt"):
    with open(filename,"r") as infile:
        df = pd.DataFrame(json.load(infile))
    no_dups = df.drop_duplicates()
    print(no_dups)
    exit()
   
def build_query(dict_keys):
    cols = ",".join(dict_keys)
    print(cols)
    url = f"https://oda.ft.dk/api/Akt%C3%B8r?$select=navn,id,typeid&$filter=typeid%20eq%205"
    data = rq.get(url).json()
    print(data["value"])

def hent_personer(filename="personer.txt"):
    url = f"https://oda.ft.dk/api/Akt%C3%B8r?$select=navn,id&$filter=typeid%20eq%205"
    with open(filename,"w") as jsonfile:
        jsonfile.write("[")
        data = rq.get(url).json()
        while True:
            try:
                next_url = data["odata.nextLink"]
                for elem in data["value"]:
                    elem["aktørid"] = elem.pop("id")
                    jsonfile.write(f"{json.dumps(elem,ensure_ascii=False)}, ")
                data = rq.get(next_url).json()
            except KeyError as ke:
                for elem in data["value"][:-1]:
                    elem["aktørid"] = elem.pop("id")
                    jsonfile.write(f"{json.dumps(elem,ensure_ascii=False)}, ")
                elem = data["value"][-1]
                elem["aktørid"] = elem.pop("id")
                jsonfile.write(f"{json.dumps(elem,ensure_ascii=False)}]")
                break
                

    print("all done")

def hent_stemmer_fra_aktørid(aktørid=5):
    url = (f"""https://oda.ft.dk/api/Stemme?"""
           f"""$select=id,typeid,afstemningid&$filter=akt%C3%B8rid%20eq%20{aktørid}""")
    #data = rq.get(url).json()
    with open("frank_aaen.txt","w") as jsonfile:
        jsonfile.write("[")
        data = rq.get(url).json()
        while True:
            try:
                next_url = data["odata.nextLink"]
                for elem in data["value"]:
                    elem["stemmeid"] = elem.pop("id")
                    jsonfile.write(f"{json.dumps(elem,ensure_ascii=False)}, ")
                data = rq.get(next_url).json()
            except KeyError as ke:
                for elem in data["value"][:-1]:
                    elem["stemmeid"] = elem.pop("id")
                    jsonfile.write(f"{json.dumps(elem,ensure_ascii=False)}, ")
                elem = data["value"][-1]
                elem["stemmeid"] = elem.pop("id")
                jsonfile.write(f"{json.dumps(elem,ensure_ascii=False)}]")
                break
                


#hent_personer()
hent_stemmer_fra_aktørid()
#make_pd_frame()
