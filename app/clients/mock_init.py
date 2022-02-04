import os,sys
rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(rootp, 'config'))
sys.path.append(os.path.join(rootp, 'db'))
print(rootp)

from app.config import config

from app.db import schemas_pydantic
import requests
from app.clients import helperfcns

auth_header = helperfcns.authenticate("kit", "KIT_huipuischui_23")


#for hamid a request
form = schemas_pydantic.Formulation(compounds=[config.LIPF6_EC_DMC], ratio=[1], ratio_method='volumetric')
temp = schemas_pydantic.Temperature(value=293.15, unit='K')
orig = schemas_pydantic.Origin(origin='simulation', what='Density')
meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig)
ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                    data=meas.json(),headers=auth_header).json()

form = schemas_pydantic.Formulation(compounds=[config.EC_DMC], ratio=[1], ratio_method='volumetric')
temp = schemas_pydantic.Temperature(value=293.15, unit='K')
orig = schemas_pydantic.Origin(origin='simulation', what='Density')
meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig)
ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                    data=meas.json(),headers=auth_header).json()

form = schemas_pydantic.Formulation(compounds=[config.EC_EMC], ratio=[1], ratio_method='volumetric')
temp = schemas_pydantic.Temperature(value=293.15, unit='K')
orig = schemas_pydantic.Origin(origin='simulation', what='Density')
meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig)
ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                    data=meas.json(),headers=auth_header).json()


form = schemas_pydantic.Formulation(compounds=[config.LiPF6_EC_EMC], ratio=[1], ratio_method='volumetric')
temp = schemas_pydantic.Temperature(value=293.15, unit='K')
orig = schemas_pydantic.Origin(origin='simulation', what='Density')
meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig)
ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                    data=meas.json(),headers=auth_header).json()


#config.port = 13371
form = schemas_pydantic.Formulation(compounds=[config.LIPF6_EC_DMC], ratio=[1], ratio_method='volumetric')
temp = schemas_pydantic.Temperature(value=293.15, unit='K')
orig = schemas_pydantic.Origin(origin='experiment', what='Density')
meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig)
ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                    data=meas.json(),headers=auth_header).json()

form = schemas_pydantic.Formulation(compounds=[config.EC_DMC], ratio=[1], ratio_method='volumetric')
temp = schemas_pydantic.Temperature(value=293.15, unit='K')
orig = schemas_pydantic.Origin(origin='experiment', what='Density')
meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig)
ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                    data=meas.json(),headers=auth_header).json()

form = schemas_pydantic.Formulation(compounds=[config.EC_EMC], ratio=[1], ratio_method='volumetric')
temp = schemas_pydantic.Temperature(value=293.15, unit='K')
orig = schemas_pydantic.Origin(origin='experiment', what='Density')
meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig)
ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                    data=meas.json(),headers=auth_header).json()


form = schemas_pydantic.Formulation(compounds=[config.LiPF6_EC_EMC], ratio=[1], ratio_method='volumetric')
temp = schemas_pydantic.Temperature(value=293.15, unit='K')
orig = schemas_pydantic.Origin(origin='experiment', what='Density')
meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig)
ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                    data=meas.json(),headers=auth_header).json()