import os
os.system("ls party*/*.tex > tmp.txt")
list_names = []
with open("tmp.txt","r") as f:
    tmp = f.read().split("\n")
    for i in tmp:
        list_names.append(i)
for i in list_names:
    os.system("xelatex {}".format(i))
    print(i)
#print(os.listdir("./party_S"))
