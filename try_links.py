import requests 
from joblib import Parallel, delayed
import multiprocessing
import time
import os 
import sys
base_link = "https://dst.dk/valg/Valg"
extention = "/xml/fintal.xml"

checked_list = []
start_time = time.time()
if os.path.isfile("checked_links.txt"):
    checked_list = open("checked_links.txt","r").read().split("\n")
    #print(checked_list)
else:
    pass 

inputs = range(1100000,2000000,100) 

def processInput(i):
    counter = 0
    tmp_list = []
    out_list = []
    for k in range(i,i+100):
        
        if str(k) in checked_list:
            continue 
        counter += 1
        try: 
            link_check = f"{base_link}{k}{extention}"
            tmp = requests.get(link_check)
            if str(tmp.status_code) == "200":
                out_list.append(k) 
                print(f"{k} works \t Note this down. ")
            else:
                print(f"{time.asctime()}\t{i}\t{str(k)[-3:]} is not an election.")
            tmp_list.append(k)
            if counter % 10 == 0:
                with open("checked_links.txt", "a") as f:
                    for link in tmp_list:
                        f.write(f"{link}\n")
            
                tmp_list = []
        except KeyboardInterrupt:
            sys.exit()
        except:
            continue 
    with open("checked_links.txt", "a") as f:
        for link in tmp_list:
            f.write(f"{link}\n")
    return out_list

num_cores = multiprocessing.cpu_count()
    
results = Parallel(n_jobs=num_cores)(delayed(processInput)(i) for i in inputs)
outfile = open("election_list.txt", "a")
for i in results:
    outfile.write(f"{i}\n")         
outfile.close()


