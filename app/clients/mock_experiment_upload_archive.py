import os,sys
sys.path.append(os.path.join(sys.path[0], '..'))
import config.config as config 
from db import schemas_pydantic
from helperfcns import authenticate
from helperfcns_externalDoExperiment import do_test_experiment
import requests
from test_setups import test_measurement
from bigmap_archive.create_metadata import createMetadataJson
import json 
import sqlite3

con = sqlite3.connect(config.db_file)

# Mocks an experiment with finale, and sends the results back to the archive 

metadata = createMetadataJson()

auth_header = authenticate("kit", "KIT_huipuischui_23")

# Upload pending measurements into the database 

# The database grows larger, and larger over time 

for k in range(5):
    post_measurement = requests.post(
        f"http://{config.host}:{config.port}/api/broker/request/measurement",
        data=test_measurement.json(),
        headers=auth_header)
   


# Get the pending measurements of the database  
pending_meas = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending",
                       params={'fom_name':'density'},headers=auth_header).json()
if type(pending_meas) != list:
    pending_meas = [pending_meas]

i = 0
try:
    for pending in pending_meas:
        i += 1
        for request_id,request_meas_ in pending.items():
            #convert to proper measurement
            request_meas = schemas_pydantic.Measurement(**request_meas_)
            
            if request_meas.kind.origin == "experiment":
                fom_value = do_test_experiment(request_meas)
                Foms = []
                #for key, val in fom_value.items():
                    
                fom_data_vals = fom_value.values
                # FomData expressed a standard scalar output from a measurement
                fom = schemas_pydantic.FomData(values=fom_data_vals,
                                            dim=len(fom_data_vals),
                                            unit='g/cm**3',
                                            origin=schemas_pydantic.Origin(origin='experiment'),
                                            internalReference="123",
                                            name='density')
                Foms.append(fom)

            #this adds the data without much hassle but with type checking
            
            posted_meas = schemas_pydantic.Measurement(formulation=request_meas.formulation,
                                                    temperature=request_meas.temperature,
                                                    pending=False,
                                                    fom_data=Foms,
                                                    kind=schemas_pydantic.Origin(origin='experiment'))
            print(request_id)
            # We send the metadata with 'metadata', meaning we send a string here 
            ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/post/measurement",
                               data=posted_meas.json(),
                               params={'request_id':request_id, 
                               'metadata' : json.dumps(metadata)},headers=auth_header).json()

except Exception as e:
    print('--------',pending,'-------')
    print('ERROR when sending to archive', e)

            
pending_meas = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending",
                       params={'fom_name':'density'},headers=auth_header).json()
print('New pending means:: ', pending_meas)