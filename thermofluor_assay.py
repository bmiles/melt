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

    total_reaction_volume =

    assay_plate = p.ref("assay_plate", id=None, cont_type="96-pcr", storage="cold_4", discard=False)
    working_sypro = p.ref("working_sypro", id=None, cont_type="micro-1.5", storage=None, discard=True)
    milli_lyso = p.ref("milli_lyso", id=None, cont_type="micro-1.5", storage=None, discard=True)
    working_lyso = p.ref("working_lyso", id=None, cont_type="micro-1.5", storage=None, discard=True)

    assay_plate_wells = assay_plate.wells_from(0, 8, columnwise=True)


    # Make master mixes

    p.provision(_res.water, working_sypro.well(0), "399:microliter")
    p.provision(sypro_res, working_sypro.well(0), "1:microliter")
    p.mix(working_sypro.well(0), "200:microliter", speed="50:microliter/second", repetitions=10)

    # make 6mM
    p.provision(_res.water, milli_lyso.well(0), "1000:microliter")
    p.provision(lysozyme, milli_lyso.well(0), "1:microliter")
    p.mix(milli_lyso.well(0), "500:microliter", speed="100:microliter/second", repetitions=10)

    # make 60uM
    p.provision(_res.water, working_lyso.well(0), "1000:microliter")
    p.transfer(milli_lyso.well(0), working_lyso.well(0), "10:microliter", mix_after=True, mix_vol="25:microliter", repetitions=10)
    p.mix(working_lyso.well(0), "500:microliter", speed="100:microliter/second", repetitions=10)

    # matermix_wells = createMastermix(p, "assay_mastermix",
    #                            reagent_plate, 10,
    #                            {_res.te: te_max_vol},
    #                            [{"source": water_wells,
    #                              "volume": Unit(5, "ul")},
    #                              {"source": enzyme_wells,
    #                              "volume": enzyme_concentration}])

    p.dispense(assay_plate, "pbs", [{"column": 0, "volume": "20:microliter"}])

    p.distribute(working_sypro.well(0), assay_plate_wells, "5:microliter", allow_carryover=True)
    p.distribute(working_lyso.well(0), assay_plate.wells_from(0, 7, columnwise=True), "2:microliter", allow_carryover=False, mix_vol="25:microliter", repetitions=10)
    p.seal(assay_plate)
    p.spin(assay_plate, "2000:rpm", "2:minute")


def thermofluor_measure(protocol, config):
    global p
    p = protocol

    p.thermocycle(assay_plate, [{
        "cycles": 1,
        "steps": gen_steps(config["start_temp"],
                config["end_temp"],
                config["temp_interval"],
                config["hold_time"])
        }],
        volume=config["reaction_volume"],
        dataref=config["assay_name"],
        dyes={
            config["Dye"][0]: assay_plate_wells.indices(),
            config["Dye"][1]: assay_plate_wells.indices()}
        )


def thermofluor_analyse(run_id):
    # pulls down data from a run, processes it and returns a dataframe
    # pull down run dataref

    # make melt curve for each water_wells
    # make a dFluoro/dT curve
    # detect peak and calc the Tm
    return df


def gen_steps(start_temp, end_temp, temp_interval, hold_time):
    steps = []
    start_temp = Unit(start_temp)
    end_temp = Unit(end_temp)
    temp_interval = Unit(temp_interval)
    temps = arange(start_temp.magnitude, end_temp.magnitude + temp_interval.magnitude, temp_interval.magnitude)
    for temp in temps:
        step = {"temperature": Unit(temp, "celsius"), "duration": hold_time, "read": True}
        steps.append(step)
    return steps
