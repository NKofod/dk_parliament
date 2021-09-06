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
    return print(out_df)

get_votes(158)
