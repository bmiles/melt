![melt_image](https://raw.githubusercontent.com/bmiles/melt/master/img/melt.png)

# melt
This repo contains a protocol for running a thermofluor melt assay on Transcriptic. It is a work in progress. An example execution is shown in `run.py` to determine the Tm of lysozyme.

# Thermofluor assay
The thermoflour assay utilizes qPCR thermocycler to monitor the fluorescence of a dye in the presence of a protein undergoing molten state transition. In the presence of the dye the solution is monotonically heated over a temperature range to cause the protein to denature. This denaturation exposes the hydrophobic core of the protein where the fluorophore may bind and its fluorescence measured by the thermocycler.

The increasing fluorescence of the sample can be plotted against the increasing temperature to determine the Tm of the protein. This is traditionally achieved by techniques such as circular dichroism.

# Dependencies
This protocol requires `autoprotocol-python`, `promodules`, `autoprotocol_utilities`.

# Config

The config dict passed to both `make_plate` and `measure` contains a number of parameters for the experiment including source wells for reaction components as wells the parameters of the melt curve.

```json
config = {
    "assay_name": "thermofluor",
    "reaction_volume": "45:microliter",
    "number_of_reactions": 8,
    "number_of_negative_controls": 3,
    "constant_component_volume": "2:microliter",
    "constant_component_source": working_lyso.well(0),
    "variable_component_volume": "2:microliter",
    "variable_component_source": ligand_plate_wells,
    "start_temp": "25.0:celsius",
    "end_temp": "99.0:celsius",
    "temp_interval": "0.5:celsius",
    "hold_time": "30:second",
    "Dye": ["SYBR", "HEX"]
}
```
## Constant components
`WellGroup`
You may wish to have  constant component in every reaction. For instance you may wish to have the same protein in all reactions and vary the ligand being added. Alternatively you may wish to have a plate of mutants and keep the ligand the same for each reaction.

## Variable components
`WellGroup`
These are components that are different for each well, so for instance if you wish to simultaneous find the Tm of multiple different proteins simultaneously you can use this, or if you wish to investigate the effect of different ligands on the Tm of a single protein you can use this for inputting the source wells for each of the different ligands.

## Dye
The dye used in this assay is actually SYPRO orange however this is not a preset on the Biorad CFX thermocycler so the Dyes are stated as SYBR and HEX channels of the instrument that correlate to the fluorescence properties of SYPRO orange.
