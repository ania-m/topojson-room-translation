import json
import os
import pandas as pd

#The script below  prints a list of specified property from shapes in geojson file

#Functions here can be used to to coordinate various lists
#Defaults to "Number" property 

#####FUNCTION DEFINED HERE #############
#returns specified property from geojson file
def get_geojson_property(json_data,property="Number"):
    return [feature["properties"][property] for feature in json_data["features"]]

#adds count to duplicates as suffix in array with a defined deliminator
def handle_duplicates(array_data,deliminator = "~!"):
    array_dict = {"values":array_data}
    array_df = pd.DataFrame(array_dict)
    s = array_df.groupby("values").cumcount().add(1).astype(str)
    array_df["values"] = array_df["values"] + (deliminator + s).where(array_df["values"] != "FOOTPRINT", "")
    return array_df

#updates geojson shape property - if property does not exist in shape, it will be added
def update_geojson(geo_data,prop_array,property="Number"):
    for i in range(len(geo_data["features"])):
        geo_data["features"][i]["properties"]["Number"]=prop_array[i]
    return geo_data

#Creates dictionary of {"ROOM1":[(x1,y1),(x2,y2),(x3,y3)],"ROOM2":[(x1,y1),(x2,y2),(x3,y3)]...etc} 
#Creates key from geojson files for each feature object
def coords_to_tuples(json_data):    
    #This makes it easier to use with the shapely geometry instead of converting arrays to tuples in code
    return {feature["properties"]["Number"]: [tuple(coord) for coord in feature["geometry"]["coordinates"][0]] for feature in json_data["features"]}

#########SCRIPT STARTS HERE #################
if __name__ == "__main__":
    file_path = input("Enter path for geojson file(s) and press ENTER:    ")
    os.chdir(file_path)

    for i in filter(lambda f: f.lower().endswith(".geojson"), os.listdir(file_path)):
        with open('{}\\{}'.format(file_path,i)) as f:
            data=json.load(f)

        # for room in handle_duplicates(get_geojson_property(data))["values"]:
        #     print(room)  

        number_array = list(handle_duplicates(get_geojson_property(data))["values"])
        update_geojson(data,number_array)


