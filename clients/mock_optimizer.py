import os,sys
rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(rootp, 'config'))
sys.path.append(os.path.join(rootp, 'clients'))

from config import config
from db import schemas_pydantic
from mock_helperfcns import assembleXY
import requests

from sklearn.ensemble import RandomForestRegressor
import composition

def simple_rf_optimizer(X,y,sampling_dens=0.01,simplex=True):
    # RF are typically not used for geospatial data ... but this is faster than GP
    regr = RandomForestRegressor(n_estimators=50, random_state=1337)

    if simplex:
        X_ = composition.clr(X+np.array([1e-9,1e-9,1e-9,1e-9]))
    regr.fit(X,y)

    #gen test data

    pred = regr.predict(np.array([x[test_ix], y[test_ix]]).T)


    y_var = np.zeros([50, len(x[test_ix])])
    for j in range(50):
        y_var[j, :] = regr.estimators_[j].predict(np.array([x[test_ix], y[test_ix]]).T)

        aqf = pred + np.var(y_var, axis=0)
        ix = np.where(aqf == np.max(aqf))[0]
        i = np.random.choice(ix)

while True:
    #getting all FOM
    all_measurements = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_fom",
                                    params={'fom_name': 'Density'}).json()
    #getting a XY style table
    measurements = {k:schemas_pydantic.Measurement(**m) for k,m in all_measurements.items()}
    xyz = assembleXY(measurements, conversions = None, fom_name = 'Density')
    X,y = xyz['X'],xyz['y']

