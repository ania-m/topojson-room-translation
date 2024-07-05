#This script compares two sets of polygons and returns translation based on overlapping of polygons
#Note: The first file will consist of the keys for the excel table 
#The sensitivity of the overlaps can be adjusted with the perc_treshold attribute, the lower the treshold the more sensitive the comparison will be to overlaps

#Possible outputs dicitonary or data frame

import pandas as pd
from shapely.geometry import Polygon

def room_translation(dict1,dict2,perc_treshold=15, col1_name="column1", col2_name="column2",data_frame = True,dup_deliminator="~",blank_ovr="",filtered_rooms=["OPEN TO BELOW","Precinct Non-Interior CB","UP","DN"],check_rooms=[]):
    #create dictionary based on overlapping polygons
    room_translation = {}
    for room1, coords1 in dict1.items():
        #if footprint room, don't do translation, just park it as footprint
        if "FOOTPRINT" in room1:
            room_translation.setdefault(room1,["FOOTPRINT"])
            continue
        pol_1 = Polygon(coords1) #create polygon for room
        room1_f = room1[:room1.index(dup_deliminator)]

        if pol_1.is_valid != True:
            # input("!!!!!!!!CHECK ONCE SCRIPT IS DONE *"+room1_f+"* press ENTER to continue")
            check_rooms.append(room1_f)
            clean = pol_1.buffer(0)
            pol_1 = clean
                    
        print(room1_f)
        room_translation[room1_f] = []
        for room2, coords2 in dict2.items():
            room2_f = room2[:room2.index(dup_deliminator)]
            #filter out rooms that contain specified words
            if room2_f in filtered_rooms:
                continue

            try:
                pol_2 = Polygon(coords2) #create polygon for room  
                
                #if the overlap is larger than the specified percentage of smallest room compared to overlap
                pol_area_list = [pol_1.area,pol_2.area]
                pol_area_list.sort()
                if (pol_1.intersection(pol_2).area / pol_area_list[0]) * 100 >= perc_treshold:
                     room_translation[room1_f].append(room2_f)
                                         
            except:
                room_translation[room1_f].append("ERROR")            

        #if no match found, return none instead of an empty array
        if room_translation[room1_f] == []:
            room_translation[room1_f] = None
    
    #Convert dictionary to data frame the size of 2 columns
    if data_frame:  #if data frame option is specified 
        output = {item: " | ".join(map(str, room_translation[item])) if room_translation[item] is not None else blank_ovr for item in room_translation}
        output_df = (pd.DataFrame.from_dict(output, orient='index', columns=['DDRooms']))
        output_df = output_df.reset_index().rename(columns={"index":"ConstructionRooms"})	
        return output_df
    return room_translation #if no data frame option is specified