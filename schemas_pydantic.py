from typing import List,Optional
from pydantic import BaseModel, validator, Field
#from uuid import uuid4, UUID
from enum import Enum

class OriginEnum(str, Enum):
    experiment = 'experiment'
    simulation = 'simulation'

class Origin(BaseModel):
    origin: OriginEnum

class FOMEnum(str, Enum):
    density = 'density'
    viscosity = 'viscosity'

class FOM(BaseModel):
    origin: OriginEnum

class Chemical(BaseModel):
    """This defines a chemical

    Every chemical needs a SMILES and a name like DMC => COC(=O)OC
    A reference is an optional thing like "Vile 211003-Vial2-DMC"
    Example:
        Chemical(smiles='COC(=O)OC',name='DMC',reference='DMC_Elyte_2020')
    """
    smiles: str# = Field(...)
    name: str# = Field(...)
    reference: str = ''
    # TODO: add smiles check?
    # TODO: add check if chemicals are allowed?

class Temperature(BaseModel):
    """Temperature in Kelvin
    Example:
        Temperature(value=380,unit='K')
    """
    value: float# = Field(...)
    unit: str# = Field(...)

    @validator('value')
    def t_value_validator(cls, v):
        if not v > 0:
            raise ValueError('Temperature must be >0K')
        return v

    @validator('unit')
    def t_unit_validator(cls, v):
        if v != 'K':
            raise ValueError('Temperature unit must be K')
        return v.title()

class Amount(BaseModel):
    """We store amount in units of mole TODO: Maybe recalc to mol?

    Amount is stored as a tuple like object i.e. how much and of what unit
    Currently we only do mol
    Example: Amount(value=0.001,unit='mol')
    """
    value: float# = Field(...)
    unit: str# = Field(...)

    @validator('unit')
    def amount_unit_validator(cls, v):
        if v != 'mol':
            raise ValueError('Unit must be mol')
        return v.title()

class Compound(BaseModel):
    """Formulations are lists of Compound which are lists of chemicals

    A Compound can be made up of one or more chemicals of amounts
    This is needed as some electrolyte chemicals are not liquid in their pure form at RT
    Example:
        Compound(chemicals=[Chemical(smiles='COC(=O)OC',name='DMC',reference='DMC_Elyte_2020'),
                                  Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F',name='LiPF6',reference='LiPF6_Elyte_2020')],
                       amounts=[Amount(value=0.5,unit='mol'),Amount(value=0.1,unit='mol')],
                       name='LiPF6_salt_in_DMC_5:1')
    """
    chemicals: List[Chemical] = Field(...)  # can be a list of len>=1
    amounts: List[Amount] = Field(...)
    name: str# = Field(...)
    # TODO: Validate that len matches

class Formulation(BaseModel):
    """A Formulation is a ratio mix of different compounds

    Example:
    A = Compound(chemicals=[Chemical(smiles='COC(=O)OC',name='DMC',reference='DMC_ELyte_2020'),
                                  Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F',name='LiPF6',reference='LiPF6_Elyte_2020')],
                       amounts=[Amount(value=0.5,unit='mol'),Amount(value=0.1,unit='mol')],
                       name='LiPF6_salt_in_DMC_5:1')
    B = Compound(chemicals=[Chemical(smiles='CC1COC(=O)O1',name='PC',reference='PC_ELyte_2020'),
                                  Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F',name='LiPF6',reference='LiPF6_Elyte_2020')],
                       amounts=[Amount(value=0.5,unit='mol'),Amount(value=0.1,unit='mol')],
                       name='LiPF6_salt_in_PC_5:1')
    form_1 = Formulation(compounds=[A,B],ratio=[3,1])
    """
    # A formulation can consist
    compounds: List[Compound] = Field(...)
    ratio: List[float] = Field(...)
    # TODO: Validate that len matches
    # TODO: Tinker about ratios and ambiguities

class RawData(BaseModel):
    """This is a wrapper for arbitrary dict type data

    TODO: This could potentially be improved such that one is not able to upload garbage
    """
    data: dict# = []
    description: str# = []

class FomData(BaseModel):
    """This is a wrapper for figure of merit (FOM) i.e. scalar data

    Example:
        fom_1 = FomData(value=3,unit="g/cm**3",origin="experiment")
    """
    value: float# = Field(...)
    unit: str# = Field(...)
    name: str
    origin: Origin# = Field(...)

class Measurement(BaseModel):
    """A Measurement is done on a Formulation and contains data

    Example:
    A = Compound(chemicals=[Chemical(smiles='COC(=O)OC',name='DMC',reference='DMC_ELyte_2020'),
                                  Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F',name='LiPF6',reference='LiPF6_Elyte_2020')],
                       amounts=[Amount(value=0.5,unit='mol'),Amount(value=0.1,unit='mol')],
                       name='LiPF6_salt_in_DMC_5:1')
    B = Compound(chemicals=[Chemical(smiles='CC1COC(=O)O1',name='PC',reference='PC_ELyte_2020'),
                                  Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F',name='LiPF6',reference='LiPF6_Elyte_2020')],
                       amounts=[Amount(value=0.5,unit='mol'),Amount(value=0.1,unit='mol')],
                       name='LiPF6_salt_in_PC_5:1')
    form_1 = Formulation(compounds=[A,B],ratio=[3,1])

    temp_1 = Temperature(unit='K',value=380)

    fom_1 = FomData(value=3,unit="g/cm**3",origin="experiment")

    meas_1 = Measurement(formulation=form_1, temperature=temp_1,pending=True,fom_data=fom_1)

    """
    #ID: UUID = Field(default_factory=uuid4)
    formulation: Formulation# = Field(...)
    temperature: Temperature# = Field(...)
    pending: bool# = True

    raw_data: Optional[RawData]# = []
    fom_data: Optional[FomData]# = []
    # TODO: if pending True raw and fom may not be set!
