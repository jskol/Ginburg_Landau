import streamlit as st
import sys,os


from Streamlit_funcs.save_button import generate_save_button,generate_download_button
from Streamlit_funcs.time_evolution import add_time_evolution_slider
from Streamlit_funcs.init_PDE import SimDetails

def display_time_evolution_sample(simulation_details:SimDetails):
    # Show the data if exists
    if 'has_data' not in st.session_state:
        st.session_state.has_data=False
    if st.session_state.has_data:
        add_time_evolution_slider(st.session_state.PDE_res,simulation_details) # show the time evolution
        generate_download_button(st.session_state.PDE_res) # allow for downloading -> button