import streamlit as st
import pde
from typing import Any
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import os,sys
curr_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(curr_dir)
from init_PDE import SimDetails



def create_layout(sys_size:int,solutions_to_showcase:dict[str,int]):    
    iter_to_keys=iter(solutions_to_showcase)
    
    return {
        "plot_bgcolor":"#FBFAFA",
        "showlegend":False,
        #Common x-axis for all subplots
        "xaxis": dict(
            range=[0,sys_size], 
            autorange=False, 
            showgrid=False,
            fixedrange=True
        ),
        "yaxis":dict( 
            title=next(iter_to_keys),
            autorange=True, 
            showgrid=False,
            fixedrange=False
        ),
        "yaxis2":dict( 
            title=next(iter_to_keys),
            #range=[-np.pi,np.pi],
            autorange=True, 
            showgrid=False,
            fixedrange=False
        ),
        "autosize": True,
        "margin": {"t":25,"b":1 },
        "height": 800,  # Dodaj to, aby subploty miały gdzie "oddychać"
        "plot_bgcolor":"#FBFAFA",
    }




def add_time_evolution_slider(data_PDE:pde.storage.memory.MemoryStorage,sim_details:SimDetails)->None:
    '''
    Docstring for add_time_evolution_slider
    This function creates a plotly slider figure 
    for the time evolution of the set of PDEs
    where a user can slide through times to analyze the 
    behaviour

    :param data: Solution of PDE
    :type data: pde.storage.memory.MemoryStorage
    '''
    st.latex(r'')
    solutions_to_showcase={
        r"$A(x,t)$":0,
        r"$phi(x,t)$":1
    }

    fig=make_subplots(rows=2,cols=1,shared_xaxes=True,vertical_spacing=0.05)
    x_axis=np.arange(data_PDE.data[0].shape[-1])/sim_details.x_points_per_unit

    for solution in solutions_to_showcase.values():
        fig.add_trace(go.Scatter(x=x_axis, y=data_PDE.data[0][solution], mode="lines+markers"), row=1+solution, col=1)
    
    #Generate frames with data -> Sublplot structure is not important
    #frames will feed the "initialized" fig structure

    frames={}
    for time_step,data_set in zip(data_PDE.times,data_PDE.data):
        frame_name=f"{time_step:.1f}"
        frames[frame_name]=go.Frame(
                data=[
                    go.Scatter(x=x_axis,y=data_set[sol]) for sol in solutions_to_showcase.values()
                ],
                name=frame_name
            )
    
    fig.frames = list(frames.values())

    steps = []
    for k in frames.keys():
        step = dict(
            method="animate",
            label=k,
            args=[
                [k],
                dict(
                    mode="immediate",
                    frame=dict(duration=0, redraw=False),
                    transition=dict(duration=0)
                )
            ]            
        )
        steps.append(step)

    sliders = [dict(active=0, currentvalue={"prefix": "time: "}, steps=steps)]
    layout=create_layout(sys_size=x_axis[-1],solutions_to_showcase=solutions_to_showcase)
    fig.update_layout(sliders=sliders, **layout)
    
    st.plotly_chart(fig,width='stretch',config={'responsive': True})

