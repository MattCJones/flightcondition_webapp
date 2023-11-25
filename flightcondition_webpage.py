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
if 'altitude_unit' not in st.session_state:
    st.session_state['altitude_unit'] = 'kft'

# Initialize unit selections
altitude_units = ("kft", "ft", "km", "m")
pressure_units = ("lbf/ft^2", "lbf/in^2", "kPa", "Pa", "inch_Hg",)
temperature_units = ("degR", "degC", "degK")
density_units = ("slug/ft^3", "kg/m^3")
mu_units = ("lbf s/ft^2", "N s/m^2")
nu_units = ("ft^2/s", "m^2/s")
k_units = ("ft slug/s^3/degR", "m kg/s^3/degK")
acceleration_units = ("ft/s^2", "m/s^2")

airspeed_units = ("knots", "ft/s", "m/s")
bylength_units = ("1/ft", "1/in", "1/m", "1/mm")

length_units = ("ft", "in", "m", "mm")

def _output_quantity(name, key, varname, units_arr, ind_US=0, ind_SI=1):
    col1, col2, col3 = st.columns(3)
    index_ = ind_US if (fc.units == "US") else ind_SI
    with col1:
        st.markdown(name)
    with col3:
        if units_arr is not None and units_arr[0] != "dimensionless":
            st.selectbox(f"label_{key}", units_arr, key=key, index=index_,
                         label_visibility="collapsed")
    with col2:
        # Convert output quantity to desired unit
        if units_arr is not None:
            if key not in st.session_state:
                st.session_state[key] = units_arr[index_]
            unit_ = st.session_state[key]
            st.text(f"{fc.asdict[varname].to(unit_).magnitude:8.5g}")
        else:  # layer name requires unique output
            st.text(f"{fc.layer.name}")


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
st.divider()


# --------------------------------------
# Altitude Input
# --------------------------------------
st.header("Input Flight Condition")
# st.subheader("Input Flight Condition")
col1, col2, col3 = st.columns(3)
with col1:
    st.selectbox(
        "Altitude Type",
        ("Geometric altitude", "Geopotential altitude", "Pressure altitude"),
        key='altitude_type',
    )

with col2:
    if (st.session_state['altitude_type'] == "Geometric altitude"
       or st.session_state['altitude_type'] == "Geopotential altitude"):
        st.number_input(
            label="Value", min_value=0.0, format='%01.8g', step=0.1, key='h',
        )
    elif st.session_state['altitude_type'] == "Pressure altitude":
        st.number_input(
            label="Value", min_value=0.0, format='%01.8g', step=0.1, key='p',
        )

with col3:
    if (st.session_state['altitude_type'] == "Geometric altitude"
       or st.session_state['altitude_type'] == "Geopotential altitude"):
        st.selectbox("Unit", altitude_units, key='altitude_unit')
    elif st.session_state['altitude_type'] == "Pressure altitude":
        st.selectbox("Unit", pressure_units,
                     key='altitude_unit')

# --------------------------------------
# Airspeed Input
# --------------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.selectbox(
        "Airspeed Type",
        ("Mach Number", "True Airspeed", "Calibrated Airspeed",
         "Equivalent Airspeed"), key='airspeed_type',
    )

with col2:
    if st.session_state['airspeed_type'] == "Mach Number":
        st.number_input(
            label="Value", min_value=0.0, format='%01.8g', step=0.05,
            value=0.5, key="airspeed",
        )
    elif (st.session_state['airspeed_type'] == "True Airspeed"
          or st.session_state['airspeed_type'] == "Calibrated Airspeed"
          or st.session_state['airspeed_type'] == "Equivalent Airspeed"):
        st.number_input(
            label="Value", min_value=0.0, format='%01.8g', step=1.0,
            key="airspeed",
        )

with col3:
    if st.session_state['airspeed_type'] == "Mach Number":
        pass
    elif (st.session_state['airspeed_type'] == "True Airspeed"
          or st.session_state['airspeed_type'] == "Calibrated Airspeed"
          or st.session_state['airspeed_type'] == "Equivalent Airspeed"):
        st.selectbox(
            "Unit",
            airspeed_units, key='airspeed_unit',
        )

# --------------------------------------
# Length Input
# --------------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.selectbox(
        "Length Type",
        ("Length", "Reynolds Number"), key='length_type',
    )

with col2:
    if st.session_state['length_type'] == "Length":
        st.number_input(
            label="Value", min_value=0.0, format='%01.8g', step=0.1, value=1.0,
            key="length",
        )
    elif st.session_state['length_type'] == "Reynolds Number":
        st.number_input(
            label="Value", min_value=0.0, format='%01.8g', step=1e5,
            key="length",
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
st.header("Output Quantities")
kwargs = {}
if st.session_state['altitude_type'] == "Geometric altitude":
    kwargs["h"] = st.session_state['h']\
        * unit(st.session_state['altitude_unit'])
elif st.session_state['altitude_type'] == "Geopotential altitude":
    kwargs["H"] = st.session_state['h']\
        * unit(st.session_state['altitude_unit'])
elif st.session_state['altitude_type'] == "Pressure altitude":
    kwargs["p"] = st.session_state['p']\
        * unit(st.session_state['altitude_unit'])

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

col1, col2, col3 = st.columns(3)
with col1:
    text_output = st.checkbox("Text Output", value=False,
                              help="Print text-formatted output",)
with col2:
    full_output = st.checkbox("Full Output", value=True,
                              help="Print full set of quantities",)
    fc.full_output = full_output
with col3:
    # units = st.selectbox("Unit System", ("US", "SI"))
    units = st.radio("Unit System", ["US", "SI"], horizontal=True,
                     label_visibility="visible")
    fc.units = units

if text_output:
    st.text(fc.tostring())
else:
    # - - - - - - - - - - - - - - - - - - -
    # Altitude
    # - - - - - - - - - - - - - - - - - - -
    st.subheader("Altitude-based")

    _output_quantity(name="Geometric altitude", key='out_h_unit', varname='h',
                     units_arr=altitude_units, ind_SI=2)
    if fc.full_output:
        _output_quantity(name="Geopotential altitude", key='out_H_unit',
                         varname='H', units_arr=altitude_units, ind_SI=2)
    _output_quantity(name="Pressure", key='out_p_unit', varname='p',
                     units_arr=pressure_units, ind_SI=2)
    _output_quantity(name="Temperature", key='out_T_unit', varname='T',
                     units_arr=temperature_units, ind_SI=2)
    _output_quantity(name="Density", key='out_rho_unit', varname='rho',
                     units_arr=density_units, ind_SI=1)
    _output_quantity(name="Sound speed", key='out_a_unit', varname='a',
                     units_arr=airspeed_units, ind_SI=2)
    if fc.full_output:
        _output_quantity(name="Dynamic viscosity", key='out_mu_unit',
                         varname='mu', units_arr=mu_units, ind_SI=1)
    _output_quantity(name="Kinematic viscosity", key='out_nu_unit',
                     varname='nu', units_arr=nu_units, ind_SI=1)
    if fc.full_output:
        _output_quantity(name="Thermal conductivity", key='out_k_unit',
                         varname='k', units_arr=k_units, ind_SI=1)
        _output_quantity(name="Gravity", key='out_g_unit',
                         varname='g', units_arr=acceleration_units, ind_SI=1)
        _output_quantity(name="Mean Free Path", key='out_MFP_unit',
                         varname='MFP', units_arr=length_units, ind_US=1,
                         ind_SI=3)
        _output_quantity(name="Layer name", key='out_name_unit',
                         varname='name', units_arr=None, ind_SI=2)

    # - - - - - - - - - - - - - - - - - - -
    # Airspeed
    # - - - - - - - - - - - - - - - - - - -
    st.subheader("Airspeed-based")
    _output_quantity(name="Mach Number", key='out_M_unit', varname='M',
                     units_arr=("dimensionless",), ind_SI=0)
    _output_quantity(name="True Airspeed", key='out_TAS_unit', varname='TAS',
                     units_arr=airspeed_units, ind_SI=2)
    _output_quantity(name="Calibrated Airspeed", key='out_CAS_unit',
                     varname='CAS', units_arr=airspeed_units, ind_SI=2)
    _output_quantity(name="Equivalent Airspeed", key='out_EAS_unit',
                     varname='EAS', units_arr=airspeed_units, ind_SI=2)
    if fc.full_output:
        _output_quantity(name="Dynamic pressure", key='out_q_inf_unit',
                         varname='q_inf', units_arr=pressure_units, ind_SI=2)
        _output_quantity(name="Impact pressure", key='out_q_c_unit',
                         varname='q_c', units_arr=pressure_units, ind_SI=2)
        _output_quantity(name="Stagnation pressure", key='out_p0_unit',
                         varname='p0', units_arr=pressure_units, ind_SI=2)
        _output_quantity(name="Stagnation temperature", key='out_T0_unit',
                         varname='T0', units_arr=temperature_units, ind_SI=2)
        _output_quantity(name="Recovery temperature (laminar)",
                         key='out_Tr_lamr_unit', varname='Tr_lamr',
                         units_arr=temperature_units, ind_SI=2)
        _output_quantity(name="Recovery temperature (turbulent)",
                         key='out_Tr_turb_unit', varname='Tr_turb',
                         units_arr=temperature_units, ind_SI=2)
    _output_quantity(name="Reynolds Number per length",
                     key='out_Re_by_L_unit', varname='Re_by_L',
                     units_arr=bylength_units, ind_US=0, ind_SI=2)

    # - - - - - - - - - - - - - - - - - - -
    # Length
    # - - - - - - - - - - - - - - - - - - -
    st.subheader("Length-based")
    _output_quantity(name="Length scale", key='out_L_unit',
                     varname='L', units_arr=length_units, ind_SI=2)
    _output_quantity(name="Reynolds Number", key='out_Re_unit', varname='Re',
                     units_arr=("dimensionless",), ind_SI=0)
    if fc.full_output:
        _output_quantity(name="Boundary layer thickness (laminar)",
                         key='out_h_BL_lamr_unit', varname='h_BL_lamr',
                         units_arr=length_units, ind_US=1, ind_SI=3)
        _output_quantity(name="Boundary layer thickness (turbulent)",
                         key='out_h_BL_turb_unit', varname='h_BL_turb',
                         units_arr=length_units, ind_US=1, ind_SI=3)
        _output_quantity(name="Skin friction coefficient (laminar)",
                         key='out_Cf_lamr_unit', varname='Cf_lamr',
                         units_arr=("dimensionless",), ind_SI=0)
        _output_quantity(name="Skin friction coefficient (turbulent)",
                         key='out_Cf_turb_unit', varname='Cf_turb',
                         units_arr=("dimensionless",), ind_SI=0)
        _output_quantity(name="Wall distance to $y^+=1$",
                         key='out_h_yplus1_unit', varname='h_yplus1',
                         units_arr=length_units, ind_US=1, ind_SI=3)
