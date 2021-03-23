

"""https://oda.ft.dk/api/Aktør?$expand=Stemme&$filter=id eq 5"""


"""https://oda.ft.dk/api/Akt%C3%B8r?$expand=Stemme&$filter=id%20eq%205&$select=navn,Stemme/id,Stemme/typeid,Stemme/afstemningid""" #Henter alle stemmer (id,typeid,afstemningid) for aktør med id = 5 (Frank Aaen)

"""https://oda.ft.dk/api/M%C3%B8de?$expand=Afstemning&$filter=Afstemning/any()"""
#Hent alle møder med mindst 1 afstemning

""" https://oda.ft.dk/api/Afstemning(1)?$expand=Stemme/Akt%C3%B8r,M%C3%B8de/Afstemning """
# Afstemning nummer 1
