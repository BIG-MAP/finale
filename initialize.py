import sqlite3
import config
import db
import schemas_pydantic
from uuid import uuid4

if config.restart:
    config.db_file = 'db/session_{}.db'.format(uuid4().int)

con = sqlite3.connect(config.db_file)
cur = con.cursor()

msg = db.reset(cur)

# The qmark style used with executemany():
chem_list = [
    ('COC(=O)OC', 'DMC', 'DMC_Elyte_2020'),
    ('[Li+].F[P-](F)(F)(F)(F)F', 'LiPF6', 'LiPF6_Elyte_2020'),
    ('smile_3', 'name_3', 'ref_3'),
    ('smile_4', 'name_4', 'ref_4'),
    ('smile_5', 'name_5', 'ref_5'),
    ('smile_6', 'name_6', 'ref_6'),
]

def make_chemicals(c):
    return schemas_pydantic.Chemical(name=c[1],smiles=c[0],reference=c[2])

chem_ids = []
for c in chem_list:
    chem_ids.append(db.add_chemical(cur,make_chemicals(chem_list[0])))


# And this is the named style:
cur.execute("select * from chemicals where name=:chem_name", {"chem_name": 'DMC'})
print(cur.fetchall())

cur.execute("select * from chemicals where name=?", 'DMC')
