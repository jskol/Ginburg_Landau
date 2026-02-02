import streamlit as st
import numpy as np
import plotly.graph_objects as go

import os,sys
curr_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(curr_dir)
from init_PDE import sym_details

@st.fragment
def CDW_tab(params:dict[str, float|str],simulation_details:sym_details):
    if st.session_state.has_data:
        data_PDE=np.array(st.session_state.PDE_res.data)
        t_range=np.array(st.session_state.PDE_res.times)
        x_range=np.arange(data_PDE[0].shape[-1])/sym_details.x_points_per_unit


        time_stamp=int(st.select_slider('Time',options=t_range,value=0,format_func=lambda x: f'{x:.2f}')/sym_details.t_step)

        fig=go.Figure( 
                go.Scatter(
                    x=x_range,y=data_PDE[time_stamp,0,:]*np.cos(params['q_0']*x_range +data_PDE[time_stamp,1,:]),
                    mode='lines+markers'
                )
                ,
                layout=(
                dict(
                    plot_bgcolor="#FBFAFA",
                    xaxis=dict(title='x',range=[x_range[0],x_range[-1]]),
                    yaxis=dict(title='rho(x,t)'),
                    margin={"t":25,"b":1}
                    )
                )
        )
        st.plotly_chart(fig)