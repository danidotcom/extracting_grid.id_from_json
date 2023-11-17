import json
import time

#---------------- Liste der Universitäten aus der .txt-datei-------------------

"""
The data was scarpt from: "https://www.timeshighereducation.com/world-university-rankings/2023/subject-ranking/engineering-and-it#!/length/100/sort_by/rank/sort_order/asc/cols/stats"
"""
uniliste = open("Unis.txt", "r", encoding="latin-1")
List_of_Universities = uniliste.read()

# wir teilen die Liste auf, sodass wir direkt eine Liste von strings mit den Universitätsnamen haben
List_of_Universities = List_of_Universities.split("\n")
List_of_Universities.pop()

# List of missing universities (we wanna remove those, where we find the grid.id)
List_of_missing_universities = List_of_Universities[:]

# datacleaning
for index in range(len(List_of_Universities)):
    """ 
    In case that the data is scapt again or gets lost we generate trotzdem the correct grid.ids
    The name of "Virginia Polytechnic Institute and State University"         is in hte json file "Virginia Tech" (look at aliases)
    The name of "University of Illinois at Urbana-Champaign"                  is in the json file "Illinois Space Grant Consortium"
    The name of "Paris Sciences et Lettres  PSL Research University Paris"    is in the json file "PSL Research University"
    The "KTH Royal Institute of Technology" is in the json file "Royal Institute of Technology", so just without the "KTH" in the beginnig
    Some fo the universities are with "The" at the beginning
    """
    List_of_Universities[index] = List_of_Universities[index].replace("Paris Sciences et Lettres  PSL Research University Paris","PSL Research University")
    List_of_Universities[index] = List_of_Universities[index].replace("Virginia Polytechnic Institute and State University","Virginia Tech")
    List_of_Universities[index] = List_of_Universities[index].replace("Penn State (Main campus)","Pennsylvania State University")
    List_of_Universities[index] = List_of_Universities[index].replace(", Singapore","")
    List_of_Universities[index] = List_of_Universities[index].replace(" (KAIST)","")
    List_of_Universities[index] = List_of_Universities[index].replace("(Seoul campus)","")
    List_of_Universities[index] = List_of_Universities[index].replace(" (POSTECH)","")
    List_of_Universities[index] = List_of_Universities[index].replace(" (SKKU)","")
    # List_of_Universities[index] = List_of_Universities[index].replace(" (Main campus)","")
    List_of_Universities[index] = List_of_Universities[index].replace("(NTU)","")
    List_of_Universities[index] = List_of_Universities[index].replace("KTH","")
    List_of_Universities[index] = List_of_Universities[index].replace("The","")
    List_of_Universities[index] = List_of_Universities[index].replace(" at ","").replace(" ", "").replace("-", "").replace(",","").replace(".","").replace("'", "")

# this gives the grid.id :
#
# grid_id = data[0]["external_ids"]["GRID"]["preferred"])

# -------------------------Durchsuchung der grid.id`s---------------------------

ror_file = open("rororg.json", encoding="latin-1")

data = json.load(ror_file)

start_time = time.time()

# The counter is to be sure, that all university is in the json file
# if counter is not equal to the length of the List of Universities, then we miss some
counter = 0

# this will be the list of the grid.ids with the name of the university
List_of_gridids = dict()

# to safe as txt (so we append to dictionary and export as txt)
for date in data:
    datename = date["name"].replace("The","").replace(" at ","").replace(" ", "").replace("\u2013", "").replace(",","").replace(".","").replace("(", "").replace(")","").replace("'", "").replace("\u00e9", "").replace("\u00c9", "").replace("-", "")

    for uni in List_of_Universities:

        if (uni.lower() in datename.lower() or datename.lower() in uni.lower()) and (len(datename) == len(uni)):
            List_of_gridids.update({List_of_missing_universities[List_of_Universities.index(uni)] : date["external_ids"]["GRID"]["preferred"]})
            List_of_missing_universities.remove(str(List_of_missing_universities[List_of_Universities.index(uni)]))
            List_of_Universities.remove(uni)
            counter += 1

        elif uni.lower() == ("the" + datename.lower()):
            List_of_gridids.update({List_of_missing_universities[List_of_Universities.index(uni)] : date["external_ids"]["GRID"]["preferred"]})
            List_of_missing_universities.remove(str(List_of_missing_universities[List_of_Universities.index(uni)]))
            List_of_Universities.remove(uni)
            counter += 1

# # this is just to look which names are included in the other, but not the "same"
# #
        # elif unim.lower() in datename.lower():
        #     print("txt in json : " + datename + " : " + str(len(datename)) + " --> " + unim + " : " + str(len(unim))) # quasi exception

        # elif datename.lower() in unim.lower(): 
        #     print("json in txt : " + datename + " : " + str(len(datename)) + " --> " + unim + " : " + str(len(unim))) # quasi exception
        
# TODO exception raisen bei doppelungen !
# TODO grid.ids mit den namen vergleichen ! (nochmal andersherum die namen zu den grid.ids mit der liste von den top 100 uni geben lassen)
# TODO als json exportieren (json.dump())

# --------------- try to export as json ----------------------

# # this is to json file (not finished)
# for date in data:
#     datename = date["name"].replace(" ", "")

#     for uni in List_of_Universities:
#         unim = uni.replace(" ", "") 

#         if unim.lower() in datename.lower() or datename.lower() in unim.lower():
#             List_of_gridids["name"].append(uni)
#             List_of_gridids.update({"name": uni, "grid.id" : date["external_ids"]["GRID"]["preferred"]})

#             if uni in List_of_missing_universities:
#                 List_of_missing_universities.remove(uni)
#                 counter += 1

# ----------------- testinstances or something -------------------------

print("\n")

print("List of missing universities : ", List_of_missing_universities, "\n")

print("List of universities : ", List_of_Universities, "\n")

# print("List of grid.ids : " List_of_gridids, "\n")

# print("Length of grid.ids-list : ", len(List_of_gridids), "\n")

print("counter : ", counter, "\n")

# print("we got every university : ", counter == len(List_of_Universities), "\n")

stop_time = time.time()

print("Zeit : ", stop_time-start_time, "\n")

# ----------------------- export grid.id`s ---------------

grid_id_file = open("grid_ids.txt", "w+")

#print(List_of_gridids.items())

for name in List_of_gridids:
    grid_id_file.write(name + " : " + List_of_gridids[name] + "\n")

# ----------------------- close files --------------------

ror_file.close()
uniliste.close()
grid_id_file.close()

# python3 -m pdb filename.py --> Syntax googlen 