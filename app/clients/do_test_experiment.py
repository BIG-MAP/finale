import os,sys

from tqdm import tqdm
import numpy as np
sys.path.append(os.path.join(sys.path[0], '..'))
from db import schemas_pydantic
import time 

def test_experiment(measurement: schemas_pydantic.Measurement):
    time.sleep(5)
    '''
        Simulate doing a real world experiment 
        Returns fom data 
    '''
    fom_data = fom_test = schemas_pydantic.FomData(values=[1.01], dim=1,
        unit="g/cm**3", origin=schemas_pydantic.Origin(origin='experiment'), 
        internalReference='123', name='density')
    return fom_data

