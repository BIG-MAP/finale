import sys
import uvicorn
from fastapi import FastAPI
import sqlite3
import config
import db
import schemas_pydantic
from uuid import uuid4


app = FastAPI(title="fastALE main server",
              description="main server accepting requests and serving queries",
              version="0.1")


@app.get("/post/chemical")
def post_chemical(chemical: schemas_pydantic.Chemical):
    """
    Experimentalists or theorists may post chemicals they can work with
    :param chemical: A Chemical object that contains the name smiles and reference
    :type chemical: Chemical validator
    :return: success return
    :rtype:
    """
    id_ = db.add_chemical(cur,chemical)
    return {"message":"recieved Chemical", "id":id_}


@app.get("/post/compound")
def post_compound(compound: schemas_pydantic.Compound):
    id_ = db.add_compound(cur, compound)
    return {"message": "recieved Compound", "id": id_}

@app.get("/get/all_chemicals")
def activate():
    pass


@app.get("/get/all_compounds")
def activate():
    pass


@app.get("/get/measurement/by_id")
def by_id(id__: str):
    try:
        id_ = UUID(id__).hex()
        ret = query(table="measurement", match="id", value=id_)

    except ValueError:
        return False

@app.get("/get/all_fom")
def all_fom(origin: schemas_pydantic.Origin, name:schemas_pydantic.FOM):
    pass


@app.get("/post/measurement")
def pos_meas(compound: schemas_pydantic.Measurement):
    pass


@app.get("/request/measurement")
def req_meas(compound: schemas_pydantic.Measurement):
    pass



@app.on_event("shutdown")
def release():
    pass


if __name__ == "__main__":

    uvicorn.run(app, host=config['servers'][serverkey]['host'], port=config['servers'][serverkey]['port'])
