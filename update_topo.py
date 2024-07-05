import pandas as pd
import json
import os

#This script updates the topojson files of a folder based on an excel file
#The excel file requires a column containing unique values as keys (default 1st column)
#The excel file requires a column containing the parameter being updated (default 2nd column)
#Returns topojson

#####FUNCTION HERE ###########

def update_topojson_from_excel(topo_file,excel_file,key="Number",parameter='DDRmNum',key_col = 1, par_col = 2):
    # Read Excel file
    df_excel = pd.read_excel(excel_file)
    
    #Create a dictionary from the Excel file for easy lookup
    # Key from first column of excel, value is parameter column identified
    excel_dict = dict(zip(df_excel.iloc[:, key_col-1], df_excel.iloc[:, par_col-1]))

    #Open topojson
    with open(topo_file) as f:
        shapes_data=json.load(f)

    #Get shapes from topojson
    shapes_array = shapes_data["objects"]["object_name"]["geometries"]

    #Go through each shape, update property based on key found in excel
    for shape in shapes_array:
        try:
            shape['properties'][parameter] = excel_dict[shape['properties'][key]]
        except:
            input("could not find room for "+shape['properties'][key]+" press ENTER to continue")
        print(shape['properties'][key])

    return shapes_data

#######SCRIPT STARTS HERE ############
if __name__ == "__main__":
    topo_path = input("Enter path to topojson folder:    ")
    topo_path_new = input("Enter path to UPDATED topojson folder:    ")
    excel_path =input("Location of excel:   ")

    excel_file_path = '{}\\ALL-LEVELS.xlsx'.format(excel_path)

    os.chdir(topo_path)
    for file in os.listdir(topo_path):
        with open("{}\\{}".format(topo_path_new,file), "w") as outfile:
            json.dump(update_topojson_from_excel(file, excel_file_path), outfile)
        
