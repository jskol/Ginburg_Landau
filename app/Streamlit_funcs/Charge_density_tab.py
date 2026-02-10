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

        st.header('Local charge-denisty evolutuion')
        locations=st.multiselect(
            "Choose location/s",
            options=np.arange(0,params['N'],round(1/simulation_details.x_points_per_unit,1)),
            placeholder="x location(s)",
            format_func=lambda x: f'{x:.1f}',
            accept_new_options=True,
            default=[round(params['N']//2,1)],key='location'
        )
        fig2=go.Figure(
            data=[go.Scatter(
                x=t_range,y=data_PDE[:,0,loc]*np.cos(params['q_0']*loc/simulation_details.x_points_per_unit +data_PDE[:,1,loc]),
                name=f'x={(loc/simulation_details.x_points_per_unit):.1f}'
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



        st.header('Fourier Transorm of the signal',divider=True,text_alignment='center') 
        time_ranges=st.multiselect(
            "Choose t_periods",
            options=t_range,
            placeholder="Picked t's",
            format_func=lambda x: f'{x:.2f}',
            accept_new_options=True,
            default=[t_range[0],t_range[-1]],
            key='time'
        )
        layout_for_FT=dict(
                    plot_bgcolor="#FBFAFA",
                    xaxis=dict(title='omega'),
                    margin={"t":25,"b":1}
                )

    time_ranges.sort()
    t_init=time_ranges[0]
    t_init_loc=np.argwhere(np.abs(t_range-t_init)<1e-5)[0][0]
    
    x_vals= list(map(lambda x: int(x*simulation_details.x_points_per_unit),locations))
    for t_end in time_ranges[1:]:
        st.subheader(f'F.T transform from {t_init:.3f}-{t_end:.3f}',text_alignment='center',divider=True)
        st.divider(width='stretch')
        cols=st.columns(2)
        t_end_loc=np.argwhere(np.abs(t_range-t_end)<1e-5)[0][0]            
            
        FT_data=np.array([np.fft.fft(
            data_PDE[t_init_loc:t_end_loc,0,x_loc]*np.cos(params['q_0']*x_loc/simulation_details.x_points_per_unit +data_PDE[t_init_loc:t_end_loc,1,x_loc])
            ) for x_loc in x_vals])
        omega_range=np.arange(len(FT_data[0])//2)

        def create_fig_data(func,data_set,points_set):
            '''
            Wrapper function to plot lines
            func: is either np.real or np.imag for
            the case I'm using
            '''
            return [
                go.Scatter(
                    x=omega_range,y=(func)(data_subset),
                    mode='lines+markers',name=f'x={(points_set[temp_it]):.2f}'
                ) for temp_it,data_subset in enumerate(data_set)

            ]
            
        fig_re=go.Figure(
            data=create_fig_data(lambda x: np.real(x), FT_data,x_vals),
            layout=layout_for_FT
        )
        fig_re.update_layout({"yaxis":dict(title=r'$Re\rho(x,\omega)$')})
        fig_im=go.Figure(
            data=create_fig_data(lambda x: np.abs(np.imag(x)),FT_data,x_vals),
            layout=layout_for_FT
        )
        fig_im.update_layout({"yaxis":dict(title=r'-$Im\rho(x,\omega)$')})
        with cols[0]:
            st.subheader('Real Part',text_alignment='center')
            st.plotly_chart(fig_re,width='stretch',config={'responsive': True},key=f're_FFT_{t_init:.3f}_{t_end:.3f}_{t_end_loc}_{x_vals}')
        with cols[1]:                
            st.subheader('Imaginary Part',text_alignment='center')
            st.plotly_chart(fig_im,width='stretch',config={'responsive': True},key=f'im_FFT_{t_init:.3f}_{t_end:.3f}_{t_end_loc}_{x_vals}')

        t_init,t_init_loc=t_end,t_end_loc


