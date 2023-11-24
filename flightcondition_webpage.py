"""
Webpage for the flightcondition Python package.

Author: Matthew C. Jones
Email: matt.c.jones.aoe@gmail.com

:copyright: 2023 Matthew C. Jones
:license: MIT License, see LICENSE for more details.
"""

# Import packages
import streamlit as st
import pandas as pd
import numpy as np

from flightcondition import FlightCondition, unit

########################################
# Initialize
########################################
# Initialize variables if no session sate
if 'h' not in st.session_state:
    st.session_state['h'] = 0.0
if 'h_unit' not in st.session_state:
    st.session_state['h_unit'] = 'kft'


# Define functional responses
def update_flightcondition(*args, **kwargs):
    """Update flightcondition data on webpage """
    fc = FlightCondition(*args, **kwargs)
    # st.session_state['h'] = fc.h.to(st.session_state.h_unit).magnitude


########################################
# Build webpage
########################################
# --------------------------------------
# Front Matter
# --------------------------------------
st.title("Flight Condition Calculator")
desc = """Compute common flight condition quantities and airspeed conversions.

Powered by the **flightcondition** Python package 
https://github.com/MattCJones/flightcondition"""
st.markdown(desc)


# --------------------------------------
# Altitude Input
# --------------------------------------
st.subheader("Altitude")
col1, col2, col3 = st.columns(3)
with col1:
    st.selectbox(
        "Altitude type",
        ("Geometric altitude", "Geopotential altitude"), key='altitude_type',
    )

with col2:
    if (st.session_state['altitude_type'] == "Geometric altitude"
       or st.session_state['altitude_type'] == "Geopotential altitude"):
        st.number_input(
            label="Value", min_value=0.0, format='%01.8g', step=0.1, key='h',
            #on_change=update_flightcondition(h=st.session_state.h*unit(st.session_state.h_unit))
        )

with col3:
    if (st.session_state['altitude_type'] == "Geometric altitude"
       or st.session_state['altitude_type'] == "Geopotential altitude"):
        st.selectbox(
            "Altitude unit",
            ("kft", "km"), key='h_unit',
            #on_change=update_flightcondition(h=st.session_state.h*unit(st.session_state.h_unit))
        )
    elif st.session_state['altitude_type'] == "Pressure":
        pass

# --------------------------------------
# Airspeed Input
# --------------------------------------
st.subheader("Airspeed")
col1, col2, col3 = st.columns(3)
with col1:
    st.selectbox(
        "Airspeed type",
        ("Mach Number", "True Airspeed", "Calibrated Airspeed", "Equivalent Airspeed"), key='airspeed_type',
    )

with col2:
    if st.session_state['airspeed_type'] == "Mach Number":
        st.number_input(
            label="Value", min_value=0.0, format='%01.8g', step=0.05,
            key="airspeed", help="Mach Number"
        )
    elif (st.session_state['airspeed_type'] == "True Airspeed"
         or st.session_state['airspeed_type'] == "Calibrated Airspeed"
         or st.session_state['airspeed_type'] == "Equivalent Airspeed"):
        st.number_input(
            label="Value", min_value=0.0, format='%01.8g', step=1.0,
            key="airspeed"
        )

with col3:
    if st.session_state['airspeed_type'] == "Mach Number":
        pass
    elif (st.session_state['airspeed_type'] == "True Airspeed"
         or st.session_state['airspeed_type'] == "Calibrated Airspeed"
         or st.session_state['airspeed_type'] == "Equivalent Airspeed"):
        st.selectbox(
            "Unit",
            ("knots", "ft/s", "m/s"), key='airspeed_unit',
        )

# --------------------------------------
# Length Input
# --------------------------------------
st.subheader("Length")
col1, col2, col3 = st.columns(3)
with col1:
    st.selectbox(
        "Length type",
        ("Length", "Reynolds Number"), key='length_type',
    )

with col2:
    if st.session_state['length_type'] == "Length":
        st.number_input(
            label="Value", min_value=0.0, format='%01.8g', step=0.1, value=1.0,
            key="length", help="Characteristic length scale"
        )
    elif st.session_state['length_type'] == "Reynolds Number":
        st.number_input(
            label="Value", min_value=0.0, format='%01.8g', step=1e5,
            key="length", help="Characteristic length scale"
        )

with col3:
    if st.session_state['length_type'] == "Length":
        st.selectbox(
            "Unit",
            ("ft", "in", "m", "mm"), key='length_unit',
        )
    elif st.session_state['length_type'] == "Reynolds Number":
        pass


# --------------------------------------
# Output Flight Condition
# --------------------------------------
st.subheader("Output")
kwargs = {}
if st.session_state['altitude_type'] == "Geometric altitude":
    kwargs["h"] = st.session_state['h'] * unit(st.session_state['h_unit'])
elif st.session_state['altitude_type'] == "Geopotential altitude":
    kwargs["H"] = st.session_state['H'] * unit(st.session_state['H_unit'])

if st.session_state['airspeed_type'] == "Mach Number":
    kwargs["M"] = st.session_state['airspeed']
elif st.session_state['airspeed_type'] == "True Airspeed":
    kwargs["TAS"] = st.session_state['airspeed']\
        * unit(st.session_state["airspeed_unit"])
elif st.session_state['airspeed_type'] == "Calibrated Airspeed":
    kwargs["CAS"] = st.session_state['airspeed']\
        * unit(st.session_state["airspeed_unit"])
elif st.session_state['airspeed_type'] == "Equivalent Airspeed":
    kwargs["EAS"] = st.session_state['airspeed']\
        * unit(st.session_state["airspeed_unit"])

if st.session_state['length_type'] == "Length":
    kwargs["L"] = st.session_state['length']\
        * unit(st.session_state["length_unit"])
elif st.session_state['length_type'] == "Reynolds Number":
    kwargs["Re"] = st.session_state['length']

fc = FlightCondition(**kwargs)
out_txt = st.text(fc.tostring(full_output=True))
