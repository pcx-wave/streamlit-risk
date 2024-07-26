# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 17:30:04 2024

@author: USER
"""

import streamlit as st

st.title('Risk-On/Risk-Off Environment Simulator')

# Input sliders for indicators
interest_rate = st.slider('Interest Rate Impact', -1.0, 1.0, 0.0)
consumer_confidence = st.slider('Consumer Confidence Impact', -1.0, 1.0, 0.0)
gdp_growth = st.slider('GDP Growth Impact', -1.0, 1.0, 0.0)

# Calculate composite score
indicators = {
    'Interest Rates': interest_rate,
    'Consumer Confidence': consumer_confidence,
    'GDP Growth': gdp_growth
}
weights = {'Interest Rates': 0.5, 'Consumer Confidence': 0.3, 'GDP Growth': 0.2}
score = sum(indicators[i] * weights[i] for i in indicators)

# Display result
if score > 0:
    st.write('Risk-On Environment')
else:
    st.write('Risk-Off Environment')
