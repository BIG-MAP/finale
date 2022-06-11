import os,sys
rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(rootp, 'config'))
sys.path.append(os.path.join(rootp, 'db'))
sys.path.append(os.path.dirname(rootp)) # Monika's line. Consider deleting it, if it is not working for you.
print(rootp)

from app.config import config

from app.db import schemas_pydantic
import requests
from app.clients import helperfcns

auth_header = helperfcns.authenticate("kit", "KIT_huipuischui_23")


#for hamid a request
form = schemas_pydantic.Formulation(chemicals=[schemas_pydantic.Chemical(smiles='C1COC(=O)O1', name='EC', reference='EC_Elyte_2020'), schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020')], amounts=[{'value':0.7,'unit':'mol'}, {'value':0.3,'unit':'mol'}], ratio_method='molar')
temp = schemas_pydantic.Temperature(value=293.15, unit='K')
orig = schemas_pydantic.Origin(origin='experiment', what='density')
meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig, fom_data=[])
ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                    data=meas.json(),headers=auth_header).json()

# form = schemas_pydantic.Formulation(chemicals=[config.EC_DMC], ratio=[1], ratio_method='volumetric')
# temp = schemas_pydantic.Temperature(value=293.15, unit='K')
# orig = schemas_pydantic.Origin(origin='simulation', what='Density')
# meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig)
# ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
#                     data=meas.json(),headers=auth_header).json()

# form = schemas_pydantic.Formulation(chemicals=[config.EC_EMC], ratio=[1], ratio_method='volumetric')
# temp = schemas_pydantic.Temperature(value=293.15, unit='K')
# orig = schemas_pydantic.Origin(origin='simulation', what='Density')
# meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig)
# ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
#                     data=meas.json(),headers=auth_header).json()


# form = schemas_pydantic.Formulation(chemicals=[config.LiPF6_EC_EMC], ratio=[1], ratio_method='volumetric')
# temp = schemas_pydantic.Temperature(value=293.15, unit='K')
# orig = schemas_pydantic.Origin(origin='simulation', what='Density')
# meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig)
# ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
#                     data=meas.json(),headers=auth_header).json()


# #config.port = 13371
# form = schemas_pydantic.Formulation(chemicals=[config.LIPF6_EC_DMC], ratio=[1], ratio_method='volumetric')
# temp = schemas_pydantic.Temperature(value=293.15, unit='K')
# orig = schemas_pydantic.Origin(origin='experiment', what='Density')
# meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig)
# ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
#                     data=meas.json(),headers=auth_header).json()

# form = schemas_pydantic.Formulation(chemicals=[config.EC_DMC], ratio=[1], ratio_method='volumetric')
# temp = schemas_pydantic.Temperature(value=293.15, unit='K')
# orig = schemas_pydantic.Origin(origin='experiment', what='Density')
# meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig)
# ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
#                     data=meas.json(),headers=auth_header).json()

# form = schemas_pydantic.Formulation(chemicals=[config.EC_EMC], ratio=[1], ratio_method='volumetric')
# temp = schemas_pydantic.Temperature(value=293.15, unit='K')
# orig = schemas_pydantic.Origin(origin='experiment', what='Density')
# meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig)
# ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
#                     data=meas.json(),headers=auth_header).json()


# form = schemas_pydantic.Formulation(chemicals=[config.LiPF6_EC_EMC], ratio=[1], ratio_method='volumetric')
# temp = schemas_pydantic.Temperature(value=293.15, unit='K')
# orig = schemas_pydantic.Origin(origin='experiment', what='Density')
# meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig)
# ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
#                     data=meas.json(),headers=auth_header).json()