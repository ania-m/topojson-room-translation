import json
import os
from create_footprint import create_footprint

#This script appends a "FOOTPRINT" of all rooms of each geojson, to each of the geojsons

#####FUNCTION DEFINED HERE #############
def add_footprint_polygon(json_files):
    footprint_feature_collection = create_footprint(json_files)
    
    for json_file in json_files:        
        with open(json_file) as f:
            file=json.load(f)


        #append footprint at begining of geojson
        footprint = [footprint_feature_collection["features"][0]]
        rooms = file["features"]
        print(rooms)
            
        file["features"] = footprint + rooms

        #return modified first file contents as geojson - to be saved as geojson
        with open(json_file, 'w') as f:
            json.dump(file, f)
    return


#########SCRIPT STARTS HERE #################
if __name__ == "__main__":
    file_path = input("Enter path for geojson file(s) and press ENTER:    ")
    os.chdir(file_path)

    geojson_files = list(filter(lambda f: f.lower().endswith(".geojson"), os.listdir(file_path)))
    add_footprint_polygon(geojson_files)

       