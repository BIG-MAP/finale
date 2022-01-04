import os,sys
rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(rootp, 'config'))
sys.path.append(os.path.join(rootp, 'db'))
print(rootp)
import config
from db import schemas_pydantic
import requests

import itertools as it
from random import random

tern = [tup for tup in it.product([round(i/20,4) for i in range(21)],repeat=3) if abs(sum(tup)-1)<1e-9]
tern = [t for t in tern if min(t)>0]
val = [1.3/abs(t[0]-0.331)+1.5/abs(t[1]-0.331)+0.9/abs(t[2]-0.331) for t in tern]

A = schemas_pydantic.Compound(chemicals=[
    schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020'),
    schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')],
                              amounts=[schemas_pydantic.Amount(value=0.5, unit='mol'),
                                       schemas_pydantic.Amount(value=0.1, unit='mol')],
                              name='LiPF6_salt_in_DMC_5:1')
B = schemas_pydantic.Compound(chemicals=[
    schemas_pydantic.Chemical(smiles='CC1COC(=O)O1', name='PC', reference='PC_ELyte_2020'),
    schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')],
                              amounts=[schemas_pydantic.Amount(value=0.5, unit='mol'), schemas_pydantic.Amount(value=0.1, unit='mol')],
                              name='LiPF6_salt_in_PC_5:1')
C = schemas_pydantic.Compound(chemicals=[
    schemas_pydantic.Chemical(smiles='CCOC(=O)OC', name='EMC', reference='EMC_ELyte_2020'),
    schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')],
                              amounts=[schemas_pydantic.Amount(value=0.5, unit='mol'), schemas_pydantic.Amount(value=0.1, unit='mol')],
                              name='LiPF6_salt_in_EMC_5:1')

#first someone posts a lot of requests for measurements
id_meas = []
for t,v in zip(tern,val):
    form_1 = schemas_pydantic.Formulation(compounds=[A, B, C], ratio=t, ratio_method='volumetric')
    temp_1 = schemas_pydantic.Temperature(value=380, unit='K')
    orig_1 = schemas_pydantic.Origin(origin='experiment',what='Density')
    meas_2 = schemas_pydantic.Measurement(formulation=form_1, temperature=temp_1, pending=True, kind=orig_1)
    ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                         data=meas_2.json()).json()
    id_meas.append(ans_)
