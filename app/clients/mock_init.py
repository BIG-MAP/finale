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

import inspect

auth_header = helperfcns.authenticate("kit", "KIT_huipuischui_23")

# ## Add all the chemicals contained in the compounds to the server
# compoundList = [v for v in dict(inspect.getmembers(config)).values() if type(v)==schemas_pydantic.Compound]
# for compound in compoundList:
#     for chemical in compound.chemicals:
#         _ = requests.post(f"http://{config.host}:{config.port}/api/broker/post/chemical", data=chemical.json(), headers=auth_header).json()

#for hamid a request
# form = schemas_pydantic.Formulation(chemicals=[schemas_pydantic.Chemical(smiles='C1COC(=O)O1', name='EC', reference='EC_ref'), schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_ref'), schemas_pydantic.Chemical(smiles='CCOC(=O)OC', name='EMC', reference='EMC_ref'), schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_ref')], amounts=[{'value':0.408041,'unit':'mol'}, {'value':0.322987,'unit':'mol'}, {'value':0.208846,'unit':'mol'}, {'value':0.060125,'unit':'mol'}], ratio_method='molar')
# temp = schemas_pydantic.Temperature(value=293.15, unit='K')
# orig = schemas_pydantic.Origin(origin='experiment', what='density')
# meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig, fom_data=[])
# # print(meas.json())
# ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
#                     data=meas.json(),headers=auth_header).json()

# form = schemas_pydantic.Formulation(chemicals=[schemas_pydantic.Chemical(smiles='C1COC(=O)O1', name='EC', reference='EC_ref'), schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_ref'), schemas_pydantic.Chemical(smiles='CCOC(=O)OC', name='EMC', reference='EMC_ref'), schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_ref')], amounts=[{'value':0.072355,'unit':'mol'}, {'value':0.823782,'unit':'mol'}, {'value':0.099809,'unit':'mol'}, {'value':0.004054,'unit':'mol'}], ratio_method='molar')
# temp = schemas_pydantic.Temperature(value=293.15, unit='K')
# orig = schemas_pydantic.Origin(origin='experiment', what='viscosity')
# meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig, fom_data=[])
# # print(meas.json())
# ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
#                     data=meas.json(),headers=auth_header).json()

# form = schemas_pydantic.Formulation(chemicals=[schemas_pydantic.Chemical(smiles='C1COC(=O)O1', name='EC', reference='EC_ref'), schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_ref'), schemas_pydantic.Chemical(smiles='CCOC(=O)OC', name='EMC', reference='EMC_ref'), schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_ref')], amounts=[{'value':0.28424,'unit':'mol'}, {'value':0.101964,'unit':'mol'}, {'value':0.555678,'unit':'mol'}, {'value':0.058117,'unit':'mol'}], ratio_method='molar')
# temp = schemas_pydantic.Temperature(value=293.15, unit='K')
# orig = schemas_pydantic.Origin(origin='experiment', what='viscosity')
# meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig, fom_data=[])
# # print(meas.json())
# ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
#                     data=meas.json(),headers=auth_header).json()

form = schemas_pydantic.Formulation(chemicals=[schemas_pydantic.Chemical(smiles='C1COC(=O)O1', name='EC', reference='EC_ref'), schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_ref'), schemas_pydantic.Chemical(smiles='CCOC(=O)OC', name='EMC', reference='EMC_ref'), schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_ref')], amounts=[{'value':0.022141,'unit':'mol'}, {'value':0.933621,'unit':'mol'}, {'value':0.041536,'unit':'mol'}, {'value':0.002701,'unit':'mol'}], ratio_method='molar')
temp = schemas_pydantic.Temperature(value=293.15, unit='K')
orig = schemas_pydantic.Origin(origin='experiment', what='density')
meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig, fom_data=[])
# print(meas.json())
ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                    data=meas.json(),headers=auth_header).json()

# form = schemas_pydantic.Formulation(chemicals=[schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_ref')], amounts=[{'value':1.,'unit':'mol'}], ratio_method='molar')
# temp = schemas_pydantic.Temperature(value=293.15, unit='K')
# orig = schemas_pydantic.Origin(origin='experiment', what='density')
# meas = schemas_pydantic.Measurement(formulation=form, temperature=temp, pending=True, kind=orig, fom_data=[])
# ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
#                    data=meas.json(),headers=auth_header).json()
# print(meas.json())

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