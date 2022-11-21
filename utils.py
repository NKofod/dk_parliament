

def remove_special_characters(instring): 
    instring = str(instring)
    outstring = ""
    for i in instring:
        if i.isalnum() or i in [",", ".", " "]:
            outstring += i 
    return outstring

