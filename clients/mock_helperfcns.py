import os,sys
rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(rootp, 'config'))
sys.path.append(os.path.join(rootp, 'db'))
from typing import List
import numpy as np

import config
from db import schemas_pydantic

from random import random
def do_experiment(measurement: schemas_pydantic.Measurement):

    return random()

def do_simulation(measurement: schemas_pydantic.Measurement):
    pass

def assembleXY(measurements,conversions: dict=None,fom_name = 'Density'):
    """
    This function will return a XY style dictionary with explanations. It is custom programmed as a helper
    to return a dictionary containing the molar amounts as X and the density as Y. Adjust to your needs.

    about conversions:
    expecting conversions to contain a conversion between the ratio method and amount
    there is no checking of this hence it is you own best interest to do this.
    Example: if ratio_method is volumetric and amounts is in mol you need a molar volume conversion (mol/V)
    """

    #we need to go through all measurements to get all chemicals
    chemicals = dict()
    for measurement in measurements.values():
        for compound in measurement.formulation.compounds:
            for chemical in compound.chemicals:
                if not chemical.smiles in chemicals.keys():
                    chemicals[chemical.smiles] = chemical

    #unsafe: if we have no conversions we assume you have compound conversion ratios of 1
    if conversions == None:
        conversions = dict()
        for k in chemicals.keys():
            conversions[k] = 1
        conversions['unit'] = 'passtrough'

    #now we can figure out how much of what is where
    amounts,results,idl = [],[],[]
    for km,measurement in measurements.items():
        ratio = measurement.formulation.ratio
        ratiomethod = measurement.formulation.ratio_method

        #assemble a list of chemicals
        amounts_ = dict()
        for ci,compound in enumerate(measurement.formulation.compounds):
            for chemical_amount,chemical in zip(compound.amounts,compound.chemicals):
                if not chemical.smiles in amounts_.keys():
                    amounts_[chemical.smiles] = ratio[ci]*conversions[chemical.smiles]*chemical_amount.value
                else:
                    #print(chemical.smiles + "\n")
                    #print(str(ratio[ci])+ ' '+ str(conversions[chemical.smiles])+ ' '+str(chemical_amount.value)+ "\n")
                    amounts_[chemical.smiles] += ratio[ci]*conversions[chemical.smiles]*chemical_amount.value
        amounts_['unit'] = ratiomethod + '*' + conversions['unit'] + '*' + chemical_amount.unit
        if measurement.fom_data.name == fom_name:
            amounts.append(amounts_)
            results.append(measurement.fom_data.value)
            idl.append(km)
    #now we can make a XY style table for easier post processing
    X_keys = list(chemicals.keys())#dics are potentially unsorted
    X,y,z = [],[],[]
    for a,r,i in zip(amounts,results,idl):
        X_ = [0 for q in range(len(X_keys))]
        for ix,xk in enumerate(X_keys):
            if xk in a.keys():
                X_[ix] = a[xk]
        X.append(X_)
        y.append(r)
        z.append(i)

    return dict(X=X,y=y,z=z,amounts=amounts,results=results,chemicals=X_keys)