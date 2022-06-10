import os,sys
rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
#rootp += "/fastALE/"
sys.path.append(os.path.join(rootp, 'config'))
sys.path.append(os.path.join(rootp, 'db'))
sys.path.append(os.path.join(rootp, 'clients'))
sys.path.append(os.path.dirname(rootp))
print(rootp)

import config
from app.db import schemas_pydantic
from helperfcns import authenticate
from helperfcns_externalDoExperiment import do_experiment
import requests
import time
import pandas as pd

units = {"density": "g/cm**3", "viscosity": "mPa*s"}

while True:
    time.sleep(config.sleeptime)
    print("Logging in...")
    auth_header = authenticate("kit", "KIT_huipuischui_23")

    print("Looking for things to do...")
    #someone then asks what measurements are pending
    pending = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending",
                           params={'fom_name':'density'},headers=auth_header).json()

    #someone does an experiment
    for request_id,request_meas_ in pending.items():
        print(request_meas_)
        #convert to proper measurement
        request_meas = schemas_pydantic.Measurement(**request_meas_)
        #do a fancy experiment
        # replace the following line with your experiment for instance
        if request_meas.kind.origin == "experiment":
            print("Starting an experiment...")
            fom_value, mixrat= do_experiment(request_meas)

            for key, val in fom_value.items():
                if key != "sampleName" and key != "quality":
                    fom_data = pd.Series(fom_value[key])
                    fom = schemas_pydantic.FomData(value=fom_data,
                                                unit=units[key],
                                                origin=schemas_pydantic.Origin(origin='experiment'),
                                                measurement_id=fom_value["sampleName"],
                                                name=str(key))

            #this adds the data without much hassle but with type checking

            posted_meas = schemas_pydantic.Measurement(formulation=request_meas.formulation,
                                                       temperature=request_meas.temperature,
                                                       pending=False,
                                                       fom_data=fom,
                                                       kind=schemas_pydantic.Origin(origin='experiment'))

            ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/post/measurement",
                                 data=posted_meas.json(),params={'request_id':request_id},headers=auth_header).json()
            print(f"Posted an experiment ... Response: {ans_}")
        else:
            print("Pending a simulation ... nothing to do")
