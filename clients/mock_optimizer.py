import os,sys
rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(rootp, 'config'))
sys.path.append(os.path.join(rootp, 'clients'))

import config
from db import schemas_pydantic
from mock_helperfcns import assembleXY
import requests
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import composition
import matplotlib.pyplot as plt
from tqdm import tqdm

def simple_rf_optimizer(X_,y,sampling_dens=0.01,simplex=True,maximize=True,return_all=True):
    # RF are typically not used for geospatial data ... but this is faster than GP
    regr = RandomForestRegressor(n_estimators=50, random_state=1337)

    if simplex:
        X = composition.ilr(X_+np.array([1e-10 for i in range(len(X_[0]))]))
    else:
        X = X_
    if maximize:
        pass
    else:
        y = -np.array(y)

    regr.fit(X,y)

    #gen test data
    Xm,XM = np.min(X,axis=0),np.max(X,axis=0)
    Xtry = np.array(np.meshgrid(*[np.linspace(m,M,40) for m,M in zip(Xm,XM)])).reshape(-1,len(Xm))
    pred = regr.predict(Xtry)

    y_var = np.zeros([50, len(pred)])
    for j in tqdm(range(50)):
        y_var[j, :] = regr.estimators_[j].predict(Xtry)
    var = np.var(y_var, axis=0)
    #my crazy aquisition function that scales for variance!
    aqf = pred/np.var(pred) + var/np.var(var)
    if return_all:
        aqf_lvl = np.unique(aqf)
        i = []
        for lvl in np.sort(-aqf_lvl):
            level_indices = np.where(aqf==-lvl)[0]
            i.append(np.random.choice(level_indices))
    else:
        ix = np.where(aqf == np.max(aqf))[0]
        i = np.random.choice(ix)

    if simplex:
        rv = composition.ilr_inv(Xtry[i])
    else:
        rv = Xtry[i]
    return rv

while True:
    #getting all FOM
    all_measurements = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_fom",
                                    params={'fom_name': 'Density'}).json()
    #getting a XY style table
    measurements = {k:schemas_pydantic.Measurement(**m) for k,m in all_measurements.items()}
    xyz = assembleXY(measurements, conversions = None, fom_name = 'Density')
    X,y = xyz['X'],xyz['y']
    try_chem_ratios = simple_rf_optimizer(X,y)

    for chem_ratio in try_chem_ratios:
        ratio = calc_formulation_from_chemicals(chem_ratio)
    #now we need to figure out if it is possibile to make this formulation
    #given our compounds! (nah who though of this!?)
    compounds = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_compounds").json()
    compounds = [schemas_pydantic.Compound(**c) for c in compounds.values()]
    #find out which chemicals we have
    chemicals = dict()
    for compound in compounds:
        for chemical in compound.chemicals:
            if not chemical.smiles in chemicals.keys():
                chemicals[chemical.smiles] = chemical
    smilesl = list(chemicals.keys())
    premat = {c.name:{s:0 for s in smilesl} for c in compounds}
    for compound in compounds:
        for chemical,amount in zip(compound.chemicals,compound.amounts):
            premat[compound.name][chemical.smiles] += amount.value
    # with premat we can get a formulation or ratio that minimizes the difference
