# import re
# tmp_list = []
#
# with open("test2.txt", "r") as f:
#     next_line = f.readline()
#     while next_line != "":
#         #print(next_line)
#         next_line = re.sub("\A<(.+?)>.+",r"\1",next_line)
#         #print(next_line)
#         if next_line not in tmp_list:
#             tmp_list.append(next_line)
#         next_line = f.readline()
#         print(tmp_list)
# with open("output.txt","w") as f:
#     for i in tmp_list:
#         f.write(i)
    
