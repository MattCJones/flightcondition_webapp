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

from flightcondition import FlightCondition


# Build webpage
st.title("Flight Condition Calculator")
st.text("Compute common flight condition quantities and airspeed conversions.")

left_column, right_column = st.columns(2)

with left_column:
    st.subheader("User Input")

with right_column:
    st.subheader("Output")
