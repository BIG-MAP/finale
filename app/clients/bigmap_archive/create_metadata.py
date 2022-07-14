from curses import meta
import json 
import os , sys

try:
    from schemas_pydantic import Measurement
    from bigmap_archive.config_bigmap_archive import config 
except:
    try:
        from db.schemas_pydantic import Measurement
        from clients.bigmap_archive.config_bigmap_archive import config 
    except:
        pass

from datetime import datetime

def createMetadataJson(
    record_restrictions = "public",
    file_restrictions = "public",
    publication_date = None):

    '''
    Creates a metadata dictionary based on the config file
    
    The metadata dictionary is compatible with the bigmap 
    archive 
    '''

    metadata = dict()
    #assert record_restrictions == "public" or record_restrictions == "private"
    #assert file_restrictions == "public" or file_restrictions == "private"
    metadata["access"] = {"record": record_restrictions,
                        "files": file_restrictions}
    metadata["files"] = {"enabled": "true"}

    if publication_date == None:
        publication_date = datetime.today().strftime('%Y-%m-%d') 
        #Set the publication date to today 
    
    metadata["metadata"] = {"creators": config["metadata"]["creators"],
    "publication_date" : publication_date,
    "resource_type" : config["metadata"]["resource_type"],
    "title" : 'FINALE - ' + config["metadata"]["title"],
    "version" : config["metadata"]["version"]
    }
    return metadata
    #Loop over the creators of an experiment 

def create_metadata_from_measurement(measurement_request:  Measurement):
    '''
        Function which takes as input a measurement request, and turns it into 
        a metadata in a .json format 
    '''
    metadata = {}
    temp = measurement_request.temperature
    print(temp)
    for chemical in measurement_request.formulation.chemicals:
        print(chemical, '-----')
    
