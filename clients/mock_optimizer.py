import os,sys
rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(rootp, 'config'))
sys.path.append(os.path.join(rootp, 'clients'))

from config import config
from db import schemas_pydantic
from mock_helperfcns import assembleXY
import requests

while True:
    #getting all FOM
    all_measurements = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_fom",
                                    params={'fom_name': 'Density'}).json()
    #getting a XY style table
    measurements = {k:schemas_pydantic.Measurement(**m) for k,m in all_measurements.items()}
    xyz = assembleXY(measurements, conversions = None, fom_name = 'Density')
    X,y = xyz['X'],xyz['y']

