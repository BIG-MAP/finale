import os,sys
rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(rootp, 'config'))
sys.path.append(os.path.join(rootp, 'db'))

from config import config
from db import schemas_pydantic
from mock_helperfcns import do_experiment
import requests

#getting all FOM
fom_dict = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_fom", params={'fom_name': 'Density'}).json()
