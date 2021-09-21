


def fetch_periods(): 
    import requests 
    import json 
    base_url = "https://oda.ft.dk/api/Periode?$inlinecount=allpages"
    outDict = {}
    while base_url:
        inData = requests.get(base_url).content
        jsonData = json.loads(inData)
        periodData = jsonData["value"]
        for entry in periodData:
            outDict[entry['id']] = {
                'startdate': entry['startdato'].split("T")[0],
                'enddate': entry['slutdato'].split("T")[0],
                'type': entry['type']
            }
        try: 
            base_url = jsonData['odata.nextLink']
        except KeyError:
            base_url = False 
    with open("periods.json", "w") as outfile:
        outfile.write(json.dumps(outDict))
    return 

fetch_periods()


def fetch_group(id,outfile):
    print(f"Fetching {outfile}")
    import requests 
    import json 
    base_url = r"https://oda.ft.dk/api/Aktør?$inlinecount=allpages&$filter=typeid%20eq%20" + str(id)
    out_dict = {}
    finished = False
    counter = 0 
    while not finished:
        print(counter)
        counter += 1
        in_data = requests.get(base_url).content
        json_data = json.loads(in_data)
        group_data = json_data["value"]
        for group in group_data:
            tmp_dict = {}
            var_name_list = [
                "id",
                "name",
                "short_name",
                "start",
                "end",
                "periodid"
            ]
            var_list = [
                'id',
                'navn',
                'gruppenavnkort',
                'startdato',
                'slutdato',
                'periodeid'
            ]
            for entry in range(len(var_name_list)):
                try:
                    tmp_dict[var_name_list[entry]] = group[var_list[entry]]
                except KeyError:
                    tmp_dict[var_name_list[entry]] = None 
            if tmp_dict['start'] != None:
                tmp_dict['start'] = tmp_dict['start'].split("T")[0]
            if tmp_dict['end'] != None:
                tmp_dict['end'] = tmp_dict['end'].split("T")[0]

            out_dict[tmp_dict['id']] = tmp_dict
        try: 
            base_url = json_data["odata.nextLink"]
        except KeyError:
            finished = True
    with open(outfile, "w") as f:
        f.write(json.dumps(out_dict,indent=4,ensure_ascii=False))


def fetch_groups():
    in_dict = {
        1: "minister_area.json",
        2: "ministertitle.json",
        3: "committee.json",
        4: "party.json",
        5: "person.json",
        6: "group.json",
        7: "other_group.json",
        8: "ministry.json",
        9: "commission.json",
        10: "organisation.json",
        11: "parlamentary.json",
        12: "private_citizen.json",
        13: "political_network.json",
    }
    for i in in_dict.keys():
        fetch_group(i, in_dict[i])
    
fetch_groups()
def fetch_actors():
    import requests
    import json 
    base_url = r"https://oda.ft.dk/api/Akt%C3%B8r?$inlinecount=allpages"
    finished = False 
    out_dict = {}
    count = 0
    while not finished:
        print(count)
        count += 1
        in_data = requests.get(base_url).content
        json_data = json.loads(in_data)
        for val in json_data["value"]:
            out_dict[val["id"]] = {
                "name": val["navn"],
                "type": val["typeid"],
            }
        try: 
            base_url = json_data["odata.nextLink"]
        except KeyError:
            finished = True
    with open("actors.json", "w") as f:
        f.write(json.dumps(out_dict,indent=4,ensure_ascii=False))


def fetch_actor_roles():
    import requests
    import json 
    base_url = r"https://oda.ft.dk/api/Akt%C3%B8rAkt%C3%B8rRolle?$inlinecount=allpages"
    in_data = requests.get(base_url).content
    json_data = json.loads(in_data)
    out_dict = {}
    for role in json_data["value"]:
        out_dict[role["id"]] = role["rolle"]
    with open("roles.json", "w") as f: 
        f.write(json.dumps(out_dict,indent=4,ensure_ascii=False))
    return out_dict

fetch_actor_roles()

def fetch_actor_relationships():
    import requests
    import json 
    with open("person.json", "r") as f:
        person_dict = json.loads(f.read())
    with open("roles.json", "r") as f: 
        role_dict = json.loads(f.read())
    with open("periods.json","r") as f: 
        period_dict = json.loads(f.read())
    # out_dict = {}
    group_dict = {
        1: "Ministerområde",
        2: "Ministertitel",
        3: "Udvalg",
        4: "Folketingsgruppe",
        5: "Person",
        6: "Gruppe",
        7: "Anden gruppe",
        8: "Ministerium",
        9: "Kommission",
        10: "Organisation",
        11: "Parlamentarisk Forsamling",
        12: "Privat Borger",
        13: "Tværpolitisk netværk"
    }
    file_dict = {
        1: "minister_area.json",
        2: "ministertitle.json",
        3: "committee.json",
        4: "party.json",
        5: "person.json",
        6: "group.json",
        7: "other_group.json",
        8: "ministry.json",
        9: "commission.json",
        10: "organisation.json",
        11: "parlamentary.json",
        12: "private_citizen.json",
        13: "political_network.json",
    }
    with open("actors.json", "r") as f: 
        actor_dict = json.loads(f.read())
    for person in person_dict["null"]:
        print(person["id"])
        out_dict = {}
        for actortype in ["til", "fra"]:
            base_url = f"https://oda.ft.dk/api/Akt%C3%B8rAkt%C3%B8r?$inlinecount=allpages&$filter={actortype}akt%C3%B8rid%20eq%20" + str(person["id"])
            finished = False 
            while not finished:
                in_data = requests.get(base_url).content
                json_data = json.loads(in_data)
                group_data = json_data["value"]
                for group in group_data:
                    tmp_dict = {}
                    var_list = [
                        "id", 
                        "fraaktørid", 
                        "tilaktørid", 
                        "startdato", 
                        "slutdato", 
                        "rolleid"
                        ]
                    var_name_list = [
                        "id",
                        "from_actor",
                        "to_actor",
                        "start",
                        "end",
                        "role"
                    ]

                    for i in range(len(var_list)):
                        try: 
                            tmp_dict[var_name_list[i]] = group[var_list[i]]
                        except KeyError:
                            tmp_dict[var_name_list[i]] = None
                        
                    if tmp_dict["role"] != None:
                        tmp_dict["role"] = role_dict[str(tmp_dict["role"])]
                    tmp_dict["from_actor_name"] = actor_dict[str(group["fraaktørid"])]["name"]
                    tmp_dict["to_actor_name"] = actor_dict[str(group["tilaktørid"])]["name"]
                    if actortype == "fra":
                        tmp_dict["type"] = group_dict[actor_dict[str(group["tilaktørid"])]["type"]]
                        if tmp_dict["start"] == None:
                            with open(str(file_dict[actor_dict[str(group["tilaktørid"])]["type"]]),"r") as tmpfile:
                                tmp_dict_two = json.loads(tmpfile.read())
                            tmp_dict_two = tmp_dict_two[f"{group['tilaktørid']}"]
                            if tmp_dict["end"] == None:
                                if tmp_dict_two["end"] == None or tmp_dict_two["start"] == None:
                                    tmp_start = period_dict[f"{tmp_dict_two['periodid']}"]["startdate"]
                                    tmp_end = period_dict[f"{tmp_dict_two['periodid']}"]["enddate"]
                                    tmp_dict["start"] = tmp_start
                                    tmp_dict["end"] = tmp_end
                                else: 
                                    tmp_dict["start"] = tmp_dict_two["start"]
                                    tmp_dict["end"] = tmp_dict_two["end"]
                            else: 
                                if tmp_dict_two["start"] == None:
                                    tmp_start = period_dict[f"{tmp_dict_two['periodid']}"]["startdate"]
                                    tmp_dict["start"] = tmp_start
                                else:
                                    tmp_dict["start"] = tmp_dict_two["start"]
                        elif tmp_dict["end"] == None:
                            with open(str(file_dict[actor_dict[str(group["tilaktørid"])]["type"]]),"r") as tmpfile:
                                tmp_dict_two = json.loads(tmpfile.read())
                            tmp_dict_two = tmp_dict_two[f"{group['tilaktørid']}"]
                            if tmp_dict_two["end"] == None: 
                                tmp_end = period_dict[f"{tmp_dict_two['periodid']}"]["enddate"]
                                tmp_dict["end"] = tmp_end
                            else: 
                                tmp_dict["end"] = tmp_dict_two["end"]
                    else:
                        tmp_dict["type"] = group_dict[actor_dict[str(group["fraaktørid"])]["type"]]
                    try: 
                        out_dict[group[f"{actortype}aktørid"]].append(tmp_dict)
                    except KeyError:
                        out_dict[group[f"{actortype}aktørid"]] = []
                        out_dict[group[f"{actortype}aktørid"]].append(tmp_dict)
                    
                try: 
                    base_url = json_data["odata.nextLink"]
                except KeyError:
                    finished = True
                out_id = group[f"{actortype}aktørid"]
        if out_dict != {}:
            with open(f"relationships/{out_id}.json", "w") as f:
                f.write(json.dumps(out_dict,indent=4,ensure_ascii=False))
fetch_actors()
fetch_actor_relationships()
# fetch_actor_relationships()
# 