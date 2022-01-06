import os,sys
import time

rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
#rootp += "/fastALE/"

sys.path.append(os.path.join(rootp, 'config'))
sys.path.append(os.path.join(rootp, 'clients'))
# terminal run: rootp += "/fastALE/"
import config
from db import schemas_pydantic
from helperfcns import *
import requests
import time
filter_ingest = "experiment"
request_type = "experiment"

posted_id = "no_posted_id_yet"

while True:
    #check if we have new measurements
    pending_measurements = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending",
                           params={'fom_name':'Density'}).json()
    if not posted_id in pending_measurements.keys():
        #getting all FOM
        all_measurements = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_fom",
                                        params={'fom_name': 'Density'}).json()
        #get a XY style table
        measurements = {k:schemas_pydantic.Measurement(**m) for k,m in all_measurements.items()}
        if filter_ingest == 'experiment':
            measurements = {k:m for k,m in measurements.items() if m.fom_data.origin.origin.value=='experiment'}
        if filter_ingest == 'simulation':
            measurements = {k:m for k,m in measurements.items() if m.fom_data.origin.origin.value=='simulation'}

        if len(measurements.keys())==0:
            break

        xyz = assembleXY(measurements, conversions = config.densities, fom_name = 'Density')
        X,y = xyz['X'],xyz['y']

        #ask the optimizer what to try
        return_all = False
        try_chem_ratios = simple_rf_optimizer(X,y,return_all=return_all)

        #translate this result into a formulation
        #warning: It may very well be possibile that the suggested chemical composition is not attainable
        #with the used compounds compositions. Right now I oped to just go for the closest one. An alternative
        #is to take the one with an error lower than the threshold...
        if return_all:
            errs = []
            for chem_ratio in try_chem_ratios:
                target = {chem_name:amnt for amnt,chem_name in zip(chem_ratio,xyz['chemicals'])}
                ratios,err = get_formulation(target,conversions=config.densities)
                errs.append(err)
        else:
            target = {chem_name: amnt for amnt, chem_name in zip(try_chem_ratios, xyz['chemicals'])}
            ratios, err = get_formulation(target)
            errs = [err]
            print(f"Error of formulation: {err}")

        #post the suggestion to the broker server
        #arrange the compounds right
        compounds = get_compounds()
        ratios_arranged = [ratios[c] for c in [cn.name for cn in compounds]]

        form_post = schemas_pydantic.Formulation(compounds=compounds, ratio=ratios_arranged, ratio_method='volumetric')
        temp = schemas_pydantic.Temperature(value=298.15, unit='K')
        if request_type == "experiment":
            orig = schemas_pydantic.Origin(origin='experiment', what='Density')
        if request_type == "simulation":
            orig = schemas_pydantic.Origin(origin='simulation', what='Density')
        meas_request = schemas_pydantic.Measurement(formulation=form_post, temperature=temp, pending=True, kind=orig)
        ans = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement",
                                 data=meas_request.json()).json()
        posted_id = ans['id']
        print(ans)
    else:
        time.sleep(config.sleeptime)
