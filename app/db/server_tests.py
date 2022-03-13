import requests
import sys
sys.path.extend(['./app/db'])

import schemas_pydantic
host = 'localhost'
port = '13371'

def authenticate(user,pw):
    token_response = requests.post(f"http://{host}:{port}/token", data={"username": user, "password": pw, "grant_type": "password"},
                                   headers={"content-type": "application/x-www-form-urlencoded"})

    token_response = token_response.json()
    token = token_response['access_token']

    auth_header = {'Authorization': 'Bearer {}'.format(token)}

    return auth_header

auth_header = authenticate("kit", "KIT_huipuischui_23")

#test chemical
dmc = schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020')
ans_ = requests.post(f"http://{host}:{port}/api/broker/post/chemical",
                     data=dmc.json(),headers=auth_header).json()

#test compound
dmc_compound = schemas_pydantic.Compound(chemicals=[schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020')],
    amounts=[schemas_pydantic.Amount(value=1.0, unit='mol')],name='DMC')
ans_ = requests.post(f"http://{host}:{port}/api/broker/post/compound",data=dmc_compound.json(),headers=auth_header).json()

#test compound complex
mixed_compound = schemas_pydantic.Compound(chemicals=[
    schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020'),
    schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')],
    amounts=[schemas_pydantic.Amount(value=1.0, unit='mol'), schemas_pydantic.Amount(value=0.2, unit='mol')],
    name='LDMC_LIPF6')

ans_ = requests.post(f"http://{host}:{port}/api/broker/post/compound",data=mixed_compound.json(),headers=auth_header).json()


#test measurement
form = schemas_pydantic.Formulation(chemicals=[schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020'),
                                                schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')],
    amounts=[schemas_pydantic.Amount(value=1.0, unit='mol'),schemas_pydantic.Amount(value=0.1, unit='mol')],
    ratio_method='molal')
orig = schemas_pydantic.Origin(origin='simulation', what='density')
data = schemas_pydantic.FomData(values=[1.23],unit='g/cm**2',dim=1,
                                name='density',origin=orig,internalReference='aTest',
                                fail=False, message='My Message', rating=1)
data_nd = schemas_pydantic.FomData(values=[1.23,234,12,13,56,26],unit='g/cm**2',dim=6,
                                name='vectorial',origin=orig,internalReference='aTest',
                                fail=False, message='My Message', rating=1)
temp = schemas_pydantic.Temperature(value=300,unit='K')
meas = schemas_pydantic.Measurement(formulation=form,temperature=temp,pending=False,fom_data=[data_nd],kind=orig)

ans_ = requests.post(f"http://{host}:{port}/api/broker/post/measurement",data=meas.json(),headers=auth_header)
ans_.json()