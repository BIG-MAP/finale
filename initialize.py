import sqlite3
import config
import db
import schemas_pydantic
from uuid import uuid4

db_ = db.dbinteraction()
db_.reset()


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
