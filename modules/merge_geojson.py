import json
import os

#This script joins geojson file with one feature colleciton in a folder into one main file

#####FUNCTION DEFINED HERE #############
#returns specified property from geojson file
def merge_geojsons(json_files):
    #Open first geojson in list - this will act as base
    with open(json_files[0]) as f:
        first_file=json.load(f)

    #Go through the rest of the geojsons, skipping the first geojson
    for i in range(1,len(json_files)-1):
        with open(json_files[i]) as f:
            current_file=json.load(f)

        #append contents to geojson to first file
        for e in range(len(current_file["features"])):
            first_file["features"].append(current_file["features"][e])

        #return modified first file contents as geojson - to be saved as geojson
        return first_file


#########SCRIPT STARTS HERE #################
if __name__ == "__main__":
    file_path = input("Enter path for geojson file(s) and press ENTER:    ")
    os.chdir(file_path)

    geojson_files = list(filter(lambda f: f.lower().endswith(".geojson"), os.listdir(file_path)))

    with open("merged_geojson.geojson", "w") as outfile:
        json.dump(merge_geojsons(geojson_files), outfile)
       