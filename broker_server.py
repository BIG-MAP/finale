import uvicorn
from fastapi import FastAPI
import config
import db
import schemas_pydantic


app = FastAPI(title="fastALE broker server",
              description="main server accepting requests and serving queries",
              version="0.1")


@app.post("/post/chemical")
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
    return {"message":"recieved Chemical", "id":id_}


@app.post("/post/compound")
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


@app.get("/get/all_chemicals")
def get_all_chemicals():
    pass


@app.get("/get/all_compounds")
def get_all_compounds():
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
def post_measurement(compound: schemas_pydantic.Measurement):
    pass


@app.get("/request/measurement")
def request_meas(compound: schemas_pydantic.Measurement):
    pass


@app.on_event("shutdown")
def release():
    pass


if __name__ == "__main__":
    db_ = db.dbinteraction()
    db_.reset()
    uvicorn.run(app, host='localhost', port=13370)
