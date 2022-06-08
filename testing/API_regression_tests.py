import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append("\\".join([str(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "app"]))
sys.path.append("\\".join([str(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "app\\clients"]))
sys.path.append("\\".join([str(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "app\\config"]))
sys.path.append("\\".join([str(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "db"]))
sys.path.append(r"C:\Users\Public\Documents\ASAB\ASAB_experiments\experiments\Hackathon_V1")
import requests
from db import schemas_pydantic

### Setup: Specify server to test against
from config import config
from app.broker_server import app
from app.clients import helperfcns_externalDoExperiment as helpfuncs
from Hackathon_V1 import config_Hackathon


usr = "helge"
pw = "1234"

# TODO: Adjust measurements according to new schemas once the new schemas are operable.

##################################################################################################
#                                          General tests                                         #
##################################################################################################


## Basic authentication (DTU, KIT, 3DS to look up username / password) 
def test_authenticate_user():
# - post username + password
    res = requests.post(f"http://{config.host}:{config.port}/token",
                                   data={"username": usr, "password": pw, "grant_type": "password"},
                                   headers={"content-type": "application/x-www-form-urlencoded"})
# - verify response OK
    assert res.status_code == 200
# - verify presence of access tokens
    assert res.json()['access_token'] != None


auth_header = helpfuncs.authenticate(usr, pw)

# Post compounds? (decide later)


## Get all compounds
def test_get_all_compounds():
# - post request
    res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_compounds", headers=auth_header)
    print(type(res.json()))
# - verify response ok 
    assert res.status_code == 200
# - verify response contains list <- shall it really be a list?
    assert type(res.json()) == dict
# - 3DS: verify compounds can be associated with formulas, structures & force fields
# - KIT: verify that compounds are available, to be discussed with Helge?
    for _key, val in res.json().items():
        assert val['name'] in config_Hackathon.config['CetoniDevice']['compoundsReservoirs'].keys()


## Post chemicals? (decide later)


## Get all chemicals
def test_get_all_chemicals():
# - post request
    res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_chemicals", headers=auth_header)
# - verify response ok
    assert res.status_code == 200
# - verify response contains list <- shall it really be a list?
    assert type(res.json()) == dict
# - 3DS: verify chemicals can be associated with formulas, structures & force fields
# - KIT: verify that chemicals are available, to be discussed with Helge? <- ASAB does not consider chemicals at the moment



##################################################################################################
#                              Test entire measurement lifecycle                                 #
##################################################################################################

measurementsDict = {"singleFOMmeasurement": {"id_request": "0", "id_measurement": "0"},
                    "duplicateSingleFOMmeasurement": {"id_request": "0", "id_measurement": "0"},
                    "multiFOMmeasurement": {"id_request": "0", "id_measurement": []},
                    }#"twoFOMmeasurement":  {"id_request": "0", "id_measurement": "0"},
                    #"failedFOMmeasurement":  {"id_request": "0", "id_measurement": "0"}}



'''----------------------------------------------------------
Test measurement lifecycle with single FOM result
-------------------------------------------------------------'''

''' Dummy FOM '''
fom = "Density"

''' Dummy origin '''
orig = "experiment"

''' Dummy measurement '''
singleFOMmeas = schemas_pydantic.Measurement(
        formulation = schemas_pydantic.Formulation(compounds=[config.LiPF6_EC_EMC, config.LiPF6_EC_DMC], ratio=[0.4, 0.6], ratio_method='volumetric'),
        temperature = schemas_pydantic.Temperature(value=293.15, unit='K'),
        pending = True,
        kind = schemas_pydantic.Origin(origin=orig, what=fom))

''' Dummy result '''
units = {"Density": "g/cm**3", "Viscosity": "mPa*s"}
post_singleFOMmeas = schemas_pydantic.Measurement(
        formulation = singleFOMmeas.formulation,
        temperature = singleFOMmeas.temperature,
        pending = False,
        fom_data = schemas_pydantic.FomData(value = 42.0,
            unit = units[singleFOMmeas.kind.what],
            origin = singleFOMmeas.kind,
            measurement_id = "123456789",
            name = singleFOMmeas.kind.what),
        kind = singleFOMmeas.kind)

## Get pending measurement requests - 1
def test_singleFOM_get_pending1():
# - post request
    res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending", params={'fom_name':fom}, headers=auth_header)
# - verify response OK
    assert res.status_code == 200

## Post measurement requests
def test_singleFOM_request_meas():
# - post request (one or more of simulation / experiment)
    res = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement", data=singleFOMmeas.json(), headers=auth_header)
# - verify response OK
    assert res.status_code == 200
# - verify response contains request ID (to be verified?) with associated time stamp <- test for timestamp pending
    measurementsDict["singleFOMmeasurement"]["id_request"] = res.json()["id"]
    assert res.json()["id"] != None

## Get pending measurement requests – 2
def test_singleFOM_get_pending2():
# - post request for all pending measurements
    res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending", params={'fom_name':fom}, headers=auth_header)
# - verify response OK
    assert res.status_code == 200
# - verify response contains request ID with the same parameters as requested above and with associated time stamp <- test for timestamp pending
    assert measurementsDict["singleFOMmeasurement"]["id_request"] in res.json().keys()
    assert res.json()[measurementsDict["singleFOMmeasurement"]["id_request"]]["formulation"] == dict(singleFOMmeas.formulation)
    assert res.json()[measurementsDict["singleFOMmeasurement"]["id_request"]]["temperature"] == dict(singleFOMmeas.temperature)
    assert res.json()[measurementsDict["singleFOMmeasurement"]["id_request"]]["pending"] == singleFOMmeas.pending
    assert res.json()[measurementsDict["singleFOMmeasurement"]["id_request"]]["kind"] == dict(singleFOMmeas.kind)

## Post measurement results
def test_singleFOM_post_measurement():
# - post result with request ID and user-provided measurement_ID
    res = requests.post(f"http://{config.host}:{config.port}/api/broker/post/measurement",
        data=post_singleFOMmeas.json(),params={'request_id':measurementsDict["singleFOMmeasurement"]["id_request"]},headers=auth_header)
# - verify response OK
    assert res.status_code == 200
# - verify response contains server-provided ID_measurement with associated time stamp <- test for timestamp pending
    assert res.json()["id_measurement"] != None
    measurementsDict["singleFOMmeasurement"]["id_measurement"] = res.json()["id_measurement"]
    assert res.json()["id_request"] == measurementsDict["singleFOMmeasurement"]["id_request"] #<- additional test for request ID

## Get pending measurement requests - 3
def test_singleFOM_get_pending3():
# - post request for all pending measurements
    res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending", params={'fom_name':fom}, headers=auth_header)
# - verify response OK
    assert res.status_code == 200
# - verify response does NOT contain request ID
    assert measurementsDict["singleFOMmeasurement"]["id_request"] not in res.json().keys()

## Get all FOM results
def test_singleFOM_all_fom():
# - post request for all FOMs
    res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_fom", params={'fom_name': fom},headers=auth_header)
# - verify response OK
    assert res.status_code == 200
# - verify response contains server-provided ID_measurement with all FOM’s posted previously and time stamp(s) <- test for timestamp pending
    assert measurementsDict["singleFOMmeasurement"]["id_measurement"] in res.json().keys()
    assert res.json()[measurementsDict["singleFOMmeasurement"]["id_measurement"]]["fom_data"] == dict(post_singleFOMmeas.fom_data)



'''----------------------------------------------------------
Test measurement lifecycle with duplicated single FOM result
-------------------------------------------------------------'''

''' Dummy result '''
units = {"Density": "g/cm**3", "Viscosity": "mPa*s"}
post_duplicateSingleFOMmeas = schemas_pydantic.Measurement(
        formulation = singleFOMmeas.formulation,
        temperature = singleFOMmeas.temperature,
        pending = False,
        fom_data = schemas_pydantic.FomData(value = 21.0,
            unit = units[singleFOMmeas.kind.what],
            origin = singleFOMmeas.kind,
            measurement_id = "987654321",
            name = singleFOMmeas.kind.what),
        kind = singleFOMmeas.kind)

## Get pending measurement requests - 1
def test_duplicatedSingleFOM_get_pending1():
# - post request
    res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending", params={'fom_name':fom}, headers=auth_header)
# - verify response OK
    assert res.status_code == 200

## Post measurement requests
def test_duplicatedSingleFOM_request_meas():
# - post request (one or more of simulation / experiment)
    res = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement", data=singleFOMmeas.json(), headers=auth_header)
# - verify response OK
    assert res.status_code == 200
# - verify response contains request ID (to be verified?) with associated time stamp <- test for timestamp pending
    measurementsDict["duplicateSingleFOMmeasurement"]["id_request"] = res.json()["id"]
    assert res.json()["id"] != None

## Get pending measurement requests – 2
def test_duplicatedSingleFOM_get_pending2():
# - post request for all pending measurements
    res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending", params={'fom_name':fom}, headers=auth_header)
# - verify response OK
    assert res.status_code == 200
# - verify response contains request ID with the same parameters as requested above and with associated time stamp <- test for timestamp pending
    assert measurementsDict["duplicateSingleFOMmeasurement"]["id_request"] in res.json().keys()
    assert res.json()[measurementsDict["duplicateSingleFOMmeasurement"]["id_request"]]["formulation"] == dict(singleFOMmeas.formulation)
    assert res.json()[measurementsDict["duplicateSingleFOMmeasurement"]["id_request"]]["temperature"] == dict(singleFOMmeas.temperature)
    assert res.json()[measurementsDict["duplicateSingleFOMmeasurement"]["id_request"]]["pending"] == singleFOMmeas.pending
    assert res.json()[measurementsDict["duplicateSingleFOMmeasurement"]["id_request"]]["kind"] == dict(singleFOMmeas.kind)

## Post measurement results
def test_duplicatedSingleFOM_post_measurement():
# - post result with request ID and user-provided measurement_ID
    res = requests.post(f"http://{config.host}:{config.port}/api/broker/post/measurement",
        data=post_duplicateSingleFOMmeas.json(),params={'request_id':measurementsDict["duplicateSingleFOMmeasurement"]["id_request"]},headers=auth_header)
# - verify response OK
    assert res.status_code == 200
# - verify response contains server-provided ID_measurement with associated time stamp <- test for timestamp pending
    assert res.json()["id_measurement"] != None
    measurementsDict["duplicateSingleFOMmeasurement"]["id_measurement"] = res.json()["id_measurement"]
    assert res.json()["id_request"] == measurementsDict["duplicateSingleFOMmeasurement"]["id_request"] #<- additional test for request ID

## Get pending measurement requests - 3
def test_duplicatedSingleFOM_get_pending3():
# - post request for all pending measurements
    res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending", params={'fom_name':fom}, headers=auth_header)
# - verify response OK
    assert res.status_code == 200
# - verify response does NOT contain request ID
    assert measurementsDict["duplicateSingleFOMmeasurement"]["id_request"] not in res.json().keys()

## Get all FOM results
def test_duplicatedSingleFOM_all_fom():
# - post request for all FOMs
    res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_fom", params={'fom_name': fom},headers=auth_header)
# - verify response OK
    assert res.status_code == 200
# - verify response contains server-provided ID_measurement with all FOM’s posted previously and time stamp(s) <- test for timestamp pending
    assert measurementsDict["duplicateSingleFOMmeasurement"]["id_measurement"] in res.json().keys()
    assert res.json()[measurementsDict["duplicateSingleFOMmeasurement"]["id_measurement"]]["fom_data"] == dict(post_duplicateSingleFOMmeas.fom_data)



'''----------------------------------------------------------------------------------------
Test measurement lifecycle with four FOMs posted successively against the same request ID
-------------------------------------------------------------------------------------------'''

''' Dummy FOMs '''
fom1 = ("Density", 7.0)
fom2 = ("Viscosity", 21.42)
fom3 = ("Viscosity", 42.21)
fom4 = ("Density", 0.7)

foms = [fom1[0], fom2[0], fom3[0], fom4[0]]

''' Dummy origin '''
orig = "experiment"

''' Dummy measurement '''
multiFOMmeas = schemas_pydantic.Measurement(
        formulation = schemas_pydantic.Formulation(compounds=[config.LiPF6_EC_EMC, config.LiPF6_EC_DMC], ratio=[0.4, 0.6], ratio_method='volumetric'),
        temperature = schemas_pydantic.Temperature(value=293.15, unit='K'),
        pending = True,
        kind = schemas_pydantic.Origin(origin=orig, what=schemas_pydantic.FomEnum(fom1[0])))

''' Dummy result '''
units = {"Density": "g/cm**3", "Viscosity": "mPa*s"}
post_multiFOMmeas1 = schemas_pydantic.Measurement(
        formulation = multiFOMmeas.formulation,
        temperature = multiFOMmeas.temperature,
        pending = False,
        fom_data = schemas_pydantic.FomData(value = fom1[1],
            unit = units[fom1[0]],
            origin = multiFOMmeas.kind,
            measurement_id = "11111111",
            name = schemas_pydantic.FomEnum(fom1[0])),
        kind = multiFOMmeas.kind)

post_multiFOMmeas2 = schemas_pydantic.Measurement(
        formulation = multiFOMmeas.formulation,
        temperature = multiFOMmeas.temperature,
        pending = False,
        fom_data = schemas_pydantic.FomData(value = fom2[1],
            unit = units[fom2[0]],
            origin = multiFOMmeas.kind,
            measurement_id = "22222222",
            name = schemas_pydantic.FomEnum(fom2[0])),
        kind = multiFOMmeas.kind)

post_multiFOMmeas3 = schemas_pydantic.Measurement(
        formulation = multiFOMmeas.formulation,
        temperature = multiFOMmeas.temperature,
        pending = False,
        fom_data = schemas_pydantic.FomData(value = fom3[1],
            unit = units[fom3[0]],
            origin = multiFOMmeas.kind,
            measurement_id = "33333333",
            name = schemas_pydantic.FomEnum(fom3[0])),
        kind = multiFOMmeas.kind)

post_multiFOMmeas4 = schemas_pydantic.Measurement(
        formulation = multiFOMmeas.formulation,
        temperature = multiFOMmeas.temperature,
        pending = False,
        fom_data = schemas_pydantic.FomData(value = fom4[1],
            unit = units[fom4[0]],
            origin = multiFOMmeas.kind,
            measurement_id = "44444444",
            name = schemas_pydantic.FomEnum(fom4[0])),
        kind = multiFOMmeas.kind)

dict_measurementResults = {1: post_multiFOMmeas1, 2: post_multiFOMmeas2, 3: post_multiFOMmeas3, 4: post_multiFOMmeas4}

## Get pending measurement requests - 1
def test_multiFOM_get_pending1():
# - post request
    res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending", params={'fom_name':fom}, headers=auth_header)
# - verify response OK
    assert res.status_code == 200

## Post measurement requests
def test_multiFOM_request_meas():
# - post request (one or more of simulation / experiment)
    res = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement", data=multiFOMmeas.json(), headers=auth_header)
# - verify response OK
    assert res.status_code == 200
# - verify response contains request ID (to be verified?) with associated time stamp <- test for timestamp pending
    measurementsDict["multiFOMmeasurement"]["id_request"] = res.json()["id"]
    assert res.json()["id"] != None

## Get pending measurement requests – 2
def test_multiFOM_get_pending2():
# - post request for all pending measurements
    res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending", params={'fom_name':fom}, headers=auth_header)
# - verify response OK
    assert res.status_code == 200
# - verify response contains request ID with the same parameters as requested above and with associated time stamp <- test for timestamp pending
    assert measurementsDict["multiFOMmeasurement"]["id_request"] in res.json().keys()
    assert res.json()[measurementsDict["multiFOMmeasurement"]["id_request"]]["formulation"] == dict(multiFOMmeas.formulation)
    assert res.json()[measurementsDict["multiFOMmeasurement"]["id_request"]]["temperature"] == dict(multiFOMmeas.temperature)
    assert res.json()[measurementsDict["multiFOMmeasurement"]["id_request"]]["pending"] == multiFOMmeas.pending
    assert res.json()[measurementsDict["multiFOMmeasurement"]["id_request"]]["kind"] == dict(multiFOMmeas.kind)

## Post measurement results
def test_multiFOM_post_measurement():
    for meas in dict_measurementResults.keys():
        # - post result with request ID and user-provided measurement_ID
            res = requests.post(f"http://{config.host}:{config.port}/api/broker/post/measurement",
                data=dict_measurementResults[meas].json(),params={'request_id':measurementsDict["multiFOMmeasurement"]["id_request"]},headers=auth_header)
        # - verify response OK
            assert res.status_code == 200
        # - verify response contains server-provided ID_measurement with associated time stamp <- test for timestamp pending
            assert res.json()["id_measurement"] != None
            measurementsDict["multiFOMmeasurement"]["id_measurement"].append(res.json()["id_measurement"])
            assert res.json()["id_request"] == measurementsDict["multiFOMmeasurement"]["id_request"] #<- additional test for request ID

## Get pending measurement requests - 3
def test_multiFOM_get_pending3():
# - post request for all pending measurements
    res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending", params={'fom_name':fom}, headers=auth_header)
# - verify response OK
    assert res.status_code == 200
# - verify response does NOT contain request ID
    assert measurementsDict["multiFOMmeasurement"]["id_request"] not in res.json().keys()

## Get all FOM results
def test_multiFOM_all_fom():
    for i in range(len(measurementsDict["multiFOMmeasurement"]["id_measurement"])):
    # - post request for all FOMs
        res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_fom", params={'fom_name': foms[i]},headers=auth_header)
    # - verify response OK
        assert res.status_code == 200
    # - verify response contains server-provided ID_measurement with all FOM’s posted previously and time stamp(s) <- test for timestamp pending
        assert measurementsDict["multiFOMmeasurement"]["id_measurement"][i] in res.json().keys()
        assert res.json()[measurementsDict["multiFOMmeasurement"]["id_measurement"][i]]["fom_data"] == dict(dict_measurementResults[i+1].fom_data)







# '''----------------------------------------------------------
# Test measurement lifecycle with failed measurement/experiment (should work in future)
# -------------------------------------------------------------'''

# ''' Dummy FOM '''
# fom = "Density"

# ''' Dummy origin '''
# orig = "experiment"

# ''' Dummy measurement '''
# failedFOMmeas = schemas_pydantic.Measurement(
#         formulation = schemas_pydantic.Formulation(compounds=[config.LiPF6_EC_EMC, config.LiPF6_EC_DMC], ratio=[0.4, 0.6], ratio_method='volumetric'),
#         temperature = schemas_pydantic.Temperature(value=293.15, unit='K'),
#         pending = True,
#         kind = schemas_pydantic.Origin(origin=orig, what=fom))

# ''' Dummy result '''
# units = {"Density": "g/cm**3", "Viscosity": "mPa*s"}
# post_failedFOMmeas = schemas_pydantic.Measurement(
#         formulation = failedFOMmeas.formulation,
#         temperature = failedFOMmeas.temperature,
#         pending = False,
#         fom_data = schemas_pydantic.FomData(value = [],
#             unit = units[failedFOMmeas.kind.what],
#             origin = failedFOMmeas.kind,
#             internalReference = "543219876",
#             name = failedFOMmeas.kind.what,
#             fail = True,
#             message = "This measurement failed.",
#             rating = "5"),
#         kind = failedFOMmeas.kind)

# ## Get pending measurement requests - 1
# def test_failedFOM_get_pending1():
# # - post request
#     res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending", params={'fom_name':fom}, headers=auth_header)
# # - verify response OK
#     assert res.status_code == 200

# ## Post measurement requests
# def test_failedFOM_request_meas():
# # - post request (one or more of simulation / experiment)
#     res = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement", data=failedFOMmeas.json(), headers=auth_header)
# # - verify response OK
#     assert res.status_code == 200
# # - verify response contains request ID (to be verified?) with associated time stamp <- test for timestamp pending
#     measurementsDict["failedFOMmeasurement"]["id_request"] = res.json()["id"]
#     assert res.json()["id"] != None

# ## Get pending measurement requests – 2
# def test_failedFOM_get_pending2():
# # - post request for all pending measurements
#     res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending", params={'fom_name':fom}, headers=auth_header)
# # - verify response OK
#     assert res.status_code == 200
# # - verify response contains request ID with the same parameters as requested above and with associated time stamp <- test for timestamp pending
#     assert measurementsDict["failedFOMmeasurement"]["id_request"] in res.json().keys()
#     assert res.json()[measurementsDict["failedFOMmeasurement"]["id_request"]]["formulation"] == dict(failedFOMmeas.formulation)
#     assert res.json()[measurementsDict["failedFOMmeasurement"]["id_request"]]["temperature"] == dict(failedFOMmeas.temperature)
#     assert res.json()[measurementsDict["failedFOMmeasurement"]["id_request"]]["pending"] == failedFOMmeas.pending
#     assert res.json()[measurementsDict["failedFOMmeasurement"]["id_request"]]["kind"] == dict(failedFOMmeas.kind)

# ## Post measurement results
# def test_failedFOM_post_measurement():
# # - post result with request ID and user-provided measurement_ID
#     res = requests.post(f"http://{config.host}:{config.port}/api/broker/post/measurement",
#         data=post_failedFOMmeas.json(),params={'request_id':measurementsDict["failedFOMmeasurement"]["id_request"]},headers=auth_header)
# # - verify response OK
#     assert res.status_code == 200
# # - verify response contains server-provided ID_measurement with associated time stamp <- test for timestamp pending
#     assert res.json()["id_measurement"] != None
#     measurementsDict["failedFOMmeasurement"]["id_measurement"] = res.json()["id_measurement"]
#     assert res.json()["id_request"] == measurementsDict["failedFOMmeasurement"]["id_request"] #<- additional test for request ID

# ## Get pending measurement requests - 3
# def test_failedFOM_get_pending3():
# # - post request for all pending measurements
#     res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending", params={'fom_name':fom}, headers=auth_header)
# # - verify response OK
#     assert res.status_code == 200
# # - verify response does NOT contain request ID
#     assert measurementsDict["failedFOMmeasurement"]["id_request"] not in res.json().keys()

# ## Get all FOM results
# def test_failedFOM_all_fom():
# # - post request for all FOMs
#     res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_fom", params={'fom_name': fom},headers=auth_header)
# # - verify response OK
#     assert res.status_code == 200
# # - verify response contains server-provided ID_measurement with all FOM’s posted previously and time stamp(s) <- test for timestamp pending
#     assert measurementsDict["failedFOMmeasurement"]["id_measurement"] in res.json().keys()
#     assert res.json()[measurementsDict["failedFOMmeasurement"]["id_measurement"]]["fom_data"] == dict(post_failedFOMmeas.fom_data)





# '''----------------------------------------------------------
# Test measurement lifecycle with two FOM’s posted at once (should work in future?)
# -------------------------------------------------------------'''

# ''' Dummy FOM '''
# fom = "Density"

# ''' Dummy origin '''
# orig = "experiment"

# ''' Dummy measurement '''
# twoFOMmeas = schemas_pydantic.Measurement(
#         formulation = schemas_pydantic.Formulation(compounds=[config.LiPF6_EC_EMC, config.LiPF6_EC_DMC], ratio=[0.4, 0.6], ratio_method='volumetric'),
#         temperature = schemas_pydantic.Temperature(value=293.15, unit='K'),
#         pending = True,
#         kind = schemas_pydantic.Origin(origin=orig, what=fom))

# ''' Dummy result '''
# units = {"Density": "g/cm**3", "Viscosity": "mPa*s"}
# post_failedFOMmeas = schemas_pydantic.Measurement(
#         formulation = failedFOMmeas.formulation,
#         temperature = failedFOMmeas.temperature,
#         pending = False,
#         fom_data = schemas_pydantic.FomData(value = [21.0 ,42.0],
#             unit = units[failedFOMmeas.kind.what],
#             origin = failedFOMmeas.kind,
#             internalReference = "543219876",
#             name = failedFOMmeas.kind.what,
#             fail = False,
#             message = "This measurement succeeded.",
#             rating = "5"),
#         kind = failedFOMmeas.kind)

# ## Get pending measurement requests - 1
# def test_twoFOM_get_pending1():
# # - post request
#     res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending", params={'fom_name':fom}, headers=auth_header)
# # - verify response OK
#     assert res.status_code == 200

# ## Post measurement requests
# def test_twoFOM_request_meas():
# # - post request (one or more of simulation / experiment)
#     res = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement", data=twoFOMmeas.json(), headers=auth_header)
# # - verify response OK
#     assert res.status_code == 200
# # - verify response contains request ID (to be verified?) with associated time stamp <- test for timestamp pending
#     measurementsDict["twoFOMmeasurement"]["id_request"] = res.json()["id"]
#     assert res.json()["id"] != None

# ## Get pending measurement requests – 2
# def test_twoFOM_get_pending2():
# # - post request for all pending measurements
#     res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending", params={'fom_name':fom}, headers=auth_header)
# # - verify response OK
#     assert res.status_code == 200
# # - verify response contains request ID with the same parameters as requested above and with associated time stamp <- test for timestamp pending
#     assert measurementsDict["twoFOMmeasurement"]["id_request"] in res.json().keys()
#     assert res.json()[measurementsDict["twoFOMmeasurement"]["id_request"]]["formulation"] == dict(twoFOMmeas.formulation)
#     assert res.json()[measurementsDict["twoFOMmeasurement"]["id_request"]]["temperature"] == dict(twoFOMmeas.temperature)
#     assert res.json()[measurementsDict["twoFOMmeasurement"]["id_request"]]["pending"] == twoFOMmeas.pending
#     assert res.json()[measurementsDict["twoFOMmeasurement"]["id_request"]]["kind"] == dict(twoFOMmeas.kind)

# ## Post measurement results
# def test_twoFOM_post_measurement():
# # - post result with request ID and user-provided measurement_ID
#     res = requests.post(f"http://{config.host}:{config.port}/api/broker/post/measurement",
#         data=post_twoFOMmeas.json(),params={'request_id':measurementsDict["twoFOMmeasurement"]["id_request"]},headers=auth_header)
# # - verify response OK
#     assert res.status_code == 200
# # - verify response contains server-provided ID_measurement with associated time stamp <- test for timestamp pending
#     assert res.json()["id_measurement"] != None
#     measurementsDict["twoFOMmeasurement"]["id_measurement"] = res.json()["id_measurement"]
#     assert res.json()["id_request"] == measurementsDict["twoFOMmeasurement"]["id_request"] #<- additional test for request ID

# ## Get pending measurement requests - 3
# def test_twoFOM_get_pending3():
# # - post request for all pending measurements
#     res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending", params={'fom_name':fom}, headers=auth_header)
# # - verify response OK
#     assert res.status_code == 200
# # - verify response does NOT contain request ID
#     assert measurementsDict["twoFOMmeasurement"]["id_request"] not in res.json().keys()

# ## Get all FOM results
# def test_twoFOM_all_fom():
# # - post request for all FOMs
#     res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_fom", params={'fom_name': fom},headers=auth_header)
# # - verify response OK
#     assert res.status_code == 200
# # - verify response contains server-provided ID_measurement with all FOM’s posted previously and time stamp(s) <- test for timestamp pending
#     assert measurementsDict["twoFOMmeasurement"]["id_measurement"] in res.json().keys()
#     assert res.json()[measurementsDict["twoFOMmeasurement"]["id_measurement"]]["fom_data"] == dict(post_twoFOMmeas.fom_data)












'''----------------------------------------------------------
Final test to check, if all measurements are in the list
-------------------------------------------------------------'''

## Get list of completed measurements (final test)
def test_all_fom2():
    # - post request for Density
        resDensity = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_fom", params={'fom_name': "Density"},headers=auth_header)
    # - verify response ok
        assert resDensity.status_code == 200
    # - post request for Viscosity
        resViscosity = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_fom", params={'fom_name': "Viscosity"},headers=auth_header)
    # - verify response ok
        assert resDensity.status_code == 200
    # - verify response contains all ID_measurement’s posted above
        for meas in measurementsDict.keys():
            if type(measurementsDict[meas]["id_measurement"]) == str:
                try:
                    assert measurementsDict[meas]["id_measurement"] in resDensity.json().keys()
                except AssertionError:
                    assert measurementsDict[meas]["id_measurement"] in resViscosity.json().keys()
            elif type(measurementsDict[meas]["id_measurement"]) == list:
                for i in range(len(measurementsDict[meas]["id_measurement"])):
                    try:
                        assert measurementsDict[meas]["id_measurement"][i] in resDensity.json().keys()
                    except AssertionError:
                        assert measurementsDict[meas]["id_measurement"][i] in resViscosity.json().keys()
            else:
                print("What is this?", type(measurementsDict[meas]["id_measurement"]))



''' Aspects to consider '''
# - should each element have all related IDs? e.g. FOM has id_measurement, measurement_id AND id_request -> link from each element to all the related elements