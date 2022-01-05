import os,sys
rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(rootp, 'config'))
sys.path.append(os.path.join(rootp, 'clients'))
# terminal run: rootp += "/fastALE/"
import config
from db import schemas_pydantic
from mock_helperfcns import assembleXY
import requests
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import composition
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.optimize import minimize

def simple_rf_optimizer(X_,y,sampling_dens=0.01,simplex=True,maximize=False,return_all=True):
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
    #get a XY style table
    measurements = {k:schemas_pydantic.Measurement(**m) for k,m in all_measurements.items()}
    xyz = assembleXY(measurements, conversions = config.densities, fom_name = 'Density')
    X,y = xyz['X'],xyz['y']

    #ask the optimizer what to try
    return_all = False
    try_chem_ratios = simple_rf_optimizer(X,y,return_all=return_all)

    #translate this result into a formulation
    #warning: It may very well be possibile that the suggested chemical composition is not attainable
    #with the used compounds compositions. Right now I oped to just go for the closest one. An alternative
    #is to take the one with an error lower than the threshold...
    if return_all:
        errs = []
        for chem_ratio in try_chem_ratios:
            target = {chem_name:amnt for amnt,chem_name in zip(chem_ratio,xyz['chemicals'])}
            ratios,err = get_formulation(target,conversions=config.densities)
            errs.append(err)
    else:
        target = {chem_name: amnt for amnt, chem_name in zip(try_chem_ratios, xyz['chemicals'])}
        ratios, err = get_formulation(target)
        errs = [err]
        print(f"Error of formulation: {err}")
    #post the suggestion to the broker server
    #arrange the compounds right
    compounds = get_compounds()
    ratios_arranged = [ratios[c] for c in [cn.name for cn in compounds]]

    form_post = schemas_pydantic.Formulation(compounds=compounds, ratio=ratios_arranged, ratio_method='volumetric')
    temp = schemas_pydantic.Temperature(value=298.15, unit='K')
    orig = schemas_pydantic.Origin(origin='experiment', what='Density')
    meas_request = schemas_pydantic.Measurement(formulation=form_post, temperature=temp, pending=True, kind=orig)
    ans = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                             data=meas_request.json()).json()
    print(ans)
