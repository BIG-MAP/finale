import sqlite3
from uuid import uuid4
import config
import schemas_pydantic

class dbinteraction:
    def __init__(self):
        self.con = sqlite3.connect(config.db_file)
        self.cur = self.con.cursor()

    def reset(self):
        # origins
        self.cur.execute("create table origins (origin, id)")
        # chemicals
        self.cur.execute("create table chemicals (smiles, name, reference, id)")
        # compounds
        amounts_value = ', '.join(['amounts_value{}'.format(i) for i in range(config.MAX_D)])
        amounts_unit = ', '.join(['amounts_unit{}'.format(i) for i in range(config.MAX_D)])
        chem_id_str = ', '.join(['chemical_id{}'.format(i) for i in range(config.MAX_D)])
        self.cur.execute("create table compounds (" + chem_id_str + ", " + amounts_value + ", " + amounts_unit + " ,name, id)")
        # formulations
        ratios_str = ', '.join(['ratio{}'.format(i) for i in range(config.MAX_D)])
        compound_id_str = ', '.join(['compound_id{}'.format(i) for i in range(config.MAX_D)])
        self.cur.execute("create table formulations (" + compound_id_str + ", " + ratios_str + " ,ratio_method , id)")
        # fom data json table
        self.cur.execute("create table fomdata (value, unit, name, origin, measurement_id, id)")
        #measurement table
        self.cur.execute("create table measurements (formulation_id,temperature_value,temperature_unit,pending,fom_data_id,kind, id)")
        self.con.commit()
        return {'message': 'reset complete'}


    def _add_chemical_forced(self, chemical: schemas_pydantic.Compound):
        id_ = uuid4().hex
        rows = [(chemical.smiles, chemical.name, chemical.reference, id_)]
        self.cur.executemany('insert into chemicals values (?,?,?,?)', rows)
        return id_


    def query_chemicals_by_smiles(self, smiles: str, return_ids=False):
        self.cur.execute("select * from chemicals where smiles=:smiles_query", {"smiles_query": smiles})
        rows_smiles = self.cur.fetchall()
        if return_ids:
            return [r[-1] for r in rows_smiles]
        else:
            return rows_smiles


    def query_chemicals_by_id(self, id_):
        self.cur.execute("select * from chemicals where id=:id_query", {"id_query": id_})
        rows_smiles = self.cur.fetchall()
        return rows_smiles[0]


    def add_chemical(self, chemical: schemas_pydantic.Chemical):
        # we consider smiles to be unique
        rows_smiles = self.query_chemicals_by_smiles(chemical.smiles)
        if len(rows_smiles) > 0:
            print("found {} smiles matching rows".format(len(rows_smiles)))
        else:
            # if we do not have the smiles in the database we add it and return the id
            id_ = self._add_chemical_forced(chemical)
            print('new smiles')
            return id_
        # only if the reference changes we consider this to be a new chemical
        # this is because a new reference can mean something changes in the calculation or a new batch has been added
        for i in range(len(rows_smiles)):
            if chemical.reference == rows_smiles[i][2]:
                # this is an exact match though it might have a different name
                id_ = rows_smiles[i][3]
                print('known smiles')
                return id_
        if i == len(rows_smiles):
            # i.e. reference changed
            id_ = self._add_chemical_forced(chemical)
            print('new reference')
            return id_
        else:
            return {"message": "fail"}

    def query_X_by_Y(self, X, Y, value):
        self.cur.execute("select * from {} where {}=:iquery".format(X,Y), {"iquery": value})
        rows = self.cur.fetchall()#expect this to be unique and return id
        if len(rows) > 0:
            return rows[0][-1]
        else:
            return -1

    def add_compound(self, compound: schemas_pydantic.Compound):
        # check if compound already exists
        id_ = self.query_X_by_Y('compounds','name',compound.name)
        if not id_ == -1:
            return id_
        # figure out how many chemicals we have
        n_chemicals: int = len(compound.chemicals)
        n_amounts: int = len(compound.amounts)
        if not n_chemicals == n_amounts:
            return {'message': 'number of chemicals does not match number of amounts'}

        # if chemical or amount is already in the database we reference to these otherwise we add
        chemical_ids, amount_ids = [], []
        chemical_ids,chem_i = [],0
        for chemical in compound.chemicals:
            chemical_ids.append(self.add_chemical(chemical))
            chem_i += 1
        for i in [i for i in range(chem_i,config.MAX_D)]:
            chemical_ids.append('-1')
        amount_values,amount_units= [],[]
        for amount in compound.amounts:
            amount_values.append(amount.value)
            amount_units.append(amount.unit)
        for i in [i for i in range(chem_i,config.MAX_D)]:
            amount_values.append('-1')
            amount_units.append('Mol')
        id_ = uuid4().hex
        arr = [*chemical_ids,*amount_values,*amount_units,compound.name,id_]
        qstr = '('+','.join(['?' for i in range(len(arr))])+')'
        self.cur.execute("insert into compounds values {}".format(qstr),arr)

        return id_


    def add_formulation(self, formulation: schemas_pydantic.Formulation):
        #add compounds where nessesary
        compound_ids,compound_i = [],0
        for compound in formulation.compounds:
            compound_ids.append(self.add_compound(compound))
            compound_i += 1
        #add padding ids
        for i in [i for i in range(compound_i, config.MAX_D)]:
            compound_ids.append('-1')
        ratios = [float(r) for r in formulation.ratio]
        for i in [i for i in range(compound_i, config.MAX_D)]:
            ratios.append(0)

        id_ = uuid4().hex
        arr = [*compound_ids,*ratios,formulation.ratio_method,id_]
        qstr = '('+','.join(['?' for i in range(len(arr))])+')'
        self.cur.execute("insert into formulations values {}".format(qstr),arr)

        return id_


    def add_fom(self,fom: schemas_pydantic.FomData,measurement_id_):
        id_ = uuid4().hex
        arr = [fom.value,fom.unit,fom.name,fom.origin.origin.value,measurement_id_,id_]
        qstr = '('+','.join(['?' for i in range(len(arr))])+')'
        self.cur.execute("insert into fomdata values {}".format(qstr),arr)
        return id_


    def add_measurement(self,measurement: schemas_pydantic.Measurement):
        id_ = uuid4().hex
        try:
            fom_data = measurement.fom_data
            fom_id_ = self.add_fom(fom_data,measurement_id_=id_)
        except AttributeError:
            fom_id_ = -1
        formulation_id = self.add_formulation(measurement.formulation)
        temperature_value = measurement.temperature.value# = Field(...)
        temperature_unit = measurement.temperature.unit# = Field(...)
        pending = measurement.pending
        kind = measurement.kind.origin.value
        arr = [formulation_id,temperature_value,temperature_unit,pending,fom_id_,kind, id_]
        qstr = '(' + ','.join(['?' for i in range(len(arr))]) + ')'
        self.cur.execute("insert into measurements values {}".format(qstr),arr)

        return id_

    def setup():
        if config.db_file==None:
            config.db_file = 'db/session_{}.db'.format(uuid4().int)

        con = sqlite3.connect(config.db_file)
        self.cur = con.cursor()

        msg = reset(cur)

        return msg,cur,con,config.db_file