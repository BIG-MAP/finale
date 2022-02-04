import os,sys
rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(rootp, 'db'))
from app.db import schemas_pydantic

#values
reset: bool = True
db_file: str = f'session_testing.db'
MAX_D = 7
host = "stein.hiu-batteries.de"
port = 49157

SECRET_KEY = "dcf832f0ec6a80dc36afd95422f0bb1f1c964d916a8c0d29b127d3246e4c88a6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24*7

sleeptime = 5

ratio_threshold = 0.01

ratio_threshold = 0.01

## Actual  compounds
LiPF6_EC_DMC = schemas_pydantic.Compound(chemicals=[
    schemas_pydantic.Chemical(smiles='C1COC(=O)O1', name='EC', reference='EC_Elyte_2020'),
    schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020'),
    schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')],
    amounts=[schemas_pydantic.Amount(value=0.47, unit='mol.-%'),
    schemas_pydantic.Amount(value=0.46, unit='mol.-%'),
    schemas_pydantic.Amount(value=0.07, unit='mol.-%')],
    name='LiPF6_salt_in_EC_DMC_1:1')

EC_DMC = schemas_pydantic.Compound(chemicals=[
    schemas_pydantic.Chemical(smiles='C1COC(=O)O1', name='EC', reference='EC_Elyte_2020'),
    schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020')],
    amounts=[schemas_pydantic.Amount(value=0.51, unit='mol.-%'),
    schemas_pydantic.Amount(value=0.49, unit='mol.-%')],
    name='EC_DMC_1:1')

LiPF6_EC_EMC = schemas_pydantic.Compound(chemicals=[
    schemas_pydantic.Chemical(smiles='C1COC(=O)O1', name='EC', reference='EC_Elyte_2020'),
    schemas_pydantic.Chemical(smiles='CCOC(=O)OC', name='EMC', reference='EMC_ELyte_2020'),
    schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')],
    amounts=[schemas_pydantic.Amount(value=0.31, unit='mol.-%'),
    schemas_pydantic.Amount(value=0.60, unit='mol.-%'),
    schemas_pydantic.Amount(value=0.09, unit='mol.-%')],
    name='LiPF6_salt_in_EC_EMC_3:7')

EC_EMC = schemas_pydantic.Compound(chemicals=[
    schemas_pydantic.Chemical(smiles='C1COC(=O)O1', name='EC', reference='EC_Elyte_2020'),
    schemas_pydantic.Chemical(smiles='CCOC(=O)OC', name='EMC', reference='EMC_ELyte_2020')],
    amounts=[schemas_pydantic.Amount(value=0.34, unit='mol.-%'),
    schemas_pydantic.Amount(value=0.66, unit='mol.-%')],
    name='EC_EMC_3:7')

densities = {'[Li+].F[P-](F)(F)(F)(F)F':2.84,'CCOC(=O)OC':0.997,'CC1COC(=O)O1':1.205,'COC(=O)OC':1.073,'unit':'g/cm**3'}
