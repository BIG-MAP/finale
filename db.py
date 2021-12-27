import sqlite3
from uuid import uuid4, UUID
MAX_D = 7
restart = True
if restart:
    db_file = 'db/session_{}.db'.format(uuid4().int)
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    # origins
    cur.execute("create table origins (origin, id)")
    # chemicals
    cur.execute("create table chemicals (smiles, name, reference, id)")
    # temperatures
    cur.execute("create table temperature (value, unit, id)")
    # amounts
    cur.execute("create table amount (value, unit, id)")
    # compounds
    amount_id_str = ', '.join(['amounts_id{}'.format(i) for i in range(MAX_D)])
    chem_id_str = ', '.join(['chemical_id{}'.format(i) for i in range(MAX_D)])
    cur.execute("create table compound (" + chem_id_str + ", " + amount_id_str + " ,name, id)")
    # formulations
    ratios = ', '.join(['ratio{}'.format(i) for i in range(MAX_D)])
    compound_id_str = ', '.join(['compound_id{}'.format(i) for i in range(MAX_D)])
    cur.execute("create table formulations (" + chem_id_str + ", " + amount_id_str + " ,name, id)")
    # raw data json table
    cur.execute("create table rawdata (data, description, id)")
    # fom data json table
    cur.execute("create table fomdata (value, unit, name, origin, id)")


# The qmark style used with executemany():
chem_list = [
    ('COC(=O)OC', 'DMC', 'DMC_Elyte_2020',uuid4().hex),
    ('[Li+].F[P-](F)(F)(F)(F)F', 'LiPF6', 'LiPF6_Elyte_2020',uuid4().hex)
]
cur.executemany("insert into chemicals values (?, ?, ?, ?)", chem_list)

# And this is the named style:
cur.execute("select * from chemicals where name=:chem_name", {"chem_name": 'DMC'})
print(cur.fetchall())

cur.execute("select * from chemicals where name=?", 'DMC')
