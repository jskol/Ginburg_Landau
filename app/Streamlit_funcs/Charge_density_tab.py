import streamlit as st
import numpy as np
import plotly.graph_objects as go

import os,sys
curr_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(curr_dir)
from init_PDE import SimDetails

@st.fragment
def CDW_tab(params:dict[str, float|str],simulation_details:SimDetails):
    if st.session_state.has_data:
        data_PDE=np.array(st.session_state.PDE_res.data)
        t_range=np.array(st.session_state.PDE_res.times)
        x_range=np.arange(data_PDE[0].shape[-1])/simulation_details.x_points_per_unit


        time_stamp=int(st.select_slider('Time',options=t_range,value=0,format_func=lambda x: f'{x:.2f}')/simulation_details.t_step)

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

        locations=st.multiselect(
            "Choose location/s",
            options=np.arange(0,params['N'],round(1/simulation_details.x_points_per_unit,1)),
            placeholder="x location(s)",
            format_func=lambda x: f'{x:.1f}',
            accept_new_options=True,
            default=[round(params['N']//2,1)],
        )
        fig2=go.Figure(
            data=[go.Scatter(
                x=t_range,y=data_PDE[:,0,loc]*np.cos(params['q_0']*loc/simulation_details.x_points_per_unit +data_PDE[:,1,loc])
            ) for loc in list(map(lambda x: int(x*simulation_details.x_points_per_unit),locations))],
            layout=(
                dict(
                    plot_bgcolor="#FBFAFA",
                    xaxis=dict(title='t',range=[t_range[0],t_range[-1]]),
                    yaxis=dict(title='rho(x,t)'),
                    margin={"t":25,"b":1}
                    )
                )
        )
        st.plotly_chart(fig2)


