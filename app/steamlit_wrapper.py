import streamlit as st
import numpy as np
import os,sys
curr_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(curr_dir)



#Solve the thing
#run the calculations only if triggered
if 'run_calc' not in st.session_state:
    st.session_state.run_calc=False
    
if 'to_file' not in st.session_state:
    st.session_state.to_file=False

if 'has_data' not in st.session_state:
    st.session_state.has_data=False

if 'needs_rerun' not in st.session_state:
    st.session_state.needs_rerun=False

## Create a sidebar to set the parameters of the model
from Streamlit_funcs.sidebar_content import sidebar_content,download_sidebar
with st.sidebar:
    params={} #initiate empty dict of params
    if 'run_button_active' not in st.session_state:
        st.session_state.run_button_active=True
    sidebar_content(params)

## Now the main page
#Title
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>G-L simulation</h1>", unsafe_allow_html=True)

#initiate Solver for PDE
from Streamlit_funcs.init_PDE import init_PDE,SimDetails

simulation_details=SimDetails(t_step=0.1,x_points_per_unit=10)
GL_PDE=init_PDE(params,simulation_details)
out_name='out.hdmf5'




if st.session_state.run_calc or st.session_state.needs_rerun:
    with st.spinner('Calculating',width='stretch'):
        # Remove the existing "old data"
        if os.path.exists(out_name):
            os.remove(out_name)

        st.session_state.PDE_res = GL_PDE.solve(to_file=st.session_state.to_file)
    st.session_state.has_data=True
    st.session_state.run_calc=False
    st.session_state.needs_rerun=False
    
with st.sidebar:
    download_sidebar()


tab_time_evolution,tab_FT,tab_CDW = st.tabs(['Time evolution sample','Time evolution local','Charge density'])
from Streamlit_funcs.Sample_tab import display_time_evolution_sample
with tab_time_evolution:
    display_time_evolution_sample(simulation_details)

from Streamlit_funcs.Local_evolution_tab import display_time_evolution_local
with tab_FT:
    display_time_evolution_local(simulation_details)


from Streamlit_funcs.Charge_density_tab import CDW_tab
with tab_CDW:
    CDW_tab(params,simulation_details)

