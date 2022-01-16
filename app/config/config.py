import os,sys
rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(rootp, 'db'))
from app.db import schemas_pydantic

#values
reset: bool = True
db_file: str = f'session_a.db'
MAX_D = 7
host = "localhost"
port = 13371

SECRET_KEY = "dcf832f0ec6a80dc36afd95422f0bb1f1c964d916a8c0d29b127d3246e4c88a6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24*7

sleeptime = 5

ratio_threshold = 0.01

A = schemas_pydantic.Compound(chemicals=[
    schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020'),
    schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')],
    amounts=[schemas_pydantic.Amount(value=0.5, unit='mol'),
             schemas_pydantic.Amount(value=0.4, unit='mol')],
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

D = schemas_pydantic.Compound(chemicals=[
    schemas_pydantic.Chemical(smiles='FC1COC(=O)O1', name='FEC', reference='FEC_ELyte_2021')],
    amounts=[schemas_pydantic.Amount(value=0.5, unit='mol'), schemas_pydantic.Amount(value=0.1, unit='mol')],
    name='LiPF6_salt_in_PC_5:1')

E = schemas_pydantic.Compound(chemicals=[
    schemas_pydantic.Chemical(smiles='CC#N', name='ACN', reference='Acetonitrile_Sigma_2021')],
    amounts=[schemas_pydantic.Amount(value=0.5, unit='mol'), schemas_pydantic.Amount(value=0.1, unit='mol')],
    name='LiPF6_salt_in_PC_5:1')







dmc = schemas_pydantic.Compound(chemicals=[
    schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020')],
    amounts=[schemas_pydantic.Amount(value=1.0, unit='mol')],
    name='DMC')

pc = schemas_pydantic.Compound(chemicals=[
    schemas_pydantic.Chemical(smiles='CC1COC(=O)O1', name='PC', reference='PC_ELyte_2020')],
    amounts=[schemas_pydantic.Amount(value=1.0, unit='mol')],
    name='PC')

emc = schemas_pydantic.Compound(chemicals=[
    schemas_pydantic.Chemical(smiles='CCOC(=O)OC', name='EMC', reference='EMC_ELyte_2020')],
    amounts=[schemas_pydantic.Amount(value=1.0, unit='mol')],
    name='EMC')

lipf6 = schemas_pydantic.Compound(chemicals=[
    schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020'),
    schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')],
    amounts=[schemas_pydantic.Amount(value=1.0, unit='mol'), schemas_pydantic.Amount(value=0.2, unit='mol')],
    name='LDMC_LIPF6')

densities = {'[Li+].F[P-](F)(F)(F)(F)F':2.84,'CCOC(=O)OC':0.997,'CC1COC(=O)O1':1.205,'COC(=O)OC':1.073,'unit':'g/cm**3'}
