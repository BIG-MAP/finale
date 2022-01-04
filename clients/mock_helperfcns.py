import os,sys
rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(rootp, 'config'))
sys.path.append(os.path.join(rootp, 'db'))
from typing import List

import config
from db import schemas_pydantic

def do_experiment(measurement: schemas_pydantic.Measurement):

    pass

def do_simulation(measurement: schemas_pydantic.Measurement):
    pass

def assembleXY(measurements: List[schemas_pydantic.Measurement],conversions: dict=None):
    """
    This function will return a XY style dictionary with explanations. It is custom programmed as a helper
    to return a dictionary containing the molar amounts as X and the density as Y. Adjust to your needs.

    about conversions:
    expecting conversions to contain a conversion between the ratio method and amount
    there is no checking of this hence it is you own best interest to do this.
    Example: if ratio_method is volumetric and amounts is in mol you need a molar volume conversion (mol/V)
    """
