from autoprotocol import *
from promodules.helpers import createMastermix
from thermofluor_assay import thermofluor_make_plate, thermofluor_measure
import transcriptic as tp
import json
from autoprotocol_utilities.resource_helpers import ResourceIDs
_res = ResourceIDs()
sypro_res = "rs18xyxuedc3gp"  # 5000x stock, need to get to  1:400
lysozyme = "rs18u5sv3y8haj"  # 50mg/ml, 3Molar, target is 5uM

p = Protocol()

milli_lyso = p.ref("milli_lyso", id=None,
                   cont_type="micro-1.5", storage=None, discard=True)
working_lyso = p.ref("working_lyso", id=None,
                     cont_type="micro-1.5", storage=None, discard=True)
# make 6mM
p.provision(_res.water, milli_lyso.well(0), "1000:microliter")
p.provision(lysozyme, milli_lyso.well(0), "1:microliter")
p.mix(milli_lyso.well(0), "500:microliter",
      speed="100:microliter/second", repetitions=10)

# make 60uM
p.provision(_res.water, working_lyso.well(0), "1000:microliter")
p.transfer(milli_lyso.well(0), working_lyso.well(0), "10:microliter",
           mix_after=True, mix_vol="25:microliter", repetitions=10)
p.mix(working_lyso.well(0), "500:microliter",
      speed="100:microliter/second", repetitions=10)

config = {
    "assay_name": "thermofluor",
    "reaction_volume": "45:microliter",
    "number_of_reactions": 8,
    "number_of_negative_controls": 3,
    "constant_component_volume": "2:microliter",
    "constant_component_source": working_lyso.well(0),
    "variable_component_volume": "2:microliter",
    "variable_component_source": None,
    "start_temp": "25.0:celsius",
    "end_temp": "99.0:celsius",
    "temp_interval": "0.5:celsius",
    "hold_time": "30:second",
    "Dye": ["SYBR", "HEX"]
}

thermofluor_make_plate(p, config)
thermofluor_measure(p, config)

print json.dumps(p.as_dict())
