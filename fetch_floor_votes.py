from json.decoder import JSONDecodeError
import multiprocessing

from bs4.element import AttributeValueWithCharsetSubstitution
from joblib.parallel import Parallel


def get_votes(member):
    import requests
    import pandas as pd 
    import json 
    base_url = r"https://oda.ft.dk/api/Stemme?$inlinecount=allpages&$filter=akt%C3%B8rid%20eq%20"
    vote_types = {
        1: "For",
        2: "Imod",
        3: "Fravær",
        4: "Hverken for eller imod"
    }
    votes = {
        'id': [],
        'vote': [],
        'type': []
    }
    vote_url = base_url + str(member)
    out_df = pd.DataFrame(columns=["id","vote","type"])
    votes_raw = requests.get(vote_url).content
    votes_json_raw = json.loads(votes_raw)
    try: 
        while votes_json_raw["odata.nextLink"]:
        # print(votes)
            votes_json = votes_json_raw["value"]
            
            # print(votes_json)
            for i in votes_json:
                votes["id"].append(i['id'])
                votes["vote"].append(i['afstemningid'])
                votes["type"].append(vote_types[i["typeid"]])
            vote_df = pd.DataFrame.from_dict(votes)
            out_df = out_df.append(vote_df,ignore_index=True)
            try: 
                next_url = votes_json_raw["odata.nextLink"]
                votes_raw = requests.get(next_url).content
                votes_json_raw = json.loads(votes_raw)
            except KeyError:
                break 
    except KeyError:
        votes_json = votes_json_raw["value"]
        # print(votes_json)
        for i in votes_json:
            votes["id"].append(i['id'])
            votes["vote"].append(i['afstemningid'])
            votes["type"].append(vote_types[i["typeid"]])
        vote_df = pd.DataFrame.from_dict(votes)
        out_df = out_df.append(vote_df,ignore_index=True)
    out_df = out_df.drop_duplicates()
    return out_df

def get_vote_details(vote):
    import requests
    import pandas as pd 
    import json 
    from bs4 import BeautifulSoup as Soup
    url = f"https://oda.ft.dk/api/Afstemning({vote})/Sagstrin?$inlinecount=allpages"
    raw_data = requests.get(url).content
    # print(raw_data)
    try: 
        json_data = json.loads(raw_data)
        subject = json_data["sagid"]
        actors = {}
        new_url = f"https://oda.ft.dk/api/Sag({subject})/SagAkt%C3%B8r?$inlinecount=allpages"
        new_data = requests.get(new_url).content
        new_json = json.loads(new_data)
        for value in new_json["value"]:
            actors[value["aktørid"]] = value["rolleid"]
        out_dict = {"vote_id": vote, "sagid": subject, "sponsors": []}
        for actor in actors.keys():
            if actors[actor] == 16 or actors[actor] == 19: 
                actor_data = requests.get(f"https://oda.ft.dk/api/Aktør({actor})").content
                actor_data = json.loads(actor_data)
                raw_soup = actor_data["biografi"]
                try: 
                    raw_soup = Soup(str(raw_soup), "lxml").find("party").text
                except AttributeError:
                    raw_soup = "Not Applicable"
                out_dict["sponsors"].append({"name": actor_data["navn"], "party": raw_soup})
        return out_dict
    except JSONDecodeError: 
        return None

def get_all_votes():
    import requests 
    import json 
    from joblib import parallel, delayed
    url = "https://oda.ft.dk/api/Afstemning?$inlinecount=allpages"
    votes = []
    data = requests.get(url).content
    json_data = json.loads(data)
    next_url = json_data["odata.nextLink"]
    vote_dict = {}
    while next_url:
        for vote in json_data["value"]:
            votes.append(vote["id"])
        data = requests.get(next_url).content
        json_data = json.loads(data)
        try: 
            next_url = json_data["odata.nextLink"]
        except KeyError:
            next_url = False
    count = 0 
    num_cores = multiprocessing.cpu_count()-1
    def processInput(vote):
        print(vote)
        tmp_dict = get_vote_details(vote)
        # if count % 100 == 0:
        with open(f"votes/{vote}.json", "w") as outfile:
            outfile.write(json.dumps(tmp_dict, indent=4,sort_keys=True, ensure_ascii=False))
    Parallel(n_jobs=num_cores)(delayed(processInput)(i) for i in votes)

    # for vote in votes: 
        # count += 1
        # print(vote)
        # vote_dict[vote] = get_vote_details(vote)
        
    # with open("votes.json", "w") as outfile:
    #     outfile.write(json.dumps(vote_dict, indent=4,sort_keys=True, ensure_ascii=False))
    return 

get_all_votes()