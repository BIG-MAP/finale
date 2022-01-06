import os,sys
rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(rootp, 'config'))
sys.path.append(os.path.join(rootp, 'db'))

import uvicorn
from fastapi import FastAPI
import config, db, schemas_pydantic
from uuid import UUID


app = FastAPI(title="finale broker server",
              description="main server accepting requests and serving queries",
              version="0.9")


@app.post("/api/broker/post/chemical")
def post_chemical(chemical: schemas_pydantic.Chemical):
    """
    Experimentalists or theorists may post chemicals they can work with
    :param chemical: A Chemical object that contains the name smiles and reference
    :type chemical: Chemical validator
    :return: success return
    :rtype:
    """
    db_ = db.dbinteraction()
    id_ = db_.add_chemical(chemical)
    db_.con.commit()
    db_.con.close()
    return {"message": "recieved Chemical", "id": id_}


@app.post("/api/broker/post/compound")
def post_compound(compound: schemas_pydantic.Compound):
    """
    Experimentalists may post compounds in the setup

    :param compound:
    :type compound:
    :return:
    :rtype:
    """
    db_ = db.dbinteraction()
    id_ = db_.add_compound(compound)
    db_.con.commit()
    db_.con.close()
    return {"message": "recieved Compound", "id": id_}

@app.get("/api/broker/get/all_chemicals")
def get_all_chemicals():
    """
    TODO: Returns you a list of all compounds
    """
    db_ = db.dbinteraction()
    response = db_.query_table('chemicals')
    db_.con.commit()
    db_.con.close()
    # go through all responses to make a
    mlist = {}
    for r in response:
        json_ = schemas_pydantic.Chemical.parse_raw(r[-2])
        mlist[r[-1]] = json_
    return mlist


@app.get("/api/broker/get/all_compounds")
def get_all_compounds():
    """
    Returns you a list of all compounds
    """
    db_ = db.dbinteraction()
    response = db_.query_table('compounds')
    db_.con.commit()
    db_.con.close()
    # go through all responses to make a
    mlist = {}
    for r in response:
        json_ = schemas_pydantic.Compound.parse_raw(r[-2])
        mlist[r[-1]] = json_
    return mlist


@app.get("/api/broker/get/measurement")
def get_measurement_by_id(query_id: str):
    """
    This returns a measurement given a valid ID
    """
    try:
        id_ = UUID(query_id).hex
        db_ = db.dbinteraction()
        measurement = db_.query_measurement_by_id(id_)
        db_.con.commit()
        db_.con.close()
        return measurement
    except ValueError:
        return {"message": "invalid id", "id": query_id}
    except IndexError:
        return {"message": "Cannot find id", "id": query_id}
#    finally:
#        return {"message": "other error", "id": query_id}

@app.get("/api/broker/get/all_fom")
async def all_fom(fom_name: str):
    # get all the measurement ids where pending is false
    db_ = db.dbinteraction()
    response = db_.query_X_by_Y('measurements', 'pending', False, return_all=True)
    db_.con.commit()
    db_.con.close()
    # go through all responses to make a
    mlist = {}
    for r in response:
        print(r[-2])
        json_ = schemas_pydantic.Measurement.parse_raw(r[-2])
        if not json_.fom_data == None:
            if json_.fom_data.name == fom_name:
                mlist[r[-1]] = json_
    return mlist


@app.get("/api/broker/get/pending")
async def get_pending(fom_name: str):
    # get all the measurement ids where pending is false
    db_ = db.dbinteraction()
    response = db_.query_X_by_Y('measurements', 'pending', True, return_all=True)
    row_meas = db_.cur.fetchall()  # expect this to be unique and return id

    db_.con.commit()
    db_.con.close()
    # go through all responses to make a
    mlist = {}
    for r in response:
        json_ = schemas_pydantic.Measurement.parse_raw(r[-2])
        if json_.kind.what == fom_name:
            mlist[r[-1]] = json_
    return mlist

@app.post("/api/broker/post/measurement")
def post_measurement(measurement: schemas_pydantic.Measurement, request_id: str = None):

    # check if not pending
    if measurement.pending:
        return {"message": "posted measurement that is pending", "id": -1}
    # check that there is a fom
    if measurement.fom_data == None:
        return {"message": "posted measurement that has no fom data", "id": -1}

    db_ = db.dbinteraction()
    id_ = db_.add_measurement(measurement)
    db_.con.commit()
    db_.con.close()

    if not request_id == None:
        db_ = db.dbinteraction()

        request_id = UUID(request_id).hex
        db_ = db.dbinteraction()
        sql_update_query = "update measurements set pending = False where id = ?"
        db_.cur.execute(sql_update_query, (request_id,))

        db_.con.commit()
        db_.con.close()
        return {"message": "recieved pending measurement",
                "id_measurement": id_,
                "id_request":request_id}

    return {"message": "recieved UNSOLICITED measurement", "id": id_}


@app.post("/api/broker/request/measurement")
def request_meas(measurement: schemas_pydantic.Measurement):
    # check if really pending
    if not measurement.pending:
        return {"message": "posted measurement as request that is not pending", "id": -1}
    # check that there is no fom
    if not measurement.fom_data == None:
        return {"message": "posted measurement as request that has fom data", "id": -1}
    if measurement.kind.what == None:
        return {"message": "Not specified what to measure", "id": -1}
    db_ = db.dbinteraction()
    id_ = db_.add_measurement(measurement)
    print(id_)
    db_.con.commit()
    db_.con.close()
    return {"message": "recieved measurement request", "id": id_}


@app.on_event("shutdown")
def release():
    """
    The broker server has been shutdown. Goodbye.
    """
    return {"message": "The broker server has been shutdown. Goodbye.", "id": -1}


if __name__ == "__main__":
    db_ = db.dbinteraction()
    db_.reset()
    uvicorn.run(app, host=config.host, port=config.port)
