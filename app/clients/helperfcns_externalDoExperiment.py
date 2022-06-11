import os,sys
rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(rootp, 'config'))
sys.path.append(os.path.join(rootp, 'db'))

from sklearn.ensemble import RandomForestRegressor
from app.clients import composition
from tqdm import tqdm
from scipy.optimize import minimize
import numpy as np

import requests
import config
from app.db import schemas_pydantic

from passlib.context import CryptContext

from do_experiment_densioVisco import do_experiment_densioVisco


from random import random
def do_experiment(measurement: schemas_pydantic.Measurement):
    results, mixRatio = do_experiment_densioVisco(measurement)
    return results, mixRatio


def do_simulation(measurement: schemas_pydantic.Measurement):
    return random()



def get_compounds(auth_header):
    compounds = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_compounds",headers=auth_header).json()
    compounds = [schemas_pydantic.Compound(**c) for c in compounds.values()]
    return compounds


def get_formulation(chem_ratio,auth_header,conversions: dict=None):
    # now we need to figure out if it is possibile to make this formulation
    # given our compounds! (nah who though of this!?)
    compounds = get_compounds(auth_header)
    # find out which chemicals we have
    chemicals = dict()
    for compound in compounds:
        for chemical in compound.chemicals:
            if not chemical.smiles in chemicals.keys():
                chemicals[chemical.smiles] = chemical
    if conversions == None:
        conversions = {n:1 for i,n in enumerate(chemicals.keys())}
    smilesl = list(chemicals.keys())

    #now we focus on the actual problem
    premat = {c.name: {s: 0 for s in smilesl} for c in compounds}
    for compound in compounds:
        for chemical, amount in zip(compound.chemicals, compound.amounts):
            premat[compound.name][chemical.smiles] += amount.value
    # with premat we can get a formulation or ratio that minimizes the difference
    target = chem_ratio#{chem_name: amnt for amnt, chem_name in zip(chem_ratio, xyz['chemicals'])}

    order_chem = list(target.keys())
    order_comp = list(premat.keys())
    def mini(factors,target=target,premat=premat,conversions=conversions):
        t = np.array([target[k] for k in order_chem])
        c = np.array([conversions[k] for k in order_chem])
        mat = c*np.array([[premat[k2][k] for k in order_chem] for k2 in order_comp])
        fac_alr = composition.alr_inv(factors)
        f = np.dot(fac_alr,mat)
        return np.sum((f-t)**2)

    res = minimize(mini,x0=[1 for i in range(len(premat.keys())-1)],method='L-BFGS-B')
    ratio_ilr = res.x
    ratio = composition.alr_inv(ratio_ilr)
    if mini(ratio_ilr)>config.ratio_threshold:
        print(f"Ratio error is: {mini(ratio_ilr)}")
    return {compound:r for compound,r in zip(order_comp,ratio)},mini(ratio_ilr)

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

def simple_rf_optimizer(X_,y,sampling_dens=0.01,simplex=True,maximize=False,return_all=True):
    # RF are typically not used for geospatial data ... but this is faster than GP
    regr = RandomForestRegressor(n_estimators=50, random_state=1337)

    if simplex:
        X = composition.ilr(X_ + np.array([1e-10 for i in range(len(X_[0]))]))
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


def authenticate(user, pw):
    token_response = requests.post(f"http://{config.host}:{config.port}/token",
                                   data={"username": user, "password": pw, "grant_type": "password"},
                                   headers={"content-type": "application/x-www-form-urlencoded"})

    token_response = token_response.json()
    token = token_response['access_token']

    auth_header = {'Authorization': 'Bearer {}'.format(token)}

    return auth_header

def hashpw(pw):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(pw)