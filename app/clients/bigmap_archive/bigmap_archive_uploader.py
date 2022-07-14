from lib2to3.pgen2 import token
from xxlimited import Str
import json
import os
import logging

try:
    #from db.schemas_pydantic import Measurement
    from bigmap_archive.upload_data_archive import *
    from bigmap_archive.config_bigmap_archive import config 
    from bigmap_archive.config_bigmap_archive import config 
except:
    from db.schemas_pydantic import Measurement
    from clients.bigmap_archive.upload_data_archive import *
    from clients.bigmap_archive.config_bigmap_archive import config 
    from clients.bigmap_archive.config_bigmap_archive import config 

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

# Class responsible for uploading data onto the BigMap archive 

class archive_uploader:

    def __init__(self):
        self.token = config['access_token']
        self.url = config['web_archive_url']

    def upload_files_to_archive(self, 
        links_filename = 'records_links.json',
        records_path_links = '/Users/paolovincenzofreieslebendeblasio/finale/app',
        filenames = ['scientific_data.json'],
        data_path = '/Users/paolovincenzofreieslebendeblasio/finale/app/bigmap_archive/records/0'):

        '''
            Uploads records onto the bigmap archive, and stores the 
            different links used for uploading the data onto the archive. 
        '''
        
         #Url for the bigmap archive  #Access token for a user on the archive 
        
        prepare_output_file(records_path_links, links_filename) 

        try:
            # Upload a record including metadata onto the archive
            record_links = upload_record(self.url, 
                data_path, 
                filenames, 
                self.token)

            # Save the links for uploading the data in a json file
            save_to_file(records_path_links, links_filename, record_links)
        except Exception as e:
            print("An error occurred when uploading the data: ", str(e))
            
    def append_files_to_archive(self, 
        record_links : str, 
        records : list, 
        records_path : str):
        '''
            Append a new experiment onto an existing entry in the bigmap archive
        '''
        with open(record_links, "r") as f:
            links = json.load(f)[0]
        #try:
        
        for (file_index, record) in enumerate(records):

            (file_content_url, file_commit_url) = start_data_file_upload(record,
                file_index,
                links,
                self.token)
            
            upload_data_file_content(records_path, 
                record,
                file_content_url, 
                self.token)

            complete_data_file_upload(record, 
                file_commit_url, 
                self.token)
        #except Exception as e:
        #    print("Data could not be uploaded to the archive, error: ", str(e))
        #    return 
        print("Data uploaded succesfully to the archive") 
    
    def add_raw_data_to_archive(self,
        measurement: Measurement,
        measurement_id : str = None,
        metadata : dict() = None,
        records_path_links = '/code',
        temp_data_path='/code', 
        name_experiment : str = None):
        '''
            Uploads a raw Measurement (pydantic schema Measurement) onto the web 
            archive. Data is saved onto a temporary path, and then 
            uploaded onto the archive
        '''
        if name_experiment is None:
            name_experiment = measurement_id

        links_filename = measurement_id + '.json'
        prepare_output_file(records_path_links, links_filename) 

        try:
            os.mkdir(temp_data_path)
        except Exception as e:
            if FileExistsError:
                pass
            else:
                print('There is an exception: ', e)
                return "An error occurred creating a temporary storage for files, make sure only uploading from an account once"
        
        data_temp_filename = name_experiment + '.json'
        with open(os.path.join(temp_data_path, data_temp_filename), 'w') as f:
            data = measurement.json()
            json.dump(data, f)
        # Save filesaving links into a json with the measurement id as a name 
        try:
            # Upload a record including metadata onto the archive
            record_links = upload_record(self.url, 
                temp_data_path, 
                [data_temp_filename], 
                self.token,
                record_metadata=metadata)
            
            # Save the links for uploading the data in a json file
            publish_record(record_links, token=self.token) #Published the record inside the archive
            save_to_file(records_path_links, links_filename, record_links)
        except Exception as e:
            print("An error occurred when uploading the data: ", str(e))
        #os.rmdir(temp_data_path) 

    def append_raw_data_to_archive(self,
        record_links : str, 
        records : list, 
        records_path : str):
        return 
    def get_data_from_archive(self):
        return 


