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
from helperfcns import do_experiment,authenticate
import requests
import time
import numpy as np

units = {"density": "g/cm**3", "viscosity": "mPa*s"}

while True:
    time.sleep(config.sleeptime)
    print("Logging in...")
    auth_header = authenticate("helge", "1234")

    print("Looking for things to do...")
    #someone then asks what measurements are pending
    pending = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending",
                           params={'fom_name':'Density'},headers=auth_header).json()

    #someone does an experiment
    for request_id,request_meas_ in pending.items():
        #convert to proper measurement
        request_meas = schemas_pydantic.Measurement(**request_meas_)
        #do a fancy experiment
        # replace the following line with your experiment for instance
        if request_meas.kind.origin == "experiment":
            print("Starting an experiment...")
            fom_value = do_experiment(request_meas)
            print("fom_value:", fom_value)

            for key, val in fom_value.items():
                if key != "sampleName":
                    print("key:", key, "val:", val)
                    print(type(val), type(val["values"]), type(val["values"][0]))
                    valFloat = []
                    for v in val["values"]:
                        try:
                            valFloat.append(float(v))
                        except ValueError:
                            valFloat.append(np.NaN)
                    valFloat = np.array(valFloat)


                    fom = schemas_pydantic.FomData(value=np.mean(valFloat),
                                                unit=units[key],
                                                origin=schemas_pydantic.Origin(origin='experiment'),
                                                measurement_id=fom_value["sampleName"],
                                                name=str(key.capitalize()))

                    #this adds the data without much hassle but with type checking

                    posted_meas = schemas_pydantic.Measurement(formulation=request_meas.formulation,
                                                            temperature=request_meas.temperature,
                                                            pending=False,
                                                            fom_data=fom,
                                                            kind=schemas_pydantic.Origin(origin='experiment'))

                    print(posted_meas)

                    ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/post/measurement",
                                        data=posted_meas.json(),params={'request_id':request_id},headers=auth_header).json()
            print(f"Posted an experiment ... Response: {ans_}")
        else:
            print("Pending a simulation ... nothing to do")
