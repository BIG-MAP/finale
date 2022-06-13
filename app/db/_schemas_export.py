import sys
sys.path.extend(['./app/db'])
import os
cwd = os.getcwd()
import schemas_pydantic

#agent = schemas_pydantic.Agent(online=True, kind='Simulation',)


dmc = schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020')

with open(r'./app/schemas_export/Chemical.json', 'w') as f:
    f.write(schemas_pydantic.Chemical.schema_json(indent=2))


form = schemas_pydantic.Formulation(chemicals=[schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020'),
                                                schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')],
    amounts=[schemas_pydantic.Amount(value=1.0, unit='mol'),schemas_pydantic.Amount(value=0.1, unit='mol')],
    ratio_method='molal')

with open('./app/schemas_export/Formulation.json', 'w') as f:
    f.write(schemas_pydantic.Formulation.schema_json(indent=2))

orig = schemas_pydantic.Origin(origin='simulation', what='density')

with open('./app/schemas_export/Origin.json', 'w') as f:
    f.write(schemas_pydantic.Origin.schema_json(indent=2))

data = schemas_pydantic.FomData(values=[1.23],unit='g/cm**2',dim=1,
                                name='density',origin=orig,internalReference='aTest',
                                fail=False, message='My Message', rating=1)

data_nd = schemas_pydantic.FomData(values=[1.23,234,12,13,56,26],unit='g/cm**2',dim=6,
                                name='vectorial',origin=orig,internalReference='aTest',
                                fail=False, message='My Message', rating=1)

with open('./app/schemas_export/FomData.json', 'w') as f:
    f.write(schemas_pydantic.FomData.schema_json(indent=2))

temp = schemas_pydantic.Temperature(value=300,unit='K')

with open('./app/schemas_export/Temperature.json', 'w') as f:
    f.write(schemas_pydantic.Temperature.schema_json(indent=2))

meas = schemas_pydantic.Measurement(formulation=form,temperature=temp,pending=False,fom_data=[data],kind=orig)

with open('./app/schemas_export/Measurement.json', 'w') as f:
    f.write(schemas_pydantic.Measurement.schema_json(indent=2))