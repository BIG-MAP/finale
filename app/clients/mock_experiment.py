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
import numpy as np

units = {"density": "g/cm**3", "viscosity": "mPa*s"}
SMILES = {'EC': 'C1COC(=O)O1', 'DMC': 'COC(=O)OC', 'LiPF6': '[Li+].F[P-](F)(F)(F)(F)F', 'EMC': 'CCOC(=O)OC'}

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
        #convert to proper measurement
        request_meas = schemas_pydantic.Measurement(**request_meas_)
        #do a fancy experiment
        # replace the following line with your experiment for instance
        if request_meas.kind.origin == "experiment":
            print("Starting an experiment...")
            fom_value, mixrat, actualMix= do_experiment(request_meas)
            nan = np.nan
            fom_value = eval(fom_value)

            Foms = []
            for key, val in fom_value.items():
                if key != "sampleName" and key != "quality":
                    print(key,val)
                    fom_data = fom_value[key]
                    fom_values_notNaN = list(pd.Series(fom_data['values']).dropna(inplace=False))
                    if fom_values_notNaN != []:
                        fom = schemas_pydantic.FomData(values=fom_values_notNaN,
                                                    dim=len(fom_data['values']),
                                                    unit=units[key],
                                                    origin=schemas_pydantic.Origin(origin='experiment', what=str(key)),
                                                    internalReference=fom_value["sampleName"],
                                                    message=f'volumetric: {str(mixrat)}, mole ratio: {str(actualMix)}',
                                                    name=str(key),
                                                    fail=False,
                                                    rating=fom_value[key]['quality'])
                    else:
                        fom = schemas_pydantic.FomData(values=list(np.zeros(len(fom_data['values']))),
                                                    dim=len(fom_data['values']),
                                                    unit=units[key],
                                                    origin=schemas_pydantic.Origin(origin='experiment', what=str(key)),
                                                    internalReference=fom_value["sampleName"],
                                                    message=f'volumetric: {str(mixrat)}, mole ratio: {str(actualMix)}',
                                                    name=str(key),
                                                    fail=True,
                                                    rating=fom_value[key]['quality'])
                    Foms.append(fom)

            ## Assemble the actual formulation based on the actualMix results
            # Get the chemicals in the actual mixture
            chemicals = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_chemicals", headers=auth_header).json()
            chemicalsList = []
            for chemicalInfo in chemicals.values():
                if actualMix[chemicalInfo['name']] > 0.0:
                    chemical = schemas_pydantic.Chemical(smiles=chemicalInfo['smiles'], name=chemicalInfo['name'], reference=chemicalInfo['reference'])
                    chemicalsList.append(chemical)

            amounts = []
            for rat in actualMix.values():
                if rat > 0.0:
                    amount = schemas_pydantic.Amount(value=rat, unit='mol')#.-%')
                    amounts.append(amount)

            actualFormulation = schemas_pydantic.Formulation(chemicals=chemicalsList,amounts=amounts, ratio_method='other')
            #this adds the data without much hassle but with type checking

            posted_meas = schemas_pydantic.Measurement(formulation=actualFormulation,
                                                    temperature=request_meas.temperature,
                                                    pending=False,
                                                    fom_data=Foms,
                                                    kind=schemas_pydantic.Origin(origin='experiment', what='vectorial'))

            ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/post/measurement",
                                data=posted_meas.json(),params={'request_id':request_id},headers=auth_header).json()
            print(f"Posted an experiment ... Response: {ans_}")
        else:
            print("Pending a simulation ... nothing to do")
