from datetime import datetime

# Configuration file used for the FINALE integration 

config = dict()
config['access_token'] = 'i7MymDVeLFBT7z1XcZwQapr02aGXHvP8o1KCrzlX2pGfIhYkLtyp6v3DMvsf'
config['web_archive_url'] = "https://dev1-big-map-archive.materialscloud.org/"
config['email'] = 'pvifr@dtu.dk'
creators = [{"person_or_org": {
          "family_name": "Paolo",
          "given_name": "De Blasio",
          "type": "personal",
          'role' : "Work package leader"
        },
        "person_or_org": {
          "family_name": "PELE",
          "given_name": "De PELE",
          "type": "personal"}}]
type = { "id": "dataset" }
title_dataset = "Density measurement PC:DMC"
version = 'v1'
config["metadata"] = {"creators": 
    creators,
    "resource_type" : type, 
    "title" : title_dataset, 
    "version": version,
    "keywords" : ['Na-ion']
}
