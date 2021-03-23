def get_data_subset_next(url,dict_keys):
    data = rq.get(url).json()
    sublist = [{k:elem.get(k,None) for k in dict_keys} for elem in data["value"]]
    key_url = data.get("odata.nextLink",None)
    return data,sublist,key_url

def get_and_write_json(url,dict_keys,filename,fmode="w"):
    data,sublist,key_url = get_data_subset_next(url,dict_keys)
    count = data["odata.count"]
    with open(filename,fmode) as ofile:
        ofile.write("[")
        for elem in sublist:
            ofile.write(f"{json.dumps(elem,ensure_ascii=False)}, ")
        for i in range(int(count)//100-1): #Alle undtagen de første og sidste
            data,sublist,key_url = get_data_subset_next(key_url,dict_keys)
            for elem in sublist:
                ofile.write(f"{json.dumps(elem,ensure_ascii=False)}, ")
        # Hent de sidste
        data,sublist,key_url = get_data_subset_next(key_url,dict_keys)
        for elem in sublist[:-1]:
            ofile.write(f"{json.dumps(elem,ensure_ascii=False)}, ")
        ofile.write(f"{json.dumps(sublist[-1],ensure_ascii=False)}]")
            
def get_aktører(dict_keys,filename="aktoerer.txt"):
    url = "https://oda.ft.dk/api/Akt%C3%B8r?$inlinecount=allpages&$skip=0"
    data = rq.get(url).json()
    count = data["odata.count"]
    sublist = [{k:elem.get(k,None) for k in dict_keys} for elem in data["value"]]
    with open(filename,"w") as ofile:
        ofile.write("[")
        for elem in sublist:
            ofile.write(f"{json.dumps(elem,ensure_ascii=False)}, ")
        for i in range(int(count)//100-1): #Alle undtagen de første og sidste
            key_url = data["odata.nextLink"]
            data = rq.get(key_url).json()
            sublist = [{k:elem.get(k,None) for k in dict_keys} for elem in data["value"]]
            for elem in sublist:
                ofile.write(f"{json.dumps(elem,ensure_ascii=False)}, ")

        # Hent de sidste
        key_url = data["odata.nextLink"]
        data = rq.get(key_url).json()
        sublist = [{k:elem.get(k,None) for k in dict_keys} for elem in data["value"]]
        for elem in sublist[:-1]:
            ofile.write(f"{json.dumps(elem,ensure_ascii=False)}, ")
        ofile.write(f"{json.dumps(sublist[-1],ensure_ascii=False)}]")
