import json
import pandas as pd
import os
from modules.geojson_props import get_geojson_property, handle_duplicates, update_geojson, coords_to_tuples
from modules.data_frame_to_excel import data_frame_to_excel
from modules.room_translation import room_translation

###############################
######  USER INPUTS      ######

file1_path = input("Enter the location of the FIRST set of geojson(s) THIS WILL BE USED AS THE PRIMARY KEY !:    ")
#file1_name = input("name of the FIRST geojson (no extension):   ")

file2_path = input("Enter the location of the SECOND set of geojson(s):")
#file2_name = input("name of the SECOND geojson (no extension):  ")

output_path =input("Location to save excel: ")
output_name =input("Name of output file (no extension): ")

output_df = pd.DataFrame({"ConstructionRooms":[],"DDRooms":[]})

check_rooms = []
no_match_geo = []

#######################################
######  LOOP THROUGH EACH FILE   ######
#for each geojson, create room translation with corresponding geojson of the same name in other folder
for file_n in filter(lambda f: f.lower().endswith(".geojson"), os.listdir(file1_path)):
    with open('{}\\{}'.format(file1_path,file_n)) as f:
        data_1=json.load(f)

    #skip to next file if no matching geojson is located in both folder
    if os.path.exists('{}\\{}'.format(file2_path,file_n)):
        with open('{}\\{}'.format(file2_path,file_n))  as f:
            data_2=json.load(f)
    else:
        no_match_geo.append(file_n)
        pass
    
    data_array = [data_1,data_2] #to easily apply same manipulation up on both data sets
    geometry_dict_array = [[],[]] #array with results from manipulation
    for data in data_array:
        #to handle duplicates in room nummbers a suffix will be added to each room number (and later remmoved), this will create an array with new rooms
        rm_count_array = list(handle_duplicates(get_geojson_property(data))["values"])
        
        #update geojson data with suffixed keys. It is important that the property array and the geojson elements are in the same order in their respective arrays
        data = update_geojson(data,rm_count_array)
        
        #Reformat geojson to tuples dictionaries
        geometry_dict_array[data_array.index(data)]=(coords_to_tuples(data))

    #Compare the geometries and translate them based on overlap
    output = room_translation(geometry_dict_array[0],geometry_dict_array[1],blank_ovr="NEW DESIGN",check_rooms=check_rooms)
    output_df = pd.concat([output_df,output])


#create a seperate dataframe where each row is split into various rows if translation gave more than one output
col1_name=list(output_df.columns)[0]
col2_name=list(output_df.columns)[1]
split_output_rows = []

for index, row in output_df.iterrows():
    col1 = row[0]
    col2 = row[1].split(' | ')
    for element in col2:
        split_output_rows.append({col1_name:col1,col2_name:element})
split_output_df = pd.DataFrame(split_output_rows)

#Create excel based on dataframe
os.chdir(output_path)
data_frame_to_excel(output_df.sort_values(by=col1_name),excel_name='{}.xlsx'.format(output_name),sheet_name="Room_Translation",table_name = "RmTranslation")
data_frame_to_excel(split_output_df.sort_values(by=col1_name),excel_name='{}_SPLIT.xlsx'.format(output_name),sheet_name="Room_Translation",table_name = "RmTranslation")

print("\nDATA FRAME:")
print(output_df)

if len(check_rooms) > 0:
    print("\n","!"*40)
    print("CHECK ROOMS:")
    [print("  ",room) for room in check_rooms]

if len(no_match_geo) > 0:
    print("\n","!"*40)
    print("NO MATCHING GEOJSON FOR:")
    [print("  ",file) for file in no_match_geo] 
    print("\n")
