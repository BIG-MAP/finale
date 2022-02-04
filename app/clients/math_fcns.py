import os,sys

import numpy as np

rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(rootp, 'config'))
sys.path.append(os.path.join(rootp, 'db'))
print(rootp)

from app.config import config
import time
from app.db import schemas_pydantic
import requests
from app.clients import helperfcns
import numpy as np

auth_header = helperfcns.authenticate("kit", "KIT_huipuischui_23")

def schwefel(params):
    params = 1000 * np.array(params) - 500  # rescale onto [-500, 500]
    result = 0
    for index, element in enumerate(params):
        result += - element * np.sin(np.sqrt(np.abs(element)))
    return (result/1000+0.9816961774673698)/2.4888170198376653


def hypere(params):
    params = np.array(params)
    params = 10 * params - 5  # rescale onto [-5, 5]
    weights = np.arange(1, len(params) + 1)
    result = 0
    for index, element in enumerate(params):
        result += weights[index] * element ** 2
    return (result/100-0.48)/2.02

def levy(params):
    params = np.array(params)
    params = 20 * params - 10  # rescale onto [-10, 10]
    w = 1. + ((params - 1.) / 4.)
    result = np.sin(np.pi * w[0]) ** 2 + ((w[-1] - 1) ** 2) * (1 + np.sin(2 * np.pi * w[-1]) ** 2)
    for i, x in enumerate(params):
        if i + 1 == len(params):
            break
        result += ((w[i] - 1) ** 2) * (1 + 10 * np.sin(np.pi * w[i] + 1) ** 2)
    return (result-10.405454374283481)/239.49297248125478


while True:
    time.sleep(config.sleeptime)
    print("Logging in...")
    auth_header = helperfcns.authenticate("kit", "KIT_huipuischui_23")

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

            #need to attach a fake fom to get a proper value later
            r_meas = request_meas
            origin = schemas_pydantic.Origin(origin='experiment', what='Density')
            r_meas.fom_data = schemas_pydantic.FomData(value=0,unit='g/cm**3',
                                                                 name='Density',
                                                                 origin=origin,
                                                                 measurement_id='fake',
                                                                 fail=True)

            mydata = helperfcns.assembleXY({0:r_meas})
            #get the order right
            chemicals = ['COC(=O)OC','C1COC(=O)O1', '[Li+].F[P-](F)(F)(F)(F)F', 'CCOC(=O)OC']
            ids = [[i for i,c in enumerate(mydata['chemicals']) if c==cc] for cc in chemicals]
            X = []
            for id_ in ids:
                if not id_ == []:
                    X.append(mydata['X'][0][id_[0]])
                else:
                    X.append(0)
            #we return mathematical functions with scaled inputs from 0-1
            if request_meas.kind.what == "Density":
                fom_value = schwefel(X)+np.random.normal(0,0.01)
            elif request_meas.kind.what == "Viscosity":
                fom_value = hypere(X)+np.random.normal(0,0.2)
            elif request_meas.kind.what == "Conductivity":
                fom_value = levy(X)+np.random.normal(0,0.1)
            else:
                fom_value = np.random.rand()

            fom = schemas_pydantic.FomData(value=fom_value,
                                           unit="g/cm**3",
                                           origin=schemas_pydantic.Origin(origin='experiment'),
                                           measurement_id='math functions with noise',
                                           name=request_meas.kind.what)

            #this adds the data without much hassle but with type checking

            posted_meas = schemas_pydantic.Measurement(formulation=request_meas.formulation,
                                                       temperature=request_meas.temperature,
                                                       pending=False,
                                                       fom_data=fom,
                                                       kind=schemas_pydantic.Origin(origin='experiment'))

            ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/post/measurement",
                                 data=posted_meas.json(),params={'request_id':request_id},headers=auth_header).json()
            print(f"Posted a math fcn ... Response: {ans_}")
        else:
            print("Pending a simulation ... nothing to do")


'''
testing this for plotting
'''
import numpy as np
import itertools as it
import matplotlib.pyplot as plt

X = np.array([q for q in it.product([i/100 for i in range(101)],repeat=4) if abs(sum(q)-1)<0.001]).T
v = schwefel(X)+ np.random.normal(0,0.01)+ hypere(X)+np.random.normal(0,0.2)+ levy(X)+np.random.normal(0,0.1)
#plt.hist(fom_value)
ix = np.where(np.abs(X[2,:]-0.8)<0.01)[0]
plt.scatter(X.T[ix,0],X.T[ix,1],c=v[ix])
plt.show()