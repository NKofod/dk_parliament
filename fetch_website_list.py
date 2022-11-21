import json 
import requests 
from bs4 import BeautifulSoup as Soup 
import os
import re 
import time
import sched
s = sched.scheduler(time.time, time.sleep)
tmp_data = open("elections.json","r").read()
in_data = json.loads(tmp_data)
link_check = []
if not os.path.isdir("tmp_data"):
    os.mkdir("tmp_data")
#print(in_data)
def try_link(link): 
    in_link = link
    tmp_time = time.time()
    try:
        trying = requests.get(in_link)
        return trying
    except requests.exceptions.ConnectionError:
        print("There seem to be noise on the line. Trying again in a minute or so...")
        time.sleep(60)
        try_link(in_link)

def find_links(link,in_list):
    tmp_list = in_list
    try:
        if re.search(r".{31}\w{0,2}\d+\w?\.html?", link['href']) is not None:
            tmp_string = re.sub(r".{31}(\w{0,2}\d+\w?\.html?)", r"\1", link['href'])
            # print(tmp_string)
            tmp_list.append(tmp_string)
        elif re.search(r".{10}\w{0,2}\d+\w?\.html?", link['href']) is not None:
            tmp_string = re.sub(r".{10}(\w{0,2}\d+\w?\.html?)", r"\1", link['href'])
            # print(tmp_string)
            tmp_list.append(tmp_string)
        elif re.search(r"\w{0,2}\d{2,}\w?\.html?", link['href']) is not None:
            tmp_list.append(link['href'])
        elif re.search(r"\w{3}\.html?", link['href']) is not None:
            tmp_list.append(link['href'])
        else:
            pass
        return tmp_list
    except KeyError:
        pass
def create_link_list(file,inlist):
    tmp_list = inlist
    try:
        with open(file, "r") as f:
            tmp = f.read().split("\n")
            for link in tmp:
                if link in tmp_list:
                    pass
                else:
                    tmp_list.append(link)
        return tmp_list
    except:
        return tmp_list

def run_prog():
    try:
        for i in in_data.keys():

            print(i)
            if not os.path.isdir(f"tmp_data/{i}"):
                    os.mkdir(f"tmp_data/{i}")
            for k in in_data[i].keys():
                counter = 0
                if not os.path.isdir(f"tmp_data/{i}/{k}"):
                    os.mkdir(f"tmp_data/{i}/{k}")
                checked_list = []
                checked_list = create_link_list(f"tmp_data/{i}/{k}/tmp.txt",checked_list)
                long_list = []
                long_list = create_link_list(f"tmp_data/{i}/{k}/unchecked_tmp.txt",long_list)
                tmp_list = []
                tmp_count = 0
                print(k)
                print(in_data[i][k]["link"])
                tmp_data = try_link(f"{in_data[i][k]['link']}")
                print(str(tmp_data.status_code))
                tmp_soup = Soup(tmp_data.content,"lxml")
                if tmp_soup.find("area") != None:
                    print(f"Area not none in {i} {k}")
                    tmp_link_list = tmp_soup.findAll("area")
                    for j in tmp_link_list:
                        tmp_links = find_links(j,tmp_list)
                else:
                    print(f"Area none in {i} {k}")
                    if tmp_soup.find("a",class_="valg-status-final") != None:
                        print(f"Valg-status-final not none in {i} {k}")
                        tmp_link_list = tmp_soup.findAll("a",class_="valg-status-final")
                        for j in tmp_link_list:
                            tmp_links = find_links(j,tmp_list)
                    else:
                        print(f"Valg-status-final none in {i} {k}")
                        if tmp_soup.find("a") != None:
                            print(f"a not none in {i} {k}")
                            tmp_link_list = tmp_soup.findAll("a")
                            for j in tmp_link_list:
                                tmp_links = find_links(j,tmp_list)
                        else:
                            print("None found thus far")
                long_list.extend(tmp_list)
                #print(long_list)
                with open(f"tmp_data/{i}/{k}/tmp.txt","a") as f:
                    for link in checked_list:
                        f.write(link + "\n")
                while long_list != []:
                    if counter % 100 == 0 or counter == 0:
                        checked_list = create_link_list(f"tmp_data/{i}/{k}/tmp.txt", checked_list)
                    current_site = long_list.pop(0)
                    tmp_count = 0
                    unchecked = []
                    for link in long_list:
                        if link not in checked_list:
                            unchecked.append(link)
                            tmp_count += 1
                        else:
                            pass
                    if tmp_count == 0:
                        break
                    long_list = unchecked
                    if current_site in checked_list:
                        print(f"Already checked {current_site}, moving on. {counter}")
                        continue
                    else:
                        checked_list.append(current_site)
                    counter += 1
                    tmp_list = []
                    tmp_count = 0
                    #print(f"https://kmdvalg.dk/{i}/{k}/{current_site}")
                    print(f"{current_site:>12}\tUnchecked: {len(long_list):5.0f}\t Checked: {len(checked_list):5.0f}\t{counter}")
                    tmp_data = try_link(f"https://kmdvalg.dk/{i}/{k}/{current_site}")
                    #print(str(tmp_data.status_code))
                    tmp_soup = Soup(tmp_data.content,"lxml")
                    if tmp_soup.find("area") != None:
                        # print(f"Area not none in {i} {k}")
                        tmp_link_list = tmp_soup.findAll("area")
                        for j in tmp_link_list:
                            tmp_links = find_links(j,tmp_list)
                    else:
                        # print(f"Area none in {i} {k}")
                        if tmp_soup.find("a",class_="valg-status-final") != None:
                            #print(f"Valg-status-final not none in {i} {k}")
                            tmp_link_list = tmp_soup.findAll("a",class_="valg-status-final")
                            for j in tmp_link_list:
                                tmp_links = find_links(j,tmp_list)
                        else:
                            #print(f"Valg-status-final none in {i} {k}")
                            if tmp_soup.find("a") != None:
                                #print(f"a not none in {i} {k}")
                                tmp_link_list = tmp_soup.findAll("a")
                                for j in tmp_link_list:
                                    tmp_links = find_links(j,tmp_list)
                            else:
                                pass
                                #print("None found thus far")
                    for link in tmp_list:
                        if link not in checked_list:
                            long_list.append(link)
                    # long_list.extend(tmp_list)
                    if counter % 100 == 0:
                        with open(f"tmp_data/{i}/{k}/unchecked_tmp.txt","w") as f:
                            for link in long_list:
                                f.write(link + "\n")
                        with open(f"tmp_data/{i}/{k}/tmp.txt","w") as f:
                            for link in checked_list:
                                f.write(link + "\n")
                with open(f"tmp_data/{i}/{k}/unchecked_tmp.txt", "w") as f:
                        f.write("")
                with open(f"tmp_data/{i}/{k}/tmp.txt", "w") as f:
                    for link in checked_list:
                        f.write(link + "\n")
    except TimeoutError:
        run_prog()

run_prog()