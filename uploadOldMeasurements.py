# import os,sys
# rootp = r"C:\Users\Public\Documents\Hackathon\finale\app"#os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# #rootp += "/fastALE/"
# sys.path.append(os.path.join(rootp, 'config'))
# sys.path.append(os.path.join(rootp, 'db'))
# sys.path.append(os.path.join(rootp, 'clients'))
# sys.path.append(os.path.dirname(rootp))

# print(rootp)

# import app.config
# from app.db import schemas_pydantic
# from app.clients.helperfcns import do_experiment,authenticate
# import requests
# import time
# import numpy as np

# from app.config import config

# import sqlite3
# import numpy as np

# auth_header = authenticate("helge", "1234")

# connection = sqlite3.connect("C:\\Users\\remote\\Downloads\\session_clean_latest.db")
# cursor = connection.cursor()

# cursor.execute("select * from measurements")
# # cursor.description
# #cursor.execute("select * from measurements where pending=False")
# #cursor.execute("select * from fomdata where id='5028363007'") # measurement_id='5028363007'")
# #cursor.description
# data = cursor.fetchall()
# print(list(data[1]))
# j=0
# for i in range(len(data)):
#     dat = list(data[i])[4]
#     print(dat)
#     measurement = schemas_pydantic.Measurement.parse_raw(data[i][6])
#     print(measurement)
#     print("\n -------------------------------------------------------------------------------------------\n")
#     #if measurement.pending == False:
#     # print(measurement.fom_data)
#     # ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/post/measurement",
#     #     data=measurement.json(),params={'request_id':dat},headers=auth_header).json()
#     j+=1

#     # if measurement.fom_data.measurement_id == "5548694957":
#         #     print(measurement)
# print(j)

# # fomData = requests.get(f"http://{config.host}:{config.port}/api/broker/get/all_fom", params={'fom_name':'Viscosity'},headers=auth_header).json()

# # print(len(fomData))

from cmath import nan
from random import sample
import pandas as pd
import numpy as np
import requests
from app.db.schemas_pydantic import Formulation, Compound, Chemical, Amount, Temperature, Origin, Measurement, FomData
from app.config import config
from app.clients.helperfcns import authenticate

auth_header = authenticate("kit", "KIT_huipuischui_23")#"helge", "1234")

savePath = r"C:\Users\remote\Desktop"

# Load the raw data
data = pd.read_csv(r"C:\Users\remote\Desktop\20220211_113931_Export.csv", sep=";", dtype=str)

units = {"density": "g/cm**3", "viscosity": "mPa*s"}

info = {
    "5548694957": {
        "formulation": Formulation(compounds=[Compound(chemicals=[Chemical(smiles='C1COC(=O)O1', name='EC', reference='EC_Elyte_2020'), Chemical(smiles='CCOC(=O)OC', name='EMC', reference='EMC_ELyte_2020')], amounts=[Amount(value=0.15, unit='Mol'), Amount(value=0.3, unit='Mol')], name='EC_EMC_3:7')], ratio=[1.0], ratio_method='volumetric'),
        "temperature": Temperature(value=293.15, unit='K'),
        "pending": False,
        "kind": Origin(origin='experiment'),
        "reqID": "123"
        },
    "5028363007": {
        "formulation": Formulation(compounds=[Compound(chemicals=[Chemical(smiles='C1COC(=O)O1', name='EC', reference='EC_Elyte_2020'), Chemical(smiles='CCOC(=O)OC', name='EMC', reference='EMC_ELyte_2020'), Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')], amounts=[Amount(value=0.5, unit='Mol'), Amount(value=0.5, unit='Mol'), Amount(value=0.1, unit='Mol')], name='LiPF6_salt_in_EC_EMC_3:7')], ratio=[1.0], ratio_method='volumetric'),
        "temperature": Temperature(value=293.15, unit='K'),
        "pending": False,
        "kind": Origin(origin='experiment'),
        "reqID": "456"
        },
    "8048016963": {
        "formulation": Formulation(compounds=[Compound(chemicals=[Chemical(smiles='C1COC(=O)O1', name='EC', reference='EC_Elyte_2020'), Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020'), Chemical(smiles='[Li+].F[P-](F)(F)(F)(F)F', name='LiPF6', reference='LiPF6_Elyte_2020')], amounts=[Amount(value=0.5, unit='Mol'), Amount(value=0.5, unit='Mol'), Amount(value=0.4, unit='Mol')], name='LiPF6_salt_in_EC_DMC_1:1')], ratio=[1.0], ratio_method='volumetric'),
        "temperature": Temperature(value=293.15, unit='K'),
        "pending": False,
        "kind": Origin(origin='experiment'),
        "reqID": "789"
        },
    "7829609892": {
        "formulation": Formulation(compounds=[Compound(chemicals=[Chemical(smiles='C1COC(=O)O1', name='EC', reference='EC_Elyte_2020'), Chemical(smiles='COC(=O)OC', name='DMC', reference='DMC_Elyte_2020')], amounts=[Amount(value=0.31, unit='Mol'), Amount(value=0.3, unit='Mol')], name='EC_DMC_1:1')], ratio=[1.0], ratio_method='volumetric'),
        "temperature": Temperature(value=293.15, unit='K'),
        "pending": False,
        "kind": Origin(origin='experiment'),
        "reqID": "159"
        }
        }

# Get the relevant data
for sampleName in data["Metadaten::Probenname"].unique():
    data2 = data.loc[data["Metadaten::Probenname"]==sampleName]
    extractedData = {"sampleName": sampleName,
                        "density":
                            {"status": list(data2.loc[data2["Ergebnisse::Messlevel"]!="Master", "Ergebnisse::Dichte Status"].values),#[1:]),
                            "quality": np.NaN,
                            "values": list(data2.loc[data2["Ergebnisse::Messlevel"]!="Master", "Ergebnisse::Dichte"].values)},#[1:])},
                        "viscosity":
                            {"status": list(data2.loc[data2["Ergebnisse::Messlevel"]!="Master", "Ergebnisse::Lovis Status"].values),#[1:]),
                            "quality": np.NaN,
                            "values": list(data2.loc[data2["Ergebnisse::Messlevel"]!="Master", "Ergebnisse::Lovis Dyn. Visk."].values)}}#[1:])}}
    print("ExtractedData:", extractedData.keys())
    for key, value in extractedData.items():
        print(key, value)
        if key != "sampleName":
            print("key:", key, "val:", value)
            # Get floats for the values
            values = np.array(value["values"], dtype=np.float64)
            # Mark the values according to their validity
            markedValues = np.ma.masked_array(values, mask=[stat != "valid" for stat in value["status"]])
            # Replace the invalid values by np.NaN
            markedValues[markedValues.mask] = np.NaN
            # Assign processed values to the extractedData
            extractedData2 = extractedData.copy()
            extractedData2[key]["values"] = list(markedValues.data)
            # Add the quality to the extractedData
            extractedData2[key]["quality"] = 10. - (np.sum(markedValues.mask)/float(len(value["values"])))
    for key2, value2 in extractedData2.items():
        print("key2", key2, "value2", value2)
        if key2 != "sampleName" and key2 != "quality":
            for v in value2["values"]:
                if not np.isnan(v):
                    fom_data = FomData(value=v,
                                unit=units[key2],
                                origin=Origin(origin='experiment'),
                                measurement_id=sampleName,
                                name=str(key2.capitalize()))
                    # Prepare the measurement for posting
                    measurementPost = Measurement( formulation=info[sampleName]["formulation"],
                                            temperature=info[sampleName]["temperature"],
                                            pending=info[sampleName]["pending"],
                                            fom_data=fom_data,
                                            kind=info[sampleName]["kind"])
                    # print("\n \n ", measurementPost, "\n \n ")
                    ans_ = requests.post(f"http://{config.host}:{config.port}/api/broker/post/measurement",
                                        data=measurementPost.json(),headers=auth_header).json()
    with open(f"{savePath}\\{sampleName}_raw.json", "w") as file:
        file.write(str(extractedData))   # https://stackoverflow.com/questions/29223246/how-do-i-save-data-in-a-text-file-python
    with open(f"{savePath}\\{sampleName}_result.json", "w") as file:
        file.write(str(extractedData2))
    print(extractedData)
