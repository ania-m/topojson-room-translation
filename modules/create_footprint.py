import json
import os
from shapely import MultiPoint, Polygon,unary_union
from geojson import Feature, FeatureCollection, dump

#This script  creates a footprint geojson of all rooms of all goejson in folder

#####FUNCTION DEFINED HERE #############
#returns specified property from geojson file
def create_footprint(json_files):
    feature_collection = [] #feature collection for footprint
    polygons_list = [] #list of all polygons from all geojsons
    
    for file in json_files:
        with open(file) as f:
            loaded_json=json.load(f)
            for feature in loaded_json["features"]:
                polygons_list.append(Polygon([tuple(coord) for coord in feature["geometry"]["coordinates"][0]]))
                
    #generate footprint polygon from all polygons
    footprint_polygon = unary_union(polygons_list)
    
    #append polygon to feature collection of geojson
    feature_collection.append(Feature(geometry=footprint_polygon, 
                properties={"Number":"FOOTPRINT"}                
                ))
    
    feature_collection_all = FeatureCollection(feature_collection)    
    return feature_collection_all 


#########SCRIPT STARTS HERE #################
if __name__ == "__main__":
    file_path = input("Enter path for geojson file(s) and press ENTER:    ")
    file_name = input("Enter file name for created footprint geojson and press ENTER:    ")
    print(file_name)
    os.chdir(file_path)
    
    geojson_files = list(filter(lambda f: f.lower().endswith(".geojson"), os.listdir(file_path)))
    
    with open('FOOTPRINT.geojson', 'w') as f:
        dump(create_footprint(geojson_files), f)
    

       