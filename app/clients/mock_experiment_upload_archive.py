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



# Mocks an experiment with finale, and sends the results back to the archive 

metadata = createMetadataJson()

auth_header = authenticate("kit", "KIT_huipuischui_23")


# Firstly we send a post request to FINALE 
# This is done by sending the measurement we want to perform

post_measurement = requests.post(
    f"http://{config.host}:{config.port}/api/broker/request/measurement",
    data=test_measurement.json(), # This is the measurement
    headers=auth_header)


pending_meas = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending",
                       params={'fom_name':'density'},headers=auth_header).json()
if type(pending_meas) != list:
    pending_meas = [pending_meas]

i = 0

# We 
try:
    # This part is to simulate the HELAO framework
    # It loops over all the pending measurements inside FINALE
    for pending in pending_meas:
        i += 1
        for request_id,request_meas_ in pending.items():
           
           
            request_meas = schemas_pydantic.Measurement(**request_meas_)
            
            if request_meas.kind.origin == "experiment":
                # HELAO then executed the measurement 
                fom_value = do_test_experiment(request_meas)
                Foms = []
                    
                fom_data_vals = fom_value.values
                # FomData expressed a standard scalar output from a measurement
                fom = schemas_pydantic.FomData(values=fom_data_vals,
                                            dim=len(fom_data_vals),
                                            unit=fom_value.unit,
                                            origin=fom_value.origin,
                                            internalReference=fom_value.internalReference,
                                            name=fom_value.name)
                Foms.append(fom)

            
            # The measurement results has to follow strict 
            # standards, which are implemented using the pydantic module 
            store_to_archive = schemas_pydantic.ArchiveStorage(upload=True, 
                append=False, existingRecord='1')
            posted_meas = schemas_pydantic.Measurement(formulation=request_meas.formulation,
                                                    temperature=request_meas.temperature,
                                                    pending=False,
                                                    fom_data=Foms,
                                                    store_to_archive = store_to_archive,
                                                    kind=fom_value.origin)
            
            # The "simulated" HELAO then sends a post request to FINALE 
            # The request contains the dummy experimental data
            # At the same time that FINALE recieves the data, it gets uploaded 
            # to the BIG-MAP archive
            ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/post/measurement",
                               data=posted_meas.json(),
                               params={'request_id':request_id, 
                               'metadata' : json.dumps(metadata)},headers=auth_header).json()
            print('Measurement with id', request_id)
            print('Added succesfully to the BIG-MAP archive')
            
except Exception as e:
    print('--------','Measurement with request id :',request_id ,'-------')
    print('Could not be uploaded')
    print('ERROR when sending to archive', e)
