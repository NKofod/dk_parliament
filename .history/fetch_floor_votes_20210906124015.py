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
    votes_raw = requests.get(vote_url).content
    # print(votes)
    votes_json = json.loads(votes_raw)["value"]
    print(votes_json)
    for i in votes_json:
        votes["id"].append(i['id'])
        votes["vote"].append(i['afstemningid'])
        votes["type"].append(vote_types[i["typeid"]])
    vote_df = pd.DataFrame.from_dict(votes)
    return print(vote_df)

get_votes(158)
