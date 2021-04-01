"""Provides the functions to fetch data on the current members of
the Danish Parliament using the Open Data of the Parliament.
There may thus be minor inaccuracies in the output, due to
delays in updating on the part of the parliament's Open Data
service.

It provides output as a number of folders, named by the party
short name (eg. "S" for the Social Democrats), containing a number
of .tex files with the output and the images necessary for the
output files. To get pdf output, run XeLaTeX on each of the files.
Also provided in the output is a list of members output in .txt
sorted alphabetically by party and name

A note of caution: As this fetches directly from the Danish Parliament's
Open Data database, the material is in Danish and translation functionality
has not yet been implemented."""


def remove_special_characters(string):
    import re
    # Takes an input string with 0 or more html codes for special characters
    # and replaces them with the special characters in the output string
    tmp_string = string
    sub_list = ["ø", "æ", " ", "å", "Å", "Ø", "Æ", "«", "»", " ", r"\&"]
    search_list = ["&oslash;", "&aelig;", "&nbsp;", "&aring;",
                   "&Aring;", "&Oslash;", "&Aelig;", "&laquo;",
                   "&raquo;", "&nbsp;", "&amp;"]
    for word in range(len(search_list)):
        while re.search(search_list[word], tmp_string) is not None:
            tmp_string = re.sub(search_list[word], sub_list[word], tmp_string)
        while re.search("\d_",tmp_string) is not None:
            tmp_string = re.sub("_","\_",tmp_string)
    return tmp_string


def write_constituencies(inlist, data):
    # Write the parliamentary career and current constituency of the given
    # member of parliament
    tmp_list = []
    outlist = list(inlist)
    tmp_list.append(str(r"\subsection*{Folketinget}" + "\n"))
    tmp_list = write_section_to_outfile(tmp_list, "Folketingets Præsidium", data, 2, ["career", "presidiums"])
    if data.find("career").find("constituencies") is not None:
        tmp_list.append(str(r"\subsubsection*{Medlemsperioder}" + "\n"))
        data = data.find("career").find("constituencies").children
        tmp_list.append(str(r"\begin{itemize}" + "\n"))
        tmp_list.append(str(r"\item " + data.find("career").find("currentconstituency").text + "\n"))
        for i in data:
            tmp_list.append(str(r"\item " + i.text + "\n"))
        tmp_list.append(str(r"\end{itemize}" + "\n"))
    else:
        tmp_list.append(str(r"\subsubsection*{Medlemsperioder}" + "\n"))
        tmp_list.append(str(r"\begin{itemize}" + "\n"))
        tmp_list.append(str(r"\item " + data.find("career").find("currentconstituency").text + "\n"))
        tmp_list.append(str(r"\end{itemize}" + "\n"))
    tmp_list = write_section_to_outfile(tmp_list, "Kandidaturer", data, 2, ["career", "nominations"])
    outlist.extend(tmp_list)
    return outlist


def write_section_to_outfile(inlist, title, data, search_level, searches, output="itemize", section_type="subsection*"):
    # Writes a section to the LaTeX outfile
    # after checking for the existence of the
    # relevant data in the given XML data.
    # Takes as input a filename (file, str),
    # the title of the subsection (title, str),
    # the data being searched (data,var),
    # the number of find operations necessary (search_level,int),
    # the searches to be performed (searches,list) and
    # the format of the output (output, standard is "itemize".
    # Options are "itemize", "paragraph" and "enumerate").
    tmp_var = True
    tmp_list = []
    outlist = list(inlist)
    # Check for the existence of the relevant data iteratively
    # through the levels of searches specified
    tmp_data = data
    for i in range(search_level):
        # Check for the existence of the given level of search data
        # Simultaneously, if data is present, assign the search
        # result to a variable for later processing
        if tmp_data.find("{}".format(searches[i])) is not None:
            tmp_var = True
            tmp_data = tmp_data.find("{}".format(searches[i]))
        else:
            tmp_var = False
            break
    # If the data is present, continue, else break and end the function
    if tmp_var is True:
        tmp_list.append(str("\{}".format(section_type) + "{" + title + r"}" + "\n"))
        tmp_data = tmp_data.children
        if output == "itemize":
            tmp_list.append(str(r"\begin{itemize}" + "\n"))
            for item in tmp_data:
                item = remove_special_characters(item.text)
                tmp_list.append(str(r"\item " + item + "\n"))
            tmp_list.append(str(r"\end{itemize}" + "\n"))
        elif output == "enumerate":
            tmp_list.append(str(r"\begin{enumerate}" + "\n"))
            for item in tmp_data:
                item = remove_special_characters(item.text)
                tmp_list.append(str(r"\item " + item + "\n"))
            tmp_list.append(str(r"\end{enumerate}" + "\n"))
        elif output == "paragraph":
            for item in tmp_data:
                item = remove_special_characters(item.text)
                tmp_list.append(str(item + "\n\n"))
        outlist.extend(tmp_list)
        return outlist
    else:
        return outlist


def write_background_to_outfile(outlist, data):
    # Writes a section to the LaTeX outfile containing the background of the MP in question
    # Takes as input a filename (file, str) and the data being searched (data,var)
    if data.find("personalinformation").find("memberdata").find("p") is not None:
        tmp_string = remove_special_characters(data.find("personalinformation").find("memberdata").find("p").text)
        outlist.extend([str(r"\lettersection{Baggrund}" + "\n"), str(tmp_string + "\n")])
        return outlist
    elif data.find("personalinformation").find("memberdata") is not None:
        tmp_string = remove_special_characters(data.find("personalinformation").find("memberdata").text)
        outlist.extend([str(r"\lettersection{Baggrund}" + "\n"), str(tmp_string + "\n")])
        return outlist
    else:
        return outlist


def write_tex_head(data):
    # Writes the head of the LaTeX file
    # with import of necessary packages and
    # the necessary preamble
    # Takes as input the outfile name and
    # the data being searched through
    pre_text = ["""%!TEX TS-program = xelatex \n%!TEX encoding = UTF-8 Unicode\n""",
                r"\documentclass[11pt, a4paper]{awesome-cv}",
                r"\geometry{left=1.4cm, top=.8cm, right=1.4cm, bottom=1.8cm, footskip=.5cm}", r"\fontdir[fonts/]",
                str(r"\colorlet{awesome}{" + "{}-colour".format(data.find("partyshortname").text) + "}"),
                r"\setbool{acvSectionColorHighlight}{true}", r"\renewcommand{\acvHeaderSocialSep}{\quad\textbar\quad}",
                r"\recipient{}{}", str(r"\name{" + str(data.find("firstname").text) + r"}{" +
                                       str(data.find("lastname").text) + "}\n")]
    # print("Finished Pre-text")
    # # print(pre_text)
    if data.find("ministerphone") is not None:
        pre_text.append(str(r"\mobile{" + str(data.find("ministerphone").text) + "}\n"))
    elif data.find("phonefolketinget") is not None:
        pre_text.append(str(r"\mobile{" + str(data.find("phonefolketinget").text) + "}\n"))
    elif data.find("mobilephone") is not None:
        pre_text.append(str(r"\mobile{" + str(data.find("mobilephone").text) + "}\n"))
    else:
        pass
    # print("Finished Phone")
    if data.find("twitterprofiles") is not None:
        tmp_string = remove_special_characters(str(data.find("twitterprofiles").
                                                   find("twitterurl").
                                                   find("desciption").text))
        pre_text.append(str(r"\twitter{" + tmp_string + "}\n"))
    else:
        pass
    # print("Finished Twitter")
    if data.find("email") is not None:
        tmp_string = remove_special_characters(str(data.find("emails").find("email").text))
        pre_text.append(str(r"\email{" + tmp_string + "}\n"))
    else:
        pass
    # print("Finished Email")
    pre_text.extend(
        [str(r"\position{Medlem af Folketingent{\enskip\cdotp\enskip}" + str(data.find("party").text) + "}\n"),
         str(r"\address{}" + "\n"),
         str(r'\photo[circle,noedge,left]{"./' + data.find("firstname").text + "_" + data.find(
             "lastname").text + "_profile.jpg" + '"}\n'),
         str(r"\letterdate{\today}" + "\n"),
         str(r"\lettertitle{" + "{} {} - Blå Bog".format(
             data.find("firstname").text, data.find("lastname").text) + r"}"),
         str(r"\letteropening{}" + "\n"),
         str(r"\letterclosing{}" + "\n"),
         str(r"\letterenclosure[Attached]{Stemme Statistik}" + "\n"),
         str(r"\begin{document}" + "\n"),
         str(r"\makecvheader[R]" + "\n"),
         str(r"\makecvfooter{\today}{" + r"\lettertitle{" + "{} {} - Blå Bog".format(
             data.find("firstname").text, data.find("lastname").text) + r"}" + "}{}\n"),
         str(r"\makelettertitle" + "\n"),
         str(r"\begin{cvletter}" + "\n")])
    # # print(pre_text)
    return pre_text


def create_folders_and_files(data):
    import time
    import os
    import re
    if not os.path.isdir("./party_{}".format(data.find("partyshortname").text)):
        os.mkdir("./party_{}".format(data.find("partyshortname").text))
        os.system("cp -r cv ./party_{}/".format(data.find("partyshortname").text))
        os.system("cp -r fonts ./party_{}/".format(data.find("partyshortname").text))
        os.system("cp awesome-cv.cls ./party_{}/".format(data.find("partyshortname").text))
    # print("Creating {} {}".format(data.find("firstname").text, data.find("lastname").text))
    picture_url = re.sub("^.+?ft.dk:443", "https://www.ft.dk",
                         str(data.find("picturemires").text))
    picture_name = data.find("firstname").text + "_" + data.find(
        "lastname").text + "_profile.jpg"
    os.system("wget --output-document='./party_{}/{}' {}".format(data.find("partyshortname").text, picture_name,
                                                                 picture_url))
    outlist = write_tex_head(data)
    # print("Finished with tex_head")
    # # print(outlist)
    outlist = write_background_to_outfile(outlist, data)
    # print("Finished with background")
    outlist = write_section_to_outfile(outlist, "Uddannelse", data, 1, ["educations"], section_type="lettersection")
    # print("Finished with Uddannelse")
    outlist.append(str(r"\lettersection{Parlamentarisk Karriere}" + "\n"))
    outlist = write_section_to_outfile(outlist, "Ministerposter", data, 2, ["careers", "ministers"])
    # print("Finished with Ministerposter")
    outlist = write_section_to_outfile(outlist, "Ordførerskaber", data, 1, ["spokesmen"])
    # print("Finished with Ordførerskaber")
    outlist = write_section_to_outfile(outlist, "Parlamentariske Tillidsposter", data, 2,
                                       ["career", "parliamentarypositionsoftrust"])
    # print("Finished with Parlamentariske Tillidsposter")
    outlist = write_constituencies(outlist, data)
    # print("Finished with Constituencies")
    outlist = write_section_to_outfile(outlist, "Erhvervserfaring", data, 1, ["occupations"],
                                       section_type="lettersection")
    # print("Finished with Erhvervserfaring")
    outlist = write_section_to_outfile(outlist, "Publikationer", data, 1, ["publications"],
                                       section_type="lettersection")
    # print("Finished with Publikationer")
    outlist.append(str(r"\end{cvletter}" + "\n"))
    outlist.append(str(r"\end{document}"))
    # ¤# print(outlist)
    return outlist


def run_writing_loop(data, memberlist, count):
    import re
    from bs4 import BeautifulSoup as Soup

    for i in range(len(data)):
        try:
            xml_data = Soup(data[i]["biografi"], "lxml").find("body").find("member")
            if re.search(r"^.+?\d{1,2}\.\s\w+?\s\d{4}", str(xml_data.find("currentconstituency").text)) is not None:
                memberlist.append("({}) {} {}".format(xml_data.find("partyshortname").text,
                                                      xml_data.find("firstname").text,
                                                      xml_data.find("lastname").text))
                print_list = create_folders_and_files(xml_data)
                count += 1
                with open("./party_{}/{}_{}.tex".format(xml_data.find("partyshortname").text,
                                                        xml_data.find("firstname").text,
                                                        xml_data.find("lastname").text), "w") as f:
                    for line in print_list:
                        f.write(line)
        except AttributeError:
            pass
        except TypeError:
            pass
    return memberlist, count


def main_function():
    import requests
    import json
    url = "https://oda.ft.dk/api/Akt%C3%B8r?$inlinecount=allpages&$filter=typeid%20eq%205"
    data = json.loads(requests.get(url).content)
    list_of_members = []
    counter = 0
    while True:
        try:
            url = data["odata.nextLink"]
            data_json = data["value"]
            list_of_members, counter = run_writing_loop(data_json, list_of_members, counter)
            data = requests.get(url)
            data = json.loads(data.content)
        except KeyError:
            data_json = data["value"]
            list_of_members, counter = run_writing_loop(data_json, list_of_members, counter)
            break
    with open("Current_members.txt", "w") as f:
        for i in list_of_members:
            f.write(i)
    return


main_function()
