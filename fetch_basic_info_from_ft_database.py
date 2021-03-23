import requests
from bs4 import BeautifulSoup as soup
import json
import re
import os
import time
url = "https://oda.ft.dk/api/Akt%C3%B8r?$inlinecount=allpages&$filter=typeid%20eq%205"
data = requests.get(url)
data = json.loads(data.content)
counter = 0
pre_text = [r"\documentclass[11pt, a5paper]{awesome-cv}",r"\geometry{left=1.4cm, top=.8cm, right=1.4cm, bottom=1.8cm, footskip=.5cm}",r"\fontdir[../fonts/]",r"\colorlet{awesome}{awesome-red}",r"\setbool{acvSectionColorHighlight}{true}",r"\renewcommand{\acvHeaderSocialSep}{\quad\textbar\quad}",r"\recipient{}{}" ]

while True:
    try:
        url = data["odata.nextLink"]
        data_json = data["value"]
        for i in range(len(data_json)):
            try:
                xml_data = soup(data_json[i]["biografi"],"lxml").find("body").find("member")
                if xml_data.find("currentconstituency") != None:
                    if re.search(r"^.+?\d{1,2}\.\s\w+?\s\d{4}", str(xml_data.find("currentconstituency").text)) != None:
                        print("{} {}".format(xml_data.find("firstname").text, xml_data.find("lastname").text))
                        print(xml_data.find("currentconstituency").text)
                        pre_text = [r"\documentclass[11pt, a5paper]{awesome-cv}",
                                    r"\geometry{left=1.4cm, top=.8cm, right=1.4cm, bottom=1.8cm, footskip=.5cm}",
                                    r"\fontdir[fonts/]", str(r"\colorlet{awesome}{" + "{}-colour".format(xml_data.find("partyshortname").text) + "}"),
                                    r"\setbool{acvSectionColorHighlight}{true}",
                                    r"\renewcommand{\acvHeaderSocialSep}{\quad\textbar\quad}", r"\recipient{}{}"]
                        counter += 1
                        print(xml_data.find("party").text)
                        if os.path.isdir("./party_{}".format(xml_data.find("partyshortname").text)):
                            picture_url = re.sub("^.+?ft.dk:443", "https://www.ft.dk",
                                                 str(xml_data.find("picturemires").text))
                            picture_name = xml_data.find("firstname").text + "_" + xml_data.find(
                                "lastname").text + "_profile.jpg"
                            print(picture_name)
                            os.system(
                                "wget --output-document='./party_{}/{}' {}".format(xml_data.find("partyshortname").text,
                                                                                   picture_name, picture_url))
                            time.sleep(3)
                            with open("./party_{}/{}_{}.tex".format(xml_data.find("partyshortname").text, xml_data.find("firstname").text, xml_data.find("lastname").text), "w") as f:
                                f.write("""%!TEX TS-program = xelatex \n%!TEX encoding = UTF-8 Unicode\n""")
                                #f.write("{} {}\n".format(xml_data.find("firstname").text, xml_data.find("lastname").text))
                                for i in pre_text:
                                    f.write(str(i)+"\n")
                                tmp_string = r"\name{" + str(xml_data.find("firstname").text) + r"}{" + str(
                                    xml_data.find("lastname").text) + "}\n"
                                f.write(tmp_string)
                                if xml_data.find("ministerphone") != None:
                                    tmp_string = r"\mobile{" + str(xml_data.find("ministerphone").text) + "}\n"
                                    f.write(tmp_string)
                                elif xml_data.find("phonefolketinget") != None:
                                    tmp_string = r"\mobile{" + str(xml_data.find("phonefolketinget").text) + "}\n"
                                    f.write(tmp_string)
                                elif xml_data.find("mobilephone") != None:
                                    tmp_string = r"\mobile{" + str(xml_data.find("mobilephone").text) + "}\n"
                                    f.write(tmp_string)
                                else:
                                    pass
                                if xml_data.find("twitterprofiles") != None:
                                    tmp_data = xml_data.find("twitterprofiles")
                                    tmp_data = tmp_data.find("twitterurl")
                                    tmp_data = tmp_data.find("desciption")
                                    tmp_string = r"\twitter{" + str(tmp_data.text) + "}\n"
                                    #print(tmp_data)
                                    f.write(tmp_string)
                                else:
                                    print("No Twitter data")
                                if xml_data.find("emails") != None:
                                    tmp_string = r"\email{" + str(xml_data.find("emails").find("email").text) + "}\n"
                                    f.write(tmp_string)
                                else:
                                    pass
                                tmp_string = r"\position{Medlem af Folketingent{\enskip\cdotp\enskip}" + str(xml_data.find("party").text) + "}\n"
                                f.write(tmp_string)
                                f.write(r"\address{}"+"\n")
                                tmp_string = r'\photo[circle,noedge,left]{"./' + picture_name + '"}\n'
                                f.write(tmp_string)
                                f.write(r"\letterdate{\today}")
                                tmp_string = r"\lettertitle{" + "{} {} - Blå Bog".format(
                                    xml_data.find("firstname").text, xml_data.find("lastname").text) + r"}"
                                f.write(tmp_string + "\n")
                                f.write("\letteropening{}\n")
                                f.write("\letterclosing{}\n")
                                f.write("\letterenclosure[Attached]{Stemme Statistik}\n")
                                f.write(r"\begin{document}" + "\n")
                                f.write(r"\makecvheader[R]"+"\n")
                                f.write(r"\makecvfooter{\today}{"+tmp_string+"}{}\n")
                                f.write(r"\makelettertitle"+"\n")
                                f.write(r"\begin{cvletter}"+"\n")

                                if xml_data.find("personalinformation").find("memberdata").find("p") != None:
                                    tmp_string = xml_data.find("personalinformation").find("memberdata").find("p").text
                                    print(tmp_string)
                                    sub_list = ["ø", "æ", " ", "å", "Å", "Ø", "Æ"]
                                    search_list = ["&oslash;", "&aelig;", "&nbsp;", "&aring;", "&Aring;", "&Oslash;",
                                                   "&Aelig;"]
                                    for i in range(len(search_list)):
                                        while re.search(search_list[i], tmp_string) != None:
                                            tmp_string = re.sub(search_list[i], sub_list[i], tmp_string)
                                    f.write(r"\lettersection{Baggrund}" + "\n")
                                    f.write(tmp_string + "\n")
                                elif xml_data.find("personalinformation").find("memberdata") != None:
                                    tmp_string = xml_data.find("personalinformation").find("memberdata").text
                                    print(tmp_string)
                                    sub_list = ["ø", "æ", " ", "å", "Å", "Ø", "Æ"]
                                    search_list = ["&oslash;", "&aelig;", "&nbsp;", "&aring;", "&Aring;", "&Oslash;",
                                                   "&Aelig;"]
                                    for i in range(len(search_list)):
                                        while re.search(search_list[i], tmp_string) != None:
                                            tmp_string = re.sub(search_list[i], sub_list[i], tmp_string)
                                    f.write(r"\lettersection{Baggrund}" + "\n")
                                    f.write(tmp_string + "\n")
                                if xml_data.find("educations") != None:
                                    f.write(r"\lettersection{Uddannelse}" + "\n")
                                    tmp_data = xml_data.find("educations").findAll("education")
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                f.write(r"\lettersection{Parlamentarisk Karriere}" + "\n")
                                if xml_data.find("career").find("ministers") != None:
                                    f.write(r"\subsection*{Ministerposter}" + "\n")
                                    tmp_data = xml_data.find("career").find("ministers").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("spokesmen") != None:
                                    f.write(r"\subsection*{Ordførerskaber}" + "\n")
                                    tmp_data = xml_data.find("spokesmen").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("career").find("parliamentarypositionsoftrust") != None:
                                    f.write(r"\subsection*{Parlamentariske Tillidsposter}" + "\n")
                                    tmp_data = xml_data.find("career").find("parliamentarypositionsoftrust").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("career").find("constituencies") != None:
                                    f.write(r"\subsection*{Folketinget}" + "\n")
                                    if xml_data.find("career").find("presidiums") != None:
                                        f.write(r"\subsubsection*{Folketingets Præsidium}" + "\n")
                                        tmp_data = xml_data.find("career").find("presidiums").children
                                        f.write(r"\begin{itemize}" + "\n")
                                        for i in tmp_data:
                                            f.write(r"\item " + i.text + "\n")
                                        f.write(r"\end{itemize}" + "\n")
                                    f.write(r"\subsubsection*{Medlemsperioder}" + "\n")
                                    tmp_data = xml_data.find("career").find("constituencies").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    f.write(r"\item " + xml_data.find("career").find("currentconstituency").text + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                    f.write(r"\subsubsection*{Kandidaturer}" + "\n")
                                    tmp_data = xml_data.find("career").find("nominations").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                else:
                                    f.write(r"\subsection*{Folketinget}" + "\n")
                                    if xml_data.find("career").find("presidiums") != None:
                                        f.write(r"\subsubsection*{Folketingets Præsidium}" + "\n")
                                        tmp_data = xml_data.find("career").find("presidiums").children
                                        f.write(r"\begin{itemize}" + "\n")
                                        for i in tmp_data:
                                            f.write(r"\item " + i.text + "\n")
                                        f.write(r"\end{itemize}" + "\n")
                                    f.write(r"\subsubsection*{Medlemsperioder}" + "\n")
                                    f.write(r"\begin{itemize}" + "\n")
                                    f.write(r"\item " + xml_data.find("career").find("currentconstituency").text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                    f.write(r"\subsubsection*{Kandidaturer}" + "\n")
                                    tmp_data = xml_data.find("career").find("nominations").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("occupations") != None:
                                    f.write(r"\lettersection{Erhvervserfaring}" + "\n")
                                    tmp_data = xml_data.find("occupations").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("publications") != None:
                                    f.write(r"\lettersection{Publikationer}" + "\n")
                                    tmp_data = xml_data.find("publications").children
                                    for i in tmp_data:
                                        f.write(i.text + "\n")
                                f.write(r"\end{cvletter}" + "\n")
                                f.write(r"\end{document}")
                        else:
                            os.mkdir("./party_{}".format(xml_data.find("partyshortname").text))
                            os.system("cp -r cv ./party_{}/".format(xml_data.find("partyshortname").text))
                            os.system("cp -r fonts ./party_{}/".format(xml_data.find("partyshortname").text))
                            os.system("cp awesome-cv.cls ./party_{}/".format(xml_data.find("partyshortname").text))
                            # os.system("cp cv ./party_{}/".format(xml_data.find("partyshortname").text))
                            picture_url = re.sub("^.+?ft.dk:443", "https://www.ft.dk",
                                                 str(xml_data.find("picturemires").text))
                            picture_name = xml_data.find("firstname").text + "_" + xml_data.find(
                                "lastname").text + "_profile.jpg"
                            print(picture_name)

                            os.system(
                                "wget --output-document='./party_{}/{}' {}".format(xml_data.find("partyshortname").text,
                                                                                   picture_name, picture_url))
                            time.sleep(3)
                            with open("./party_{}/{}_{}.tex".format(xml_data.find("partyshortname").text, xml_data.find("firstname").text, xml_data.find("lastname").text), "w") as f:
                                f.write("""%!TEX TS-program = xelatex \n%!TEX encoding = UTF-8 Unicode\n""")
                                #f.write("{} {}\n".format(xml_data.find("firstname").text, xml_data.find("lastname").text))
                                for i in pre_text:
                                    f.write(str(i)+"\n")
                                tmp_string = r"\name{" + str(xml_data.find("firstname").text) + r"}{" + str(
                                    xml_data.find("lastname").text) + "}\n"
                                f.write(tmp_string)
                                if xml_data.find("ministerphone") != None:
                                    tmp_string = r"\mobile{" + str(xml_data.find("ministerphone").text) + "}\n"
                                    f.write(tmp_string)
                                elif xml_data.find("phonefolketinget") != None:
                                    tmp_string = r"\mobile{" + str(xml_data.find("phonefolketinget").text) + "}\n"
                                    f.write(tmp_string)
                                elif xml_data.find("mobilephone") != None:
                                    tmp_string = r"\mobile{" + str(xml_data.find("mobilephone").text) + "}\n"
                                    f.write(tmp_string)
                                else:
                                    pass
                                if xml_data.find("twitterprofiles") != None:
                                    tmp_data = xml_data.find("twitterprofiles")
                                    tmp_data = tmp_data.find("twitterurl")
                                    tmp_data = tmp_data.find("desciption")
                                    tmp_string = r"\twitter{" + str(tmp_data.text) + "}\n"
                                    # print(tmp_data)
                                    f.write(tmp_string)
                                else:
                                    print("No Twitter data")
                                if xml_data.find("emails") != None:
                                    tmp_string = r"\email{" + str(xml_data.find("emails").find("email").text) + "}\n"
                                    f.write(tmp_string)
                                else:
                                    pass
                                tmp_string = r"\position{Medlem af Folketingent{\enskip\cdotp\enskip}" + str(
                                    xml_data.find("party").text) + "}\n"
                                f.write(tmp_string)
                                f.write(r"\address{}" + "\n")
                                tmp_string = r'\photo[circle,noedge,left]{"./' + picture_name + '"}\n'
                                f.write(tmp_string)
                                f.write(r"\letterdate{\today}")
                                tmp_string = r"\lettertitle{" + "{} {} - Blå Bog".format(
                                    xml_data.find("firstname").text, xml_data.find("lastname").text) + r"}"
                                f.write(tmp_string + "\n")
                                f.write("\letteropening{}\n")
                                f.write("\letterclosing{}\n")
                                f.write("\letterenclosure[Attached]{Stemme Statistik}\n")
                                f.write(r"\begin{document}" + "\n")
                                f.write(r"\makecvheader[R]" + "\n")
                                f.write(r"\makecvfooter{\today}{" + tmp_string + "}{}\n")
                                f.write(r"\makelettertitle" + "\n")
                                f.write(r"\begin{cvletter}" + "\n")

                                if xml_data.find("personalinformation").find("memberdata").find("p") != None:
                                    tmp_string = xml_data.find("personalinformation").find("memberdata").find("p").text
                                    print(tmp_string)
                                    sub_list = ["ø", "æ", " ", "å", "Å", "Ø", "Æ"]
                                    search_list = ["&oslash;", "&aelig;", "&nbsp;", "&aring;", "&Aring;", "&Oslash;",
                                                   "&Aelig;"]
                                    for i in range(len(search_list)):
                                        while re.search(search_list[i], tmp_string) != None:
                                            tmp_string = re.sub(search_list[i], sub_list[i], tmp_string)
                                    f.write(r"\lettersection{Baggrund}" + "\n")
                                    f.write(tmp_string + "\n")
                                elif xml_data.find("personalinformation").find("memberdata") != None:
                                    tmp_string = xml_data.find("personalinformation").find("memberdata").text
                                    print(tmp_string)
                                    sub_list = ["ø", "æ", " ", "å", "Å", "Ø", "Æ"]
                                    search_list = ["&oslash;", "&aelig;", "&nbsp;", "&aring;", "&Aring;", "&Oslash;",
                                                   "&Aelig;"]
                                    for i in range(len(search_list)):
                                        while re.search(search_list[i], tmp_string) != None:
                                            tmp_string = re.sub(search_list[i], sub_list[i], tmp_string)
                                    f.write(r"\lettersection{Baggrund}" + "\n")
                                    f.write(tmp_string + "\n")
                                # sub_list = ["ø", "æ", " ", "å", "Å", "Ø", "Æ"]
                                # search_list = ["&oslash;", "&aelig;", "&nbsp;", "&aring;", "&Aring;", "&Oslash;",
                                #                "&Aelig;"]
                                # for i in range(len(search_list)):
                                #     while re.search(search_list[i], tmp_string) != None:
                                #         tmp_string = re.sub(search_list[i], sub_list[i], tmp_string)
                                # f.write(r"\lettersection{Baggrund}" + "\n")
                                # f.write(tmp_string + "\n")
                                if xml_data.find("educations") != None:
                                    f.write(r"\lettersection{Uddannelse}" + "\n")
                                    tmp_data = xml_data.find("educations").findAll("education")
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                f.write(r"\lettersection{Parlamentarisk Karriere}" + "\n")
                                if xml_data.find("career").find("ministers") != None:
                                    f.write(r"\subsection*{Ministerposter}" + "\n")
                                    tmp_data = xml_data.find("career").find("ministers").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("spokesmen") != None:
                                    f.write(r"\subsection*{Ordførerskaber}" + "\n")
                                    tmp_data = xml_data.find("spokesmen").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("career").find("parliamentarypositionsoftrust") != None:
                                    f.write(r"\subsection*{Parlamentariske Tillidsposter}" + "\n")
                                    tmp_data = xml_data.find("career").find("parliamentarypositionsoftrust").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("career").find("constituencies") != None:
                                    f.write(r"\subsection*{Folketinget}" + "\n")
                                    if xml_data.find("career").find("presidiums") != None:
                                        f.write(r"\subsubsection*{Folketingets Præsidium}" + "\n")
                                        tmp_data = xml_data.find("career").find("presidiums").children
                                        f.write(r"\begin{itemize}" + "\n")
                                        for i in tmp_data:
                                            f.write(r"\item " + i.text + "\n")
                                        f.write(r"\end{itemize}" + "\n")
                                    f.write(r"\subsubsection*{Medlemsperioder}" + "\n")
                                    tmp_data = xml_data.find("career").find("constituencies").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    f.write(r"\item " + xml_data.find("career").find("currentconstituency").text + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                    f.write(r"\subsubsection*{Kandidaturer}" + "\n")
                                    tmp_data = xml_data.find("career").find("nominations").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                else:
                                    f.write(r"\subsection*{Folketinget}" + "\n")
                                    if xml_data.find("career").find("presidiums") != None:
                                        f.write(r"\subsubsection*{Folketingets Præsidium}" + "\n")
                                        tmp_data = xml_data.find("career").find("presidiums").children
                                        f.write(r"\begin{itemize}" + "\n")
                                        for i in tmp_data:
                                            f.write(r"\item " + i.text + "\n")
                                        f.write(r"\end{itemize}" + "\n")
                                    f.write(r"\subsubsection*{Medlemsperioder}" + "\n")
                                    f.write(r"\begin{itemize}" + "\n")
                                    f.write(r"\item " + xml_data.find("career").find("currentconstituency").text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                    f.write(r"\subsubsection*{Kandidaturer}" + "\n")
                                    tmp_data = xml_data.find("career").find("nominations").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("occupations") != None:
                                    f.write(r"\lettersection{Erhvervserfaring}" + "\n")
                                    tmp_data = xml_data.find("occupations").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("publications") != None:
                                    f.write(r"\lettersection{Publikationer}" + "\n")
                                    tmp_data = xml_data.find("publications").children
                                    for i in tmp_data:
                                        f.write(i.text + "\n")
                                f.write(r"\end{cvletter}" + "\n")
                                f.write(r"\end{document}")

            except AttributeError:
                pass
                #print("AttributeError")
            except TypeError:
                pass
                #print("TypeError")

        data = requests.get(url)
        data = json.loads(data.content)
    except KeyError:
        data_json = data["value"]

        for i in range(len(data_json)):
            try:
                xml_data = soup(data_json[i]["biografi"], "lxml").find("body").find("member")
                if xml_data.find("currentconstituency") != None:
                    if re.search(r"^.+?\d{1,2}\.\s\w+?\s\d{4}",str(xml_data.find("currentconstituency").text)) != None:

                        pre_text = [r"\documentclass[11pt, a5paper]{awesome-cv}",
                                    r"\geometry{left=1.4cm, top=.8cm, right=1.4cm, bottom=1.8cm, footskip=.5cm}",
                                    r"\fontdir[fonts/]", str(r"\colorlet{awesome}{" + "{}-colour".format(
                                xml_data.find("partyshortname").text) + "}"),
                                    r"\setbool{acvSectionColorHighlight}{true}",
                                    r"\renewcommand{\acvHeaderSocialSep}{\quad\textbar\quad}", r"\recipient{}{}"]
                        print("{} {}".format(xml_data.find("firstname").text, xml_data.find("lastname").text))
                        print(xml_data.find("currentconstituency").text)
                        counter += 1
                        print(xml_data.find("party").text)
                        if os.path.isdir("./party_{}".format(xml_data.find("partyshortname").text)):
                            picture_url = re.sub("^.+?ft.dk:443", "https://www.ft.dk",
                                                 str(xml_data.find("picturemires").text))
                            picture_name = xml_data.find("firstname").text + "_" + xml_data.find("lastname").text + "_profile.jpg"
                            print(picture_name)

                            os.system("wget --output-document='./party_{}/{}' {}".format(xml_data.find("partyshortname").text,picture_name, picture_url))
                            time.sleep(3)
                            with open("./party_{}/{}_{}.tex".format(xml_data.find("partyshortname").text, xml_data.find("firstname").text, xml_data.find("lastname").text), "w") as f:
                                f.write("""%!TEX TS-program = xelatex \n%!TEX encoding = UTF-8 Unicode\n""")
                                #f.write("{} {}\n".format(xml_data.find("firstname").text, xml_data.find("lastname").text))
                                for i in pre_text:
                                    f.write(str(i)+"\n")
                                tmp_string = r"\name{" + str(xml_data.find("firstname").text) + r"}{" + str(xml_data.find("lastname").text) + "}\n"
                                f.write(tmp_string)
                                if xml_data.find("ministerphone") != None:
                                    tmp_string = r"\mobile{" + str(xml_data.find("ministerphone").text) + "}\n"
                                    f.write(tmp_string)
                                elif xml_data.find("phonefolketinget") != None:
                                    tmp_string = r"\mobile{" + str(xml_data.find("phonefolketinget").text) + "}\n"
                                    f.write(tmp_string)
                                elif xml_data.find("mobilephone") != None:
                                    tmp_string = r"\mobile{" + str(xml_data.find("mobilephone").text) + "}\n"
                                    f.write(tmp_string)
                                else:
                                    pass
                                if xml_data.find("twitterprofiles") != None:
                                    tmp_data = xml_data.find("twitterprofiles")
                                    tmp_data = tmp_data.find("twitterurl")
                                    tmp_data = tmp_data.find("desciption")
                                    tmp_string = r"\twitter{" + str(tmp_data.text) + "}\n"
                                    # print(tmp_data)
                                    f.write(tmp_string)
                                else:
                                    print("No Twitter data")
                                if xml_data.find("emails") != None:
                                    tmp_string = r"\email{" + str(xml_data.find("emails").find("email").text) + "}\n"
                                    f.write(tmp_string)
                                else:
                                    pass
                                tmp_string = r"\position{Medlem af Folketingent{\enskip\cdotp\enskip}" + str(
                                    xml_data.find("party").text) + "}\n"
                                f.write(tmp_string)
                                f.write(r"\address{}" + "\n")
                                tmp_string = r'\photo[circle,noedge,left]{"./' + picture_name + '"}\n'
                                f.write(tmp_string)
                                f.write(r"\letterdate{\today}")
                                tmp_string = r"\lettertitle{" + "{} {} - Blå Bog".format(
                                    xml_data.find("firstname").text, xml_data.find("lastname").text) + r"}"
                                f.write(tmp_string + "\n")
                                f.write("\letteropening{}\n")
                                f.write("\letterclosing{}\n")
                                f.write("\letterenclosure[Attached]{Stemme Statistik}\n")
                                f.write(r"\begin{document}" + "\n")
                                f.write(r"\makecvheader[R]" + "\n")
                                f.write(r"\makecvfooter{\today}{" + tmp_string + "}{}\n")
                                f.write(r"\makelettertitle" + "\n")
                                f.write(r"\begin{cvletter}" + "\n")

                                if xml_data.find("personalinformation").find("memberdata").find("p") != None:
                                    tmp_string = xml_data.find("personalinformation").find("memberdata").find("p").text
                                    print(tmp_string)
                                    sub_list = ["ø", "æ", " ", "å", "Å", "Ø", "Æ"]
                                    search_list = ["&oslash;", "&aelig;", "&nbsp;", "&aring;", "&Aring;", "&Oslash;",
                                                   "&Aelig;"]
                                    for i in range(len(search_list)):
                                        while re.search(search_list[i], tmp_string) != None:
                                            tmp_string = re.sub(search_list[i], sub_list[i], tmp_string)
                                    f.write(r"\lettersection{Baggrund}" + "\n")
                                    f.write(tmp_string + "\n")
                                elif xml_data.find("personalinformation").find("memberdata") != None:
                                    tmp_string = xml_data.find("personalinformation").find("memberdata").text
                                    print(tmp_string)
                                    sub_list = ["ø", "æ", " ", "å", "Å", "Ø", "Æ"]
                                    search_list = ["&oslash;", "&aelig;", "&nbsp;", "&aring;", "&Aring;", "&Oslash;",
                                                   "&Aelig;"]
                                    for i in range(len(search_list)):
                                        while re.search(search_list[i], tmp_string) != None:
                                            tmp_string = re.sub(search_list[i], sub_list[i], tmp_string)
                                    f.write(r"\lettersection{Baggrund}" + "\n")
                                    f.write(tmp_string + "\n")
                                if xml_data.find("educations") != None:
                                    f.write(r"\lettersection{Uddannelse}" + "\n")
                                    tmp_data = xml_data.find("educations").findAll("education")
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                f.write(r"\lettersection{Parlamentarisk Karriere}" + "\n")
                                if xml_data.find("career").find("ministers") != None:
                                    f.write(r"\subsection*{Ministerposter}" + "\n")
                                    tmp_data = xml_data.find("career").find("ministers").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("spokesmen") != None:
                                    f.write(r"\subsection*{Ordførerskaber}" + "\n")
                                    tmp_data = xml_data.find("spokesmen").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("career").find("parliamentarypositionsoftrust") != None:
                                    f.write(r"\subsection*{Parlamentariske Tillidsposter}" + "\n")
                                    tmp_data = xml_data.find("career").find("parliamentarypositionsoftrust").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("career").find("constituencies") != None:
                                    f.write(r"\subsection*{Folketinget}" + "\n")
                                    if xml_data.find("career").find("presidiums") != None:
                                        f.write(r"\subsubsection*{Folketingets Præsidium}" + "\n")
                                        tmp_data = xml_data.find("career").find("presidiums").children
                                        f.write(r"\begin{itemize}" + "\n")
                                        for i in tmp_data:
                                            f.write(r"\item " + i.text + "\n")
                                        f.write(r"\end{itemize}" + "\n")
                                    f.write(r"\subsubsection*{Medlemsperioder}" + "\n")
                                    tmp_data = xml_data.find("career").find("constituencies").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    f.write(r"\item " + xml_data.find("career").find("currentconstituency").text + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                    f.write(r"\subsubsection*{Kandidaturer}" + "\n")
                                    tmp_data = xml_data.find("career").find("nominations").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                else:
                                    f.write(r"\subsection*{Folketinget}" + "\n")
                                    if xml_data.find("career").find("presidiums") != None:
                                        f.write(r"\subsubsection*{Folketingets Præsidium}" + "\n")
                                        tmp_data = xml_data.find("career").find("presidiums").children
                                        f.write(r"\begin{itemize}" + "\n")
                                        for i in tmp_data:
                                            f.write(r"\item " + i.text + "\n")
                                        f.write(r"\end{itemize}" + "\n")
                                    f.write(r"\subsubsection*{Medlemsperioder}" + "\n")
                                    f.write(r"\begin{itemize}" + "\n")
                                    f.write(r"\item " + xml_data.find("career").find("currentconstituency").text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                    f.write(r"\subsubsection*{Kandidaturer}" + "\n")
                                    tmp_data = xml_data.find("career").find("nominations").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("occupations") != None:
                                    f.write(r"\lettersection{Erhvervserfaring}" + "\n")
                                    tmp_data = xml_data.find("occupations").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("publications") != None:
                                    f.write(r"\lettersection{Publikationer}" + "\n")
                                    tmp_data = xml_data.find("publications").children
                                    for i in tmp_data:
                                        f.write(i.text + "\n")
                                f.write(r"\end{cvletter}" + "\n")
                                f.write(r"\end{document}")
                        else:
                            os.mkdir("./party_{}".format(xml_data.find("partyshortname").text))
                            os.system("cp -r cv ./party_{}/".format(xml_data.find("partyshortname").text))
                            os.system("cp -r fonts ./party_{}/".format(xml_data.find("partyshortname").text))
                            os.system("cp awesome-cv.cls ./party_{}/".format(xml_data.find("partyshortname").text))
                            os.system("cp fontawesome.sty ./party_{}/".format(xml_data.find("partyshortname").text))
                            #if "https://master-ft.ft.dk:443/" in str(xml_data.find("picturemires").text:
                            picture_url = re.sub("^.+?ft.dk:443", "https://www.ft.dk",
                                                 str(xml_data.find("picturemires").text))
                            picture_name = xml_data.find("firstname").text + "_" + xml_data.find(
                                "lastname").text + "_profile.jpg"
                            print(picture_name)

                            os.system(
                                "wget --output-document='./party_{}/{}' {}".format(xml_data.find("partyshortname").text,
                                                                                   picture_name, picture_url))

                            time.sleep(3)
                            with open("./party_{}/{}_{}.tex".format(xml_data.find("partyshortname").text, xml_data.find("firstname").text, xml_data.find("lastname").text), "w") as f:
                                f.write("""%!TEX TS-program = xelatex \n%!TEX encoding = UTF-8 Unicode\n""")
                                #f.write("{} {}\n".format(xml_data.find("firstname").text, xml_data.find("lastname").text))
                                #for i in xml_data.children:
                                #    f.write(str(i)+"\n")
                                for i in pre_text:
                                    f.write(str(i)+"\n")
                                tmp_string = r"\name{" + str(xml_data.find("firstname").text) + r"}{" + str(
                                    xml_data.find("lastname").text) + "}\n"
                                f.write(tmp_string)
                                if xml_data.find("ministerphone") != None:
                                    tmp_string = r"\mobile{" + str(xml_data.find("ministerphone").text) + "}\n"
                                    f.write(tmp_string)
                                elif xml_data.find("phonefolketinget") != None:
                                    tmp_string = r"\mobile{" + str(xml_data.find("phonefolketinget").text) + "}\n"
                                    f.write(tmp_string)
                                elif xml_data.find("mobilephone") != None:
                                    tmp_string = r"\mobile{" + str(xml_data.find("mobilephone").text) + "}\n"
                                    f.write(tmp_string)
                                else:
                                    pass
                                if xml_data.find("twitterprofiles") != None:
                                    tmp_data = xml_data.find("twitterprofiles")
                                    tmp_data = tmp_data.find("twitterurl")
                                    tmp_data = tmp_data.find("desciption")
                                    tmp_string = r"\twitter{" + str(tmp_data.text) + "}\n"
                                    # print(tmp_data)
                                    f.write(tmp_string)
                                else:
                                    print("No Twitter data")
                                if xml_data.find("emails") != None:
                                    tmp_string = r"\email{" + str(xml_data.find("emails").find("email").text) + "}\n"
                                    f.write(tmp_string)
                                else:
                                    pass
                                tmp_string = r"\position{Medlem af Folketingent{\enskip\cdotp\enskip}" + str(
                                    xml_data.find("party").text) + "}\n"
                                f.write(tmp_string)
                                f.write(r"\address{}" + "\n")
                                tmp_string = r'\photo[circle,noedge,left]{"./' + picture_name + '"}\n'
                                f.write(tmp_string)
                                f.write(r"\letterdate{\today}")
                                tmp_string = r"\lettertitle{" + "{} {} - Blå Bog".format(
                                    xml_data.find("firstname").text, xml_data.find("lastname").text) + r"}"
                                f.write(tmp_string + "\n")
                                f.write("\letteropening{}\n")
                                f.write("\letterclosing{}\n")
                                f.write("\letterenclosure[Attached]{Stemme Statistik}\n")
                                f.write(r"\begin{document}" + "\n")
                                f.write(r"\makecvheader[R]" + "\n")
                                f.write(r"\makecvfooter{\today}{" + tmp_string + "}{}\n")
                                f.write(r"\makelettertitle" + "\n")
                                f.write(r"\begin{cvletter}" + "\n")

                                if xml_data.find("personalinformation").find("memberdata").find("p") != None:
                                    tmp_string = xml_data.find("personalinformation").find("memberdata").find("p").text
                                    print(tmp_string)
                                    sub_list = ["ø", "æ", " ", "å", "Å", "Ø", "Æ"]
                                    search_list = ["&oslash;", "&aelig;", "&nbsp;", "&aring;", "&Aring;", "&Oslash;",
                                                   "&Aelig;"]
                                    for i in range(len(search_list)):
                                        while re.search(search_list[i], tmp_string) != None:
                                            tmp_string = re.sub(search_list[i], sub_list[i], tmp_string)
                                    f.write(r"\lettersection{Baggrund}" + "\n")
                                    f.write(tmp_string + "\n")
                                elif xml_data.find("personalinformation").find("memberdata") != None:
                                    tmp_string = xml_data.find("personalinformation").find("memberdata").text
                                    print(tmp_string)
                                    sub_list = ["ø", "æ", " ", "å", "Å", "Ø", "Æ"]
                                    search_list = ["&oslash;", "&aelig;", "&nbsp;", "&aring;", "&Aring;", "&Oslash;",
                                                   "&Aelig;"]
                                    for i in range(len(search_list)):
                                        while re.search(search_list[i], tmp_string) != None:
                                            tmp_string = re.sub(search_list[i], sub_list[i], tmp_string)
                                    f.write(r"\lettersection{Baggrund}" + "\n")
                                    f.write(tmp_string + "\n")
                                if xml_data.find("educations") != None:
                                    f.write(r"\lettersection{Uddannelse}" + "\n")
                                    tmp_data = xml_data.find("educations").findAll("education")
                                    f.write(r"\begin{itemize}"+"\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}"+"\n")
                                f.write(r"\lettersection{Parlamentarisk Karriere}" + "\n")
                                if xml_data.find("career").find("ministers") != None:
                                    f.write(r"\subsection*{Ministerposter}" + "\n")
                                    tmp_data = xml_data.find("career").find("ministers").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("spokesmen") != None:
                                    f.write(r"\subsection*{Ordførerskaber}"+"\n")
                                    tmp_data = xml_data.find("spokesmen").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("career").find("parliamentarypositionsoftrust") != None:
                                    f.write(r"\subsection*{Parlamentariske Tillidsposter}"+"\n")
                                    tmp_data = xml_data.find("career").find("parliamentarypositionsoftrust").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("career").find("constituencies") != None:
                                    f.write(r"\subsection*{Folketinget}" + "\n")
                                    if xml_data.find("career").find("presidiums") != None:
                                        f.write(r"\subsubsection*{Folketingets Præsidium}" + "\n")
                                        tmp_data = xml_data.find("career").find("presidiums").children
                                        f.write(r"\begin{itemize}" + "\n")
                                        for i in tmp_data:
                                            f.write(r"\item " + i.text + "\n")
                                        f.write(r"\end{itemize}" + "\n")
                                    f.write(r"\subsubsection*{Medlemsperioder}" + "\n")
                                    tmp_data = xml_data.find("career").find("constituencies").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    f.write(r"\item " + xml_data.find("career").find("currentconstituency").text + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                    f.write(r"\subsubsection*{Kandidaturer}" + "\n")
                                    tmp_data = xml_data.find("career").find("nominations").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                else:
                                    f.write(r"\subsection*{Folketinget}" + "\n")
                                    if xml_data.find("career").find("presidiums") != None:
                                        f.write(r"\subsubsection*{Folketingets Præsidium}" + "\n")
                                        tmp_data = xml_data.find("career").find("presidiums").children
                                        f.write(r"\begin{itemize}" + "\n")
                                        for i in tmp_data:
                                            f.write(r"\item " + i.text + "\n")
                                        f.write(r"\end{itemize}" + "\n")
                                    f.write(r"\subsubsection*{Medlemsperioder}" + "\n")
                                    f.write(r"\begin{itemize}" + "\n")
                                    f.write(r"\item " + xml_data.find("career").find("currentconstituency").text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                    f.write(r"\subsubsection*{Kandidaturer}" + "\n")
                                    tmp_data = xml_data.find("career").find("nominations").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("occupations") != None:
                                    f.write(r"\lettersection{Erhvervserfaring}"+"\n")
                                    tmp_data = xml_data.find("occupations").children
                                    f.write(r"\begin{itemize}" + "\n")
                                    for i in tmp_data:
                                        f.write(r"\item " + i.text + "\n")
                                    f.write(r"\end{itemize}" + "\n")
                                if xml_data.find("publications") != None:
                                    f.write(r"\lettersection{Publikationer}"+"\n")
                                    tmp_data = xml_data.find("publications").children
                                    for i in tmp_data:
                                        f.write(i.text + "\n")
                                f.write(r"\end{cvletter}"+"\n")
                                f.write(r"\end{document}")
            except AttributeError:
                pass
            except TypeError:
                pass

        break
print(counter)



