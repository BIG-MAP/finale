import os,sys
rootp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
#sys.path.append(os.path.join(rootp, 'config'))
#sys.path.append(os.path.join(rootp, 'db'))
sys.path.append('/code/./app/config')
sys.path.append('/code/./app/db')

#ssl certificates make nothing but problems ...
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


import uvicorn
from fastapi import FastAPI, Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import config, db, schemas_pydantic
from users import users_db

from uuid import UUID
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


app = FastAPI(title="finale broker server",
              description="main server accepting requests and serving queries",
              version="0.9")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return schemas_pydantic.UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schemas_pydantic.User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=schemas_pydantic.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/broker/post/chemical")
def post_chemical(chemical: schemas_pydantic.Chemical,token: str = Depends(oauth2_scheme)):
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
def post_compound(compound: schemas_pydantic.Compound,token: str = Depends(oauth2_scheme)):
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
def get_all_chemicals(token: str = Depends(oauth2_scheme)):
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
def get_all_compounds(token: str = Depends(oauth2_scheme)):
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
def get_measurement_by_id(query_id: str,token: str = Depends(oauth2_scheme)):
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
async def all_fom(fom_name: str,token: str = Depends(oauth2_scheme)):
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
async def get_pending(fom_name: str,token: str = Depends(oauth2_scheme)):
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
def post_measurement(measurement: schemas_pydantic.Measurement, request_id: str = None,token: str = Depends(oauth2_scheme)):

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
def request_meas(measurement: schemas_pydantic.Measurement, token: str = Depends(oauth2_scheme)):
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

@app.on_event("startup")
def release():
    """
    The broker server has been shutdown. Goodbye.
    """
    db_ = db.dbinteraction()
    db_.reset()
    return {"message": "The broker server has been shutdown. Goodbye.", "id": -1}

if __name__ == "__main__":
    db_ = db.dbinteraction()
    db_.reset()
    uvicorn.run("broker_server:app", host=config.host, port=config.port)

