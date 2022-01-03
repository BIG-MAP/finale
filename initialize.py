import random
import sqlite3
import config
import db
import schemas_pydantic
from uuid import UUID
'''
db_ = db.dbinteraction()
#db_.reset()



chem_list = [
    ('COC(=O)OC', 'DMC', 'DMC_Elyte_2020'),
    ('[Li+].F[P-](F)(F)(F)(F)F', 'LiPF6', 'LiPF6_Elyte_2020'),
    ('smile_3', 'name_3', 'ref_3'),
    ('smile_4', 'name_4', 'ref_4'),
    ('smile_5', 'name_5', 'ref_5'),
    ('smile_6', 'name_6', 'ref_6'),
]

def make_chemicals(c):
    return schemas_pydantic.Chemical(name=c[1],smiles=c[0],reference=c[2])

chem_ids = []
for c in chem_list:
    chem_ids.append(db_.add_chemical(make_chemicals(c)))

A = schemas_pydantic.Compound(chemicals=[schemas_pydantic.Chemical(smiles='COC(=O)OC',name='DMC',reference='DMC_Elyte_2020'),
                                  schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F',name='LiPF6',reference='LiPF6_Elyte_2020')],
                       amounts=[schemas_pydantic.Amount(value=0.5,unit='mol'),schemas_pydantic.Amount(value=0.1,unit='mol')],
                       name='LiPF6_salt_in_DMC_5:1')

id_comp1 = db_.add_compound(A)
id_comp2 = db_.add_compound(A)


B = schemas_pydantic.Compound(chemicals=[schemas_pydantic.Chemical(smiles='CC1COC(=O)O1', name='PC', reference='PC_ELyte_2020'),
                        schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')],
             amounts=[schemas_pydantic.Amount(value=0.5, unit='mol'), schemas_pydantic.Amount(value=0.1, unit='mol')],
             name='LiPF6_salt_in_PC_5:1')

form_1 = schemas_pydantic.Formulation(compounds=[A, B], ratio=[3, 1], ratio_method='volumetric')

id_form1 = db_.add_formulation(form_1)
temp_1 = schemas_pydantic.Temperature(value=380,unit='K')
orig_1 = schemas_pydantic.Origin(origin='experiment')
meas_1 = schemas_pydantic.Measurement(formulation=form_1, temperature=temp_1, pending=True, kind=orig_1)

id_form1 = db_.add_measurement(meas_1)

fom_1 = schemas_pydantic.FomData(value=3,unit="g/cm**3",origin=orig_1,measurement_id='123',name='Density')

meas_2 = schemas_pydantic.Measurement(formulation=form_1, temperature=temp_1, pending=True, kind=orig_1,fom_data=fom_1)

id_form1 = db_.add_measurement(meas_2)


#we make a ternary with max somewhere near the middle
import itertools as it
tern = [tup for tup in it.product([i/10 for i in range(11)],repeat=3) if sum(tup)==1]
val = [1.3/abs(t[0]-0.33)+1.5/abs(t[1]-0.33)+0.9/abs(t[2]-0.33) for t in tern]

A = schemas_pydantic.Compound(chemicals=[schemas_pydantic.Chemical(smiles='COC(=O)OC',name='DMC',reference='DMC_Elyte_2020'),
                                  schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F',name='LiPF6',reference='LiPF6_Elyte_2020')],
                       amounts=[schemas_pydantic.Amount(value=0.5,unit='mol'),schemas_pydantic.Amount(value=0.1,unit='mol')],
                       name='LiPF6_salt_in_DMC_5:1')
B = schemas_pydantic.Compound(chemicals=[schemas_pydantic.Chemical(smiles='CC1COC(=O)O1', name='PC', reference='PC_ELyte_2020'),
                        schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')],
             amounts=[schemas_pydantic.Amount(value=0.5, unit='mol'), schemas_pydantic.Amount(value=0.1, unit='mol')],
             name='LiPF6_salt_in_PC_5:1')
C = schemas_pydantic.Compound(chemicals=[schemas_pydantic.Chemical(smiles='CCOC(=O)OC', name='EMC', reference='EMC_ELyte_2020'),
                        schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')],
             amounts=[schemas_pydantic.Amount(value=0.5, unit='mol'), schemas_pydantic.Amount(value=0.1, unit='mol')],
             name='LiPF6_salt_in_EMC_5:1')

id_meas = []
for t,v in zip(tern,val):
    form_1 = schemas_pydantic.Formulation(compounds=[A, B, C], ratio=t, ratio_method='volumetric')
    temp_1 = schemas_pydantic.Temperature(value=380,unit='K')
    orig_1 = schemas_pydantic.Origin(origin='experiment')
    fom_1 = schemas_pydantic.FomData(value=v, unit="g/cm**3", origin=orig_1, measurement_id='123', name='Density')
    meas_2 = schemas_pydantic.Measurement(formulation=form_1, temperature=temp_1, pending=False, kind=orig_1,fom_data=fom_1)
    id_meas.append(db_.add_measurement(meas_2))


id_ = id_meas[2]
me = db_.query_measurement_by_id(id_)
db_.con.commit()
db_.con.close()

#test the API
'''

import requests
import random
#chemical posting
ans = []
for i in range(100):
    chemical = schemas_pydantic.Chemical(name=f'name_{i}',smiles=f'smiles_{i}',reference='ref_{i}')
    ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/post/chemical",
                        data=chemical.json()).json()
    ans.append(ans_)

#compound posting
ans = []
for i in range(100):
    compound = schemas_pydantic.Compound(chemicals=[schemas_pydantic.Chemical(smiles='CC1COC(=O)O1', name='PC', reference='PC_ELyte_2020'),
                        schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')],
             amounts=[schemas_pydantic.Amount(value=random.random(), unit='mol'), schemas_pydantic.Amount(value=random.random(), unit='mol')],
             name=f'LiPF6_salt_in_PC_random_{i}')
    ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/post/compound",
                        data=compound.json()).json()
    ans.append(ans_)

#getting chemicals
res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_chemicals").json()

#getting compounds
res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_compounds").json()

#posting measurements
import itertools as it
tern = [tup for tup in it.product([i/10 for i in range(11)],repeat=3) if sum(tup)==1]
val = [1.3/abs(t[0]-0.33)+1.5/abs(t[1]-0.33)+0.9/abs(t[2]-0.33) for t in tern]

A = schemas_pydantic.Compound(chemicals=[schemas_pydantic.Chemical(smiles='COC(=O)OC',name='DMC',reference='DMC_Elyte_2020'),
                                  schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F',name='LiPF6',reference='LiPF6_Elyte_2020')],
                       amounts=[schemas_pydantic.Amount(value=0.5,unit='mol'),schemas_pydantic.Amount(value=0.1,unit='mol')],
                       name='LiPF6_salt_in_DMC_5:1')
B = schemas_pydantic.Compound(chemicals=[schemas_pydantic.Chemical(smiles='CC1COC(=O)O1', name='PC', reference='PC_ELyte_2020'),
                        schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')],
             amounts=[schemas_pydantic.Amount(value=0.5, unit='mol'), schemas_pydantic.Amount(value=0.1, unit='mol')],
             name='LiPF6_salt_in_PC_5:1')
C = schemas_pydantic.Compound(chemicals=[schemas_pydantic.Chemical(smiles='CCOC(=O)OC', name='EMC', reference='EMC_ELyte_2020'),
                        schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')],
             amounts=[schemas_pydantic.Amount(value=0.5, unit='mol'), schemas_pydantic.Amount(value=0.1, unit='mol')],
             name='LiPF6_salt_in_EMC_5:1')

id_meas = []
for t,v in zip(tern,val):
    form_1 = schemas_pydantic.Formulation(compounds=[A, B, C], ratio=t, ratio_method='volumetric')
    temp_1 = schemas_pydantic.Temperature(value=380,unit='K')
    orig_1 = schemas_pydantic.Origin(origin='experiment')
    fom_1 = schemas_pydantic.FomData(value=v, unit="g/cm**3", origin=orig_1, measurement_id='123', name='Density')
    meas_2 = schemas_pydantic.Measurement(formulation=form_1, temperature=temp_1, pending=False, kind=orig_1,fom_data=fom_1)
    ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/post/measurement",
                        data=meas_2.json()).json()
    id_meas.append(ans_)

idq = id_meas[11]['id']
ans_ = requests.get(f"http://{config.host}:{config.port}/api/broker/get/measurement",
                        params={'query_id':idq}).json()
retrieved_measurement = schemas_pydantic.Measurement(**ans_)

#getting all FOM
res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_fom",params={'fom_name':'Density'}).json()


#requesting a measurement wrongly by posting
meas_2 = schemas_pydantic.Measurement(formulation=form_1, temperature=temp_1, pending=True, kind=orig_1)
ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/post/measurement",
                     data=meas_2.json()).json()

#requesting a measurement wrongly by not supplying data
meas_2 = schemas_pydantic.Measurement(formulation=form_1, temperature=temp_1, pending=False, kind=orig_1)
ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/post/measurement",
                     data=meas_2.json()).json()

#requesting a measurement wrongly by setting pending to false
meas_2 = schemas_pydantic.Measurement(formulation=form_1, temperature=temp_1, pending=False, kind=orig_1)
ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                     data=meas_2.json()).json()

#not specifying what to measure when posting a measurement
orig_1 = schemas_pydantic.Origin(origin='experiment')
meas_2 = schemas_pydantic.Measurement(formulation=form_1, temperature=temp_1, pending=True, kind=orig_1)
ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                     data=meas_2.json()).json()

#correctly posting a measurement
orig_1 = schemas_pydantic.Origin(origin='experiment',what='Density')
meas_2 = schemas_pydantic.Measurement(formulation=form_1, temperature=temp_1, pending=True, kind=orig_1)
ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                     data=meas_2.json()).json()