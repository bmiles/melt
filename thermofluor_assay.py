from autoprotocol import *
from autoprotocol_utilities.thermocycle_helpers import melt_curve
from autoprotocol_utilities.resource_helpers import ResourceIDs
from promodules.helpers import createMastermix
from numpy import arange

_res = ResourceIDs()

sypro_res = "rs18xyxuedc3gp"  # 5000x stock, need to get to  1:400
lysozyme = "rs18u5sv3y8haj"  # 50mg/ml, 3Molar, target is 5uM


def thermofluor_make_plate(protocol, config):
    global p
    global assay_plate
    global assay_plate_wells
    p = protocol

    reaction_volume = Unit(config["reaction_volume"])
    constant_component_volume = Unit(config["constant_component_volume"])
    variable_component_volume = Unit(config["variable_component_volume"])
    sypro_volume = Unit("5:microliter")

    buffer_volume = reaction_volume - (constant_component_volume +
                                       variable_component_volume + sypro_volume)

    assay_plate = p.ref("assay_plate", id=None,
                        cont_type="96-pcr", storage="cold_4", discard=False)

    assay_plate_wells = assay_plate.wells_from(
        0, config["number_of_reactions"], columnwise=True)
    working_sypro = p.ref("working_sypro", id=None,
                          cont_type="micro-1.5", storage=None, discard=True)

    assert len(assay_plate_wells) == config["number_of_reactions"]
    # Make master mixes

    p.mix(working_sypro.well(0), "200:microliter",
          speed="50:microliter/second", repetitions=10)

    working_sypro = createMastermix(p, "sypro_mm", "micro-1.5",
                                    config["number_of_reactions"],
                                    {
                                        _res.water: Unit("5:microliter") * 0.96,
                                        sypro_res: Unit("5:microliter") * 0.04
                                    })

    p.dispense(assay_plate, "pbs", [{"column": 0, "volume": Unit(
        dispense_round(buffer_volume.magnitude), "microliter")}])

    p.distribute(working_sypro, assay_plate_wells,
                 "5:microliter", allow_carryover=False)
    for well in assay_plate_wells[:-1]:
        p.transfer(config["constant_component_source"], well,
                   "2:microliter", mix_vol="25:microliter", repetitions=10)

    p.seal(assay_plate)
    p.spin(assay_plate, "2000:g", "2:minute")


def thermofluor_measure(protocol, config):
    global p
    p = protocol
    start_temp = Unit(config["start_temp"])
    end_temp = Unit(config["end_temp"])
    temp_interval = Unit(config["temp_interval"])
    hold_time = Unit(config["hold_time"])

    melt_params = melt_curve(start=start_temp.magnitude, end=end_temp.magnitude,
                             inc=temp_interval.magnitude, rate=int(hold_time.magnitude))

    p.thermocycle(assay_plate, [{
        "cycles": 1,
        "steps": [{"temperature": start_temp,
                   "duration": hold_time, "read": True}]
    }],
        volume=config["reaction_volume"],
        dataref=config["assay_name"],
        dyes={
            config["Dye"][0]: assay_plate_wells.indices(),
            config["Dye"][1]: assay_plate_wells.indices()},
        **melt_params)


def dispense_round(x, base=5):
    return int(base * round(float(x) / base))
