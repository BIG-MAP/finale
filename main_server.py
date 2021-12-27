import sys
import uvicorn
from fastapi import FastAPI
import os
import schemas_pydantic

app = FastAPI(title="fastALE main server",
              description="main server accepting requests and serving queries",
              version="0.1")


@app.get("/post/chemical")
def post_chemical(chemical: schemas_pydantic.Chemical):
    pass


@app.get("/post/compound")
def activate(compound: schemas_pydantic.Compound):
    pass

@app.get("/get/all_chemicals")
def activate():
    pass


@app.get("/get/all_compounds")
def activate():
    pass


@app.get("/get/measurement/by_id")
def by_id(id: str):
    pass


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
