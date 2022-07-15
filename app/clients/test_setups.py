import sys , os
sys.path.append(os.path.join(sys.path[0], '..'))
from schemas_pydantic import *
import config.config as config 
# Creating a test setup for an experiment

temperature_test = Temperature(value=380, unit='K')
compound_1 = Chemical(smiles='CC1COC(=O)O1', name='PC', reference='PC_ELyte_2020')
compound_2 = Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020')
                            
formulation_test = Formulation(chemicals=[compound_1, compound_2], 
    amounts=[Amount(value=1,unit='mol'),Amount(value=1,unit='mol')], 
    ratio_method='molal')

store_to_archive = ArchiveStorage(upload=True, 
    append=False, existingRecord='')

test_measurement = Measurement(
    formulation=formulation_test,
    temperature=temperature_test,
    pending=True,
    fom_data=[],
    kind=Origin(origin='experiment',what='density'),
    store_to_archive = store_to_archive)


       




