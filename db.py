import sqlite3
from uuid import uuid4
import config
import schemas_pydantic


def reset(cur):
    # origins
    cur.execute("create table origins (origin, id)")
    # chemicals
    cur.execute("create table chemicals (smiles, name, reference, id)")
    # temperatures
    cur.execute("create table temperature (value, unit, id)")
    # amounts
    cur.execute("create table amount (value, unit, id)")
    # compounds
    amount_id_str = ', '.join(['amounts_id{}'.format(i) for i in range(config.MAX_D)])
    chem_id_str = ', '.join(['chemical_id{}'.format(i) for i in range(config.MAX_D)])
    cur.execute("create table compound (" + chem_id_str + ", " + amount_id_str + " ,name, id)")
    # formulations
    ratios = ', '.join(['ratio{}'.format(i) for i in range(config.MAX_D)])
    compound_id_str = ', '.join(['compound_id{}'.format(i) for i in range(config.MAX_D)])
    cur.execute("create table formulations (" + chem_id_str + ", " + amount_id_str + " ,name, id)")
    # raw data json table
    cur.execute("create table rawdata (data, description, id)")
    # fom data json table
    cur.execute("create table fomdata (value, unit, name, origin, id)")
    return {'message': 'reset complete'}


def add_chemical(cur, chemical: schemas_pydantic.Compound):
    id_ = uuid4().hex
    rows = [(chemical.smiles, chemical.name, chemical.reference, id_)]
    cur.executemany('insert into chemicals values (?,?,?,?)', rows)
    return id_

def query_chemical(cur, name:str, smiles:str):
    cur.execute("SELECT * FROM chemicals WHERE smiles=?", (smiles,))
    rows_smiles = cur.fetchall()
    cur.execute("SELECT * FROM chemicals WHERE name=?", (name,))
    rows_smiles = cur.fetchall()


    id_ = uuid4().hex
    rows = [(chemical.smiles, chemical.name, chemical.reference, id_)]
    cur.executemany('insert into chemicals values (?,?,?,?)', rows)
    return id_

def add_amount(cur, amount: schemas_pydantic.Amount):
    id_ = uuid4().hex
    rows = [(amount.value, amount.unit, id_)]
    cur.executemany('insert into chemicals values (?,?,?,?)', rows)
    return id_

def add_compound(cur, compound: schemas_pydantic.Compound):
    #figure out how many chemicals we have
    n_chemicals: int = len(compound.chemicals)
    n_amounts: int = len(compound.amounts)
    if not n_chemicals == n_amounts:
        return {'message': 'number of chemicals does not match number of amounts'}

    #if chemical or amount is already in the database we reference to these otherwise we add
    chemical_ids,amount_ids = [],[]

    amount_id_str = ', '.join(['amounts_id{}'.format(i) for i in range(config.MAX_D)])
    chem_id_str = ', '.join(['chemical_id{}'.format(i) for i in range(config.MAX_D)])
    cur.execute("create table compound (" + chem_id_str + ", " + amount_id_str + " ,name, id)")

    id_ = uuid4().hex
    rows = [(chemical.smiles, chemical.name, chemical.reference, id_)]
    cur.executemany('insert into compound values (?,?,?,?)', rows)
    return id_


