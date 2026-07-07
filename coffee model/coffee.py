"""
Python model 'coffee.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.statefuls import Integ
from pysd.py_backend.lookups import HardcodedLookups
from pysd import Component

__pysd_version__ = "3.14.3"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 100,
    "time_step": lambda: 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="Minute", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Minute", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Minute",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="Minute",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="adjust", units="Minute", comp_type="Constant", comp_subtype="Normal"
)
def adjust():
    """
    29
    """
    return 30


@component.add(
    name="change in coffee temp",
    units="celsius/Minute",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"diff": 1, "adjust": 1},
)
def change_in_coffee_temp():
    return diff() / adjust()


@component.add(
    name="coffee temp",
    units="celsius",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_coffee_temp": 1},
    other_deps={
        "_integ_coffee_temp": {"initial": {}, "step": {"change_in_coffee_temp": 1}}
    },
)
def coffee_temp():
    return _integ_coffee_temp()


_integ_coffee_temp = Integ(
    lambda: change_in_coffee_temp(), lambda: 87, "_integ_coffee_temp"
)


@component.add(
    name="room temp", units="celsius", comp_type="Constant", comp_subtype="Normal"
)
def room_temp():
    return 29


@component.add(
    name="diff",
    units="celsius",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"room_temp": 1, "coffee_temp": 1},
)
def diff():
    return room_temp() - coffee_temp()


@component.add(
    name="coffee temperature",
    units="celsius",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "one_minute": 1, "coffee_temperature_lookup": 1},
)
def coffee_temperature():
    return coffee_temperature_lookup(time() / one_minute())


@component.add(
    name="coffee temperature lookup",
    units="celsius",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_coffee_temperature_lookup"},
)
def coffee_temperature_lookup(x, final_subs=None):
    return _hardcodedlookup_coffee_temperature_lookup(x, final_subs)


_hardcodedlookup_coffee_temperature_lookup = HardcodedLookups(
    [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    [87, 72, 58, 50, 45, 41, 38, 35, 32, 30, 29],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_coffee_temperature_lookup",
)


@component.add(
    name="one minute", units="Minute", comp_type="Constant", comp_subtype="Normal"
)
def one_minute():
    return 1
