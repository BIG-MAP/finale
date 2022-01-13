import sys
sys.path.extend(['/Users/helgestein/PycharmProjects/finale/db'])

import schemas_pydantic
import json

dmc = schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020')

dmc_compound = schemas_pydantic.Compound(chemicals=[
    schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020')],
    amounts=[schemas_pydantic.Amount(value=1.0, unit='mol')],
    name='DMC')

lipf6_dmc = schemas_pydantic.Compound(chemicals=[
    schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020'),
    schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')],
    amounts=[schemas_pydantic.Amount(value=1.0, unit='mol'), schemas_pydantic.Amount(value=0.2, unit='mol')],
    name='LDMC_LIPF6')

densities = {'[Li+].F[P-](F)(F)(F)(F)F':2.84,'CCOC(=O)OC':0.997,'CC1COC(=O)O1':1.205,'COC(=O)OC':1.073,'unit':'g/cm**3'}


with open('/Users/helgestein/PycharmProjects/finale/schemas_export/chemical.json', 'w') as f:
    f.write(schemas_pydantic.Chemical.schema_json(indent=2))

with open('/Users/helgestein/PycharmProjects/finale/schemas_export/chemical_example.json', 'w') as f:
    f.write(dmc.json(indent=2))


with open('/Users/helgestein/PycharmProjects/finale/schemas_export/compound.json', 'w') as f:
    f.write(schemas_pydantic.Compound.schema_json(indent=2))

with open('/Users/helgestein/PycharmProjects/finale/schemas_export/compound_pure_example.json', 'w') as f:
    f.write(dmc_compound.json(indent=2))

with open('/Users/helgestein/PycharmProjects/finale/schemas_export/compound_mix_example.json', 'w') as f:
    f.write(lipf6_dmc.json(indent=2))

A = schemas_pydantic.Compound(chemicals=[schemas_pydantic.Chemical(smiles='COC(=O)OC',name='DMC',reference='DMC_Elyte_2020'),
                                  schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F',name='LiPF6',reference='LiPF6_Elyte_2020')],
                       amounts=[schemas_pydantic.Amount(value=0.5,unit='mol'),schemas_pydantic.Amount(value=0.1,unit='mol')],
                       name='LiPF6_salt_in_DMC_5:1')

B = schemas_pydantic.Compound(chemicals=[schemas_pydantic.Chemical(smiles='CC1COC(=O)O1', name='PC', reference='PC_ELyte_2020'),
                        schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')],
             amounts=[schemas_pydantic.Amount(value=0.5, unit='mol'), schemas_pydantic.Amount(value=0.1, unit='mol')],
             name='LiPF6_salt_in_PC_5:1')

with open('/Users/helgestein/PycharmProjects/finale/schemas_export/compound_A_example.json', 'w') as f:
    f.write(A.json(indent=2))

with open('/Users/helgestein/PycharmProjects/finale/schemas_export/compound_B_example.json', 'w') as f:
    f.write(A.json(indent=2))

form = schemas_pydantic.Formulation(compounds=[A,B], ratio=[0.4,0.6], ratio_method='volumetric')

with open('/Users/helgestein/PycharmProjects/finale/schemas_export/formulation.json', 'w') as f:
    f.write(schemas_pydantic.Formulation.schema_json(indent=2))

with open('/Users/helgestein/PycharmProjects/finale/schemas_export/formulation_example_two_compounds.json', 'w') as f:
    f.write(form.json(indent=2))

with open('/Users/helgestein/PycharmProjects/finale/schemas_export/formulation_example_one_compound_one_chemical.json', 'w') as f:
    smf = schemas_pydantic.Formulation(compounds=[dmc_compound], ratio=[1], ratio_method='volumetric')
    f.write(smf.json(indent=2))

with open('/Users/helgestein/PycharmProjects/finale/schemas_export/temperature.json', 'w') as f:
    f.write(schemas_pydantic.Temperature.schema_json(indent=2))

with open('/Users/helgestein/PycharmProjects/finale/schemas_export/origin.json', 'w') as f:
    f.write(schemas_pydantic.Origin.schema_json(indent=2))

temp_1 = schemas_pydantic.Temperature(value=380,unit='K')

with open('/Users/helgestein/PycharmProjects/finale/schemas_export/temperature_example.json', 'w') as f:
    f.write(temp_1.json(indent=2))


orig_1 = schemas_pydantic.Origin(origin='simulation',what='density')
with open('/Users/helgestein/PycharmProjects/finale/schemas_export/origin_example.json', 'w') as f:
    f.write(orig_1.json(indent=2))

meas_1 = schemas_pydantic.Measurement(formulation=form, temperature=temp_1, pending=True, kind=orig_1)

with open('/Users/helgestein/PycharmProjects/finale/schemas_export/measurement.json', 'w') as f:
    f.write(schemas_pydantic.Measurement.schema_json(indent=2))

with open('/Users/helgestein/PycharmProjects/finale/schemas_export/measurement_request_example.json', 'w') as f:
    f.write(schemas_pydantic.Measurement.schema_json(indent=2))

fom_1 = schemas_pydantic.FomData(value=3,unit="g/cm**3",origin=orig_1,measurement_id='fancy_density_simulation_12345678',name='Density')

with open('/Users/helgestein/PycharmProjects/finale/schemas_export/fomdata.json', 'w') as f:
    f.write(schemas_pydantic.FomData.schema_json(indent=2))

with open('/Users/helgestein/PycharmProjects/finale/schemas_export/fomdata_example.json', 'w') as f:
    f.write(fom_1.json(indent=2))

meas = schemas_pydantic.Measurement(formulation=form, temperature=temp_1, pending=False, fom_data=fom_1, kind=orig_1)

with open('/Users/helgestein/PycharmProjects/finale/schemas_export/measurement_post_example.json', 'w') as f:
    f.write(meas.json(indent=2))
