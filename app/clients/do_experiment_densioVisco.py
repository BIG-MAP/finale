import os,sys
rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(rootp, 'config'))
sys.path.append(os.path.join(rootp, 'db'))
sys.path.append(os.path.dirname(rootp))
import requests
import numpy as np
from db import schemas_pydantic

def do_experiment(measurement: schemas_pydantic.Measurement):
    #print(measurement)
    #print(measurement.formulation)
    compounds = frozenset([comp.name for comp in measurement.formulation.compounds])
    ratios = frozenset(measurement.formulation.ratio)
    #print(compounds, type(compounds), ratios, type(ratios))
    #print("mixRatioHelper:", mixingRatio, type(mixingRatio))
    sampleName = str(int(np.random.random()*10**10)) #str(uuid4())#measurement.fom_data.measurement_id
    print("Sample name", sampleName)
    method = "Lovis-DMA_MultiMeasure_20" #TODO: Change when new method implemented.
    measurementtype = "densioVisco"
    print("Starting to mix...")
    _ = requests.get("http://localhost:13372/action/CetoniDevice_action/mix", params={"compounds": compounds, "ratios": ratios}).json()
    print("Mixed. Flows should result in desired volumetric mixing ratio.")
    print(f"Providing sample to {measurementtype}.")
    _ = requests.get("http://localhost:13372/action/CetoniDevice_action/provideSample", params={"measurementtype": measurementtype, "sample_node": "M1.0"}).json()
    print("Sample provided. Ready to measure.")
    print(f"Measuring sample {sampleName}...")
    _ = requests.get("http://localhost:13373/action/densioVisco_action/measure", params={"sampleName": sampleName, "method": method}).json()
    print(f"Waiting for measurement of sample {sampleName} to finish.")
    results = requests.get("http://localhost:13373/action/densioVisco_action/retrieveData", params={"sampleName": sampleName, "method": method, "methodtype": "Measurement", "savePath": "Y:\\extractions"}).json()
    return results