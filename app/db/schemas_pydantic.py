from typing import List, Optional
from pydantic import BaseModel, validator, Field
from enum import Enum

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    level: Optional[int] = 0


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserInDB(User):
    hashed_password: str


class Message(BaseModel):
    message: str
    id: int


class OriginEnum(str, Enum):
    experiment = 'experiment'
    simulation = 'simulation'
    test = 'test'


class ok(BaseModel):
    typeob: str


class FomEnum(str, Enum):
    density = 'density'
    viscosity = 'viscosity'
    conductivity = 'conductivity'
    aniondiffusion = 'aniondiffusion'
    cationdiffusion = 'cationdiffusion'
    vectorial = 'vectorial'


class Origin(BaseModel):
    origin: OriginEnum
    what: Optional[FomEnum]


class Ratio(str, Enum):
    molar = 'molar'
    molal = 'molal'
    other = 'other'


class FOM(BaseModel):
    origin: OriginEnum


class Chemical(BaseModel):
    """This defines a chemical

    Every chemical needs a SMILES and a name like DMC => COC(=O)OC
    A reference is an optional thing like "Vile 211003-Vial2-DMC"
    Example:
    dmc = schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020')
    """
    smiles: str  # = Field(...)
    name: str  # = Field(...)
    reference: str = ''
    # TODO: add smiles check?
    # TODO: add check if chemicals are allowed?


class Temperature(BaseModel):
    """Temperature in Kelvin
    Example:
        Temperature(value=380,unit='K')
    """
    value: float  # = Field(...)
    unit: str  # = Field(...)

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
    value: float  # = Field(...)
    unit: str  # = Field(...)

    @validator('unit')
    def amount_unit_validator(cls, v):
        if not v in ['mol', 'Mol','at.-%','mol.-%']:
            raise ValueError('Unit must be mol or other')
        return v.title()

class ChemRange(BaseModel):
    """We store amount in units of mole TODO: Maybe recalc to mol?

    Amount is stored as a tuple like object i.e. how much and of what unit
    Currently we only do mol
    Example: Amount(value=0.001,unit='mol')
    """
    min_value: float  # = Field(...)
    max_value: float  # = Field(...)
    chemical: Chemical
    unit: str  # = Field(...)

    @validator('unit')
    def amount_unit_validator(cls, v):
        if not v in ['mol', 'Mol','at.-%','mol.-%']:
            raise ValueError('Unit must be mol or other')
        return v.title()



#legacy
class Compound(BaseModel):
    """Legacy Schema mostly used by experimentalists: Formulations are lists of Compound which are lists of chemicals

    A Compound can be made up of one or more chemicals of amounts
    This is needed as some electrolyte chemicals are not liquid in their pure form at RT
    Example:
        dmc_compound = schemas_pydantic.Compound(chemicals=[
    schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020')],
    amounts=[schemas_pydantic.Amount(value=1.0, unit='mol')],
    name='DMC')
    """
    chemicals: List[Chemical] = Field(...)  # breaking change as from now on users need to specify a compound with only one chemical
    amounts: List[Amount] = Field(...)
    name: str  # = Field(...)
    # TODO: Validate that len matches


class Agent(BaseModel):
    """This stores the range accesibile by a machine
    """
    online: bool #is it online
    kind: OriginEnum #theory or experiment
    chemicals: List[Chemical]
    ranges: List[ChemRange]
    name: str
    compounds: Optional[List[Compound]]


class Formulation(BaseModel):
    """A Formulation is a ratio mix of different compounds

    Example:
    form = schemas_pydantic.Formulation(chemicals=[schemas_pydantic.Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020'),
                                                schemas_pydantic.Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')],
    amounts=[schemas_pydantic.Amount(value=1.0, unit='mol'),schemas_pydantic.Amount(value=0.1, unit='mol')],
    ratio_method='molal')
    """
    # A formulation can consist
    chemicals: List[Chemical] = Field(...)
    amounts: List[Amount] = Field(...)
    ratio_method: Ratio
    # TODO: Validate that len matches
    # TODO: Tinker about ratios and ambiguities


class FomData(BaseModel):
    """This is a wrapper for figure of merit (FOM) i.e. scalar data

    Example:
    data = schemas_pydantic.FomData(values=[1.23],unit='g/cm**2',dim=1,
                                    name='density',origin=orig,internalReference='aTest',
                                    fail=False, message='My Message', rating=1)

    data_nd = schemas_pydantic.FomData(values=[1.23,234,12,13,56,26],unit='g/cm**2',dim=6,
                                    name='vectorial',origin=orig,internalReference='aTest',
                                    fail=False, message='My Message', rating=1)
    """
    values: List[float] #breaking change as now you'd have to give it [[1.23]]
    unit: str = Field(...)
    dim: int = Field(...)
    name: FomEnum = Field(...)
    origin: Origin = Field(...)
    internalReference: str = Field(...)
    fail: Optional[bool]
    message: Optional[str]
    rating: Optional[int]


class Measurement(BaseModel):
    """A Measurement is done on a Formulation and contains data

    Example:
    meas = schemas_pydantic.Measurement(formulation=form,temperature=temp,pending=False,fom_data=[data],kind=orig)


    """
    # ID: UUID = Field(default_factory=uuid4)
    formulation: Formulation  # = Field(...)
    temperature: Temperature  # = Field(...)
    pending: bool  # = True
    #processing: Optional[bool] TODO: in later update should also keep track on tah and need to update this
    fom_data: List[Optional[FomData]]  # = []
    kind: Origin
    # TODO: if pending True raw and fom may not be set!


class Message(BaseModel):
    message: dict = None
