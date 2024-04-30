"""wrapper for functions for geographical analysis"""
import geopandas
import pgeocode
import numpy as np
import json

from ..Enviroment_Variables import enviroment as env

from .DataService import dataService 
 
# tell pgeocode that PLZ are in Germany
distance = pgeocode.GeoDistance(env.PGEOCODE_COUNTRY_CODE)

# finds the distance between two PLZ in km
def find_distance(plz1, plz2):
    
    # raises error if PLZ is not string
    if not isinstance(plz1, str) or not isinstance(plz2, str):
        raise ValueError("postal codes must be represented as as string")
    
 
    
    
    return distance.query_postal_code(plz1,plz2)

# returns pgeocode information about PLZ
def find_info(plz1):
    # raises error if plz is not string
    if not isinstance(plz1, str):
        raise ValueError("postal codes must be represented as as string")
    
    # tell pgeocode that PLZ is in Germany
    info = pgeocode.Nominatim(env.PGEOCODE_COUNTRY_CODE)
    
    return info.query_postal_code(plz1)

# gets coordinates of PLZ
def get_coordinates(plz):
    if not isinstance(plz, str):
        raise ValueError("postal codes must be represented as as string")
    
    info = pgeocode.Nominatim(env.PGEOCODE_COUNTRY_CODE)
    
    DF = info.query_postal_code(plz)
    
    return[DF.loc["latitude"],DF.loc["longitude"]]

# reads shape file in enviroment.py, filters it to given PLZ and returns it as geoJSON string
def make_shape_file():
    print("Map Generation Started...")
    print("Retrieving Postal Codes...")
    PLZ = dataService.get_all_PLZ()    

    shape_frame = geopandas.read_file(env.POSTAL_CODE_AREAS,dtype = {'plz':str})
    
    shape_frame = shape_frame.merge(PLZ, how = 'inner',left_on = 'plz', right_on = env.META_POSTAL)
    shape_frame.insert(0, "selected", np.full(len(shape_frame[env.META_POSTAL]), False))
    
    print("Postal Codes Filtered...")
    
    SampleNums = []
    Coordinates = []
    
    for i in shape_frame[env.META_POSTAL]:
        SampleNums.append(len(dataService.get_all_in_plz(i).index))
        Coordinates.append(get_coordinates(i))

    shape_frame.insert(0, "total_samples", SampleNums)
    shape_frame.insert(0, "Coordinates", Coordinates)
    
    print("Sample Data Collected...")
    print("Map Generation Complete\n\n")
    return json.loads(shape_frame.to_json())
    
def getPLZListController():
        
        print("Starting Retrieval of Map Data...")
        PLZDF=dataService.get_all_PLZ_DataTable()
        locationNameData = []
        dataPointsData = []
    
        print("Filtering for Postal Codes...")
        for i in PLZDF['postal_code']:    
            dataPointsData.append(len(dataService.get_all_in_plz(i).index))
            locationNameData.append(find_info(i).place_name)
        
        print("Inserting Data...")
        PLZDF.insert(0,"number_of_samples",dataPointsData)
        PLZDF.insert(0,"place_name",locationNameData)
        print("done\n\n")
        return PLZDF.to_json(orient="records")

shape_frame_global = make_shape_file()
plz_list_global = getPLZListController()