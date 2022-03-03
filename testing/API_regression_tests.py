from msilib import schema
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append("\\".join([str(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "app"]))
sys.path.append("\\".join([str(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "app\\clients"]))
sys.path.append("\\".join([str(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "app\\config"]))
sys.path.append("\\".join([str(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "db"]))
sys.path.append("C:\\Users\\Public\\Documents\\ASAB\\ASAB")
from fastapi.testclient import TestClient
from fastapi import HTTPException
import requests
import app
from db import schemas_pydantic

### Setup: Specify server to test against
from config import config
from app.broker_server import app
from app.clients import helperfcns_externalDoExperiment as helpfuncs
from experiments.Hackathon import config_Hackathon


usr = "helge"
pw = "1234"

# # Create a test client
# TC = TestClient(app)    # https://fastapi.tiangolo.com/tutorial/testing/

## Basic authentication (DTU, KIT, 3DS to look up username / password) 
def test_authenticate_user():
# - post username + password
    auth_header = helpfuncs.authenticate(usr, pw)
    print(auth_header)
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

''' Test entire measurement lifecycle '''

''' Dummy measurements '''
singleFOMmeas = schemas_pydantic.Measurement(
        formulation = schemas_pydantic.Formulation(compounds=[config.LiPF6_EC_EMC, config.LiPF6_EC_DMC], ratio=[0.4, 0.6], ratio_method='volumetric'),
        temperature = schemas_pydantic.Temperature(value=293.15, unit='K'),
        pending = True,
        kind = schemas_pydantic.Origin(origin='experiment', what='Density'),
)
# duplicatedSingleFOMmeas
# fourFOMmeas
# failedMeas
# twoFOMmeas

## Get pending measurement requests - 1
def test_get_pending1():
# - post request
    res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending", params={'fom_name':'Density'}, headers=auth_header)
# - verify response OK
    assert res.status_code == 200

## Post measurement requests
def test_request_meas():
# - post request (one or more of simulation / experiment)
    res = requests.post(f"http://{config.host}:{config.port}/api/broker/request/measurement", data=singleFOMmeas.json(), headers=auth_header)
# - verify response OK
    assert res.status_code == 200
# - verify response contains request ID (to be verified?) with associated time stamp
    assert res.json()["id"] != None

## Get pending measurement requests – 2
def test_get_pending1():
# - post request for all pending measurements
    res = requests.get(f"http://{config.host}:{config.port}/api/broker/get/pending", params={'fom_name':'Density'}, headers=auth_header)
# - verify response OK
    assert res.status_code == 200
# - verify response contains request ID with the same parameters as requested above and with associated time stamp

## Post measurement results 
# - post result with request ID and user-provided measurement_ID 
# - verify response OK
# - verify response contains server-provided ID_measurement with associated time stamp

## Get pending measurement requests - 3
# - post request for all pending measurements 
# - verify response OK
# - verify response does NOT contains request ID

## Get all FOM results
# - verify response OK
# - verify response contains server-provided ID_measurement with all FOM’s posted previously and time stamp(s)

''' # Test measurement lifecycle with single FOM result 
# Test measurement lifecycle with duplicated single FOM result
# Test measurement lifecycle with four FOM’s posted successively against the same request ID
# Test at end: 
# Test measurement lifecycle with failed measurement/experiment (should work in future)
# Test measurement lifecycle with two FOM’s posted at once (should work in future?) '''

## Get list of completed measurements (final test)
# - post request
# - verify response ok
# - verify response contains all ID_measurement’s posted above

test_request_meas()