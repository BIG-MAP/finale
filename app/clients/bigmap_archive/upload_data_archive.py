import json
import os
import logging
import requests

try:
    from bigmap_archive.config_bigmap_archive import config 
    from bigmap_archive.create_metadata import  createMetadataJson
except:
    from clients.bigmap_archive.config_bigmap_archive import config 
    from clients.bigmap_archive.create_metadata import  createMetadataJson

# Different functions for uploading data onto the BigMap archive 


def prepare_output_file(records_path, filename):
    file_path = os.path.join(records_path, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Create a file for storing records' links  
    with open(file_path, 'w') as f:
        json_formatted_text = json.dumps([])
        f.write(json_formatted_text)
    

def upload_record(url, record_path, records, token,record_metadata = None ):
    '''
    Uploads metadata onto the bigmap archive.  
    Also filecommit, and filestorage links are sent 
    '''
    # Get title, authors, and metadata from configuration file
    
    if record_metadata is None:
        record_metadata = createMetadataJson() #Creates metadata from the config file 
    print( 'THis is record metaddta', record_metadata, )
    # Create a record in the PostgreSQL database
    # Get the url for the record's attached files
    # e.g., 'https://dev1-big-map-archive.materialscloud.org/api/records/cpbc8-ss975/draft/files'
    links = create_record_in_database(url, record_metadata, token)

    data_file_index = 0
    for filename in records: # Upload all the experimental data
        upload_data_file(record_path, filename, data_file_index, links, token)
        data_file_index += 1

    return links


def create_record_in_database(url, record_metadata, token):
    '''
        Creates the first record in the archive by publishing the metadata
        of an experiment

        RETURNS: URLs for the records attached files 
    '''
    payload = record_metadata
    
    request_headers = {
        "Accept": "application/json",
        "Content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(
        f"{url}/api/records",
        data=payload,
        headers=request_headers,
        verify=True)
    # Raise an exception if the record could not be created
    if response.status_code != 201:
        raise ValueError(f"Failed to create record (code: {response.status_code})")

    #  Get urls for the record
    #  e.g., 'https://dev1-big-map-archive.materialscloud.org/api/records/h0zrf-17b65/draft/files'
    
    links = response.json()['links']
    return links


def upload_data_file(record_path, filename, file_index, links, token):
    '''
        Uploads the data from a specific file path into the archive
    '''
    (file_content_url, file_commit_url) = start_data_file_upload(filename, file_index, links, token)
    upload_data_file_content(record_path, filename, file_content_url, token)
    complete_data_file_upload(filename, file_commit_url, token)


def start_data_file_upload(filename, file_index, links, token):
    '''
        Uploads the file name onto the archive 
    '''
    files_url = links['files']
    
    payload = json.dumps([{"key": filename}])
    
    request_headers = {
        "Accept": "application/json",
        "Content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.post(
        files_url,
        data=payload,
        headers=request_headers,
        verify=True) #We simply post the filename to the archive 
        
    
    # Raise an exception if the file could not be created
    if response.status_code != 201:
        raise ValueError(f"Failed to create record (code: {response.status_code})")

    # Get the file content url and the file commit url
    # e.g., 'https://dev1-big-map-archive.materialscloud.org/api/records/eqcks-b1q35/draft/files/scientific_data.json/content'
    # e.g, 'https://dev1-big-map-archive.materialscloud.org/api/records/eqcks-b1q35/draft/files/scientific_data.json/commit'

    # Get the number of entries inside the 
    n_entries = len(response.json()['entries'])    
    file_links = response.json()['entries'][n_entries - 1]['links']
    file_content_url = file_links['content']
    file_commit_url = file_links['commit']
    print('------',file_content_url, file_commit_url, '------------')
    return (file_content_url, file_commit_url)


def upload_data_file_content(record_path, filename, file_content_url, token):
    # Upload the file content by streaming the data
    with open(os.path.join(record_path, filename), 'rb') as f:
        
        #We read the scientific data, here denoted as f
        request_headers = {
            "Accept": "application/json",
            "Content-type": "application/octet-stream",
            "Authorization": f"Bearer {token}"
        }
        
        #We then try to send the data to the server
        # The file_content_url is the url pointing to the place where we want to store
        # the data 

        # It seems the error is here, as we can easily create a reference inside the 
        # archive 
        response = requests.put(
            file_content_url,
            data=f,
            headers=request_headers,    
            verify=True)
        print(response.reason, 'This is reason for failure')
    # Raise an exception if the file content could not be uploaded
    if response.status_code != 200:
        raise ValueError(f"Failed to upload file content {filename} (code: {response.status_code})")

def complete_data_file_upload(filename, file_commit_url, token):
    #This commits the data into the server?
    request_headers = {
        "Accept": "application/json",
        "Content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(
        file_commit_url,
        headers=request_headers,
        verify=True)

    # Raise an exception if the file content could not be uploaded
    if response.status_code != 200:
        raise ValueError(f"Failed to complete file upload {filename} (code: {response.status_code})")


def publish_record(links, token):
    publish_url = links['publish']

    request_headers = {
        "Accept": "application/json",
        "Content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(
        publish_url,
        headers=request_headers,
        verify=True)

    # Raise an exception if the record could not be published
    if response.status_code != 202:
        raise ValueError(f"Failed to publish record (code: {response.status_code})")

def save_to_file(record_path, links_filename, links):
    filename = os.path.join(record_path, links_filename)
    with open(filename, "r") as f:
        data = json.load(f)

    data.append(links)

    with open(filename, "w") as f:
        json.dump(data, f)

if __name__ == '__main__':
    print('')
