from autoprotocol import *
from promodules.helpers import createMastermix
from thermofluor_assay import thermofluor_make_plate, thermofluor_measure
import transcriptic as tp
import json

p = Protocol()

config = {
    "assay_name": "thermofluor",
    "reaction_volume": "25:microliter",
    "number_of_reactions": 96,
    "number_of_negative_controls": 3,
    "start_temp": "25.0:celsius",
    "end_temp": "99.0:celsius",
    "temp_interval": "0.5:celsius",
    "hold_time": "30:second",
    "Dye": ["SYBR", "HEX"]
}

thermofluor_make_plate(p, config)
thermofluor_measure(p, config)

print json.dumps(p.as_dict())

# tp.submit(p, "dev", config["assay_name"], test_mode=True)
