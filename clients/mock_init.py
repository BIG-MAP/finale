import os,sys
rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(rootp, 'config'))
sys.path.append(os.path.join(rootp, 'db'))
print(rootp)

import config
from db import schemas_pydantic
import requests
import helperfcns

auth_header = helperfcns.authenticate("helge","1234")

#initialize the pure compounds so nothing complains
ids = []
#LIPF6
form = schemas_pydantic.Formulation(compounds=[config.lipf6], ratio=[1], ratio_method='volumetric')
temp = schemas_pydantic.Temperature(value=298.15, unit='K')
orig = schemas_pydantic.Origin(origin='experiment',what='Density')
meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig)
ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                    data=meas.json(),headers=auth_header).json()
ids.append(ans_)
#DMC
form = schemas_pydantic.Formulation(compounds=[config.dmc], ratio=[1], ratio_method='volumetric')
meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig)
ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                    data=meas.json(),headers=auth_header).json()
ids.append(ans_)
#PC
form = schemas_pydantic.Formulation(compounds=[config.pc], ratio=[1], ratio_method='volumetric')
meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig)
ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                    data=meas.json(),headers=auth_header).json()
ids.append(ans_)
#EMC
form = schemas_pydantic.Formulation(compounds=[config.emc], ratio=[1], ratio_method='volumetric')
meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig)
ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                    data=meas.json(),headers=auth_header).json()
ids.append(ans_)
print(ids)