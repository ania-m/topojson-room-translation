import json
import os
from pytopojson import topology
from geojson import dump

#This script converts geojson files to topojson files

#####FUNCTION DEFINED HERE #############
#returns specified property from geojson file
def geo_to_topo (json_files,output_path): 
    for json_file in json_files:        
        with open(json_file) as f:
            feature_collection=json.load(f)        

        try:
            os.mkdir(output_path)
        except FileExistsError:
            pass
        
        topology_ = topology.Topology()
        topojson = topology_({"object_name": feature_collection})
        topo_name = json_file.split(".")[0].replace("geo-","topo-")
        with open(output_path+'\\{}.json'.format(topo_name), 'w') as f:
            dump(topojson, f)
    return


#########SCRIPT STARTS HERE #################
if __name__ == "__main__":
    file_path = input("Enter path for geojson file(s) and press ENTER:    ")
    os.chdir(file_path)

    geojson_files = list(filter(lambda f: f.lower().endswith(".geojson"), os.listdir(file_path)))
    geo_to_topo(geojson_files,file_path+"\\topo")

       