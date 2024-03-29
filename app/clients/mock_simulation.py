import os,sys
rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(rootp, 'config'))
sys.path.append(os.path.join(rootp, 'db'))

import config
from app.db import schemas_pydantic
from helperfcns import authenticate
import requests
import time

while True:
    time.sleep(config.sleeptime)
    print("Logging in...")
    auth_header = authenticate("helge", "1234")

    print("Looking for simulations to do...")
    #asks what measurements are pending
    pending = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending",
                           params={'fom_name':'Density'},headers=auth_header).json()

    #do simulations
    for request_id,request_meas in pending.items():
        #convert to proper measurement
        request_meas = schemas_pydantic.Measurement(**request_meas)
        #do a fancy experiment
        # replace the following line with your experiment for instance
        if request_meas.kind.origin == "Simulation":
            print("Starting a Simulation...")
            fom_value = do_simulation(request_meas)

            fom = schemas_pydantic.FomData(value=fom_value,
                                           unit="g/cm**3",
                                           origin=schemas_pydantic.Origin(origin='experiment'),
                                           measurement_id='123',
                                           name='Density')

            #this adds the data without much hassle but with type checking

            posted_meas = schemas_pydantic.Measurement(formulation=request_meas.formulation,
                                                       temperature=request_meas.temperature,
                                                       pending=False,
                                                       fom_data=fom,
                                                       kind=schemas_pydantic.Origin(origin='experiment'))

            ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/post/measurement",
                                 data=posted_meas.json(),params={'request_id':request_id},headers=auth_header).json()
