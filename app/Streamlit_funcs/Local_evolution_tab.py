import plotly.graph_objects as go
import streamlit as st
import numpy as np
import pde

@st.fragment
def display_time_evolution_local():

    if st.session_state.has_data:
        data_PDE=np.array(st.session_state.PDE_res.data)
        t_range=np.array(st.session_state.PDE_res.times)
       
        st.header('Evolution of the space-resolved profile',divider=True,text_alignment='center')
        st.text(f'Impurity is at x={st.session_state.imp_loc}')
        r_space_locations=np.arange(data_PDE[0].shape[-1])

        tickers = st.multiselect(
            "Choose x locations to display",
            options=r_space_locations,
            placeholder="Pick x's",
            accept_new_options=True,
            default=[0,r_space_locations[len(r_space_locations)//2]]
        )
        cols=st.columns(2)
        for it, data_name in enumerate([r'$A(x,t)$',r'$\phi(x,t)$']):
            fig=go.Figure(
                data=[ 
                    go.Scatter(
                        x=t_range,y=data_PDE[:,it,x_loc],
                        mode='lines+markers',name=f'x={x_loc}'
                    
                    ) for x_loc in tickers
                ],
                layout=(
                    dict(
                        plot_bgcolor="#FBFAFA",
                        yaxis=dict(title=data_name),
                        xaxis=dict(title='time',range=[t_range[0],t_range[-1]]),
                        margin={"t":25,"b":1}
                        )
                )
                )
            cols[it].plotly_chart(fig,width='stretch',config={'responsive': True})
       
        #FT-part
        st.header('Fourier Transorm of the signal',divider=True,text_alignment='center') 
        time_ranges=st.multiselect(
            "Choose t_periods",
            options=t_range,
            placeholder="Picked t's",
            accept_new_options=True,
            default=[t_range[0],t_range[-1]]
        )
        layout_for_FT=dict(
                    plot_bgcolor="#FBFAFA",
                    xaxis=dict(title='omega'),
                    margin={"t":25,"b":1}
                )

        time_ranges.sort()
        t_init=time_ranges[0]
        t_init_loc=np.argwhere(np.abs(t_range-t_init)<1e-5)[0][0]
        for t_end in time_ranges[1:]:
            st.subheader(f'F.T transform from {t_init:.3f}-{t_end:.3f}',text_alignment='center',divider=True)
            st.divider(width='stretch')
            cols=st.columns(2)
            t_end_loc=np.argwhere(np.abs(t_range-t_end)<1e-5)[0][0]            
            for it, data_name in enumerate([r'$A(x,\omega)$',r'$\phi(x,\omega)$']):                
                with cols[it].container(border=True) as cont:
                    #Calculate FFT once and then post-process it
                    FT_data=np.array([np.fft.fft(data_PDE[t_init_loc:t_end_loc,it,x_loc]) for x_loc in tickers])
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
                                mode='lines+markers',name=f'x={points_set[temp_it]}'
                            ) for temp_it,data_subset in enumerate(data_set)

                        ]
                    
                    fig_re=go.Figure(
                        data=create_fig_data(lambda x: np.real(x), FT_data,tickers),
                        layout=layout_for_FT
                    )
                    fig_re.update_layout({"yaxis":dict(title=f'Re({data_name})')})
                    fig_im=go.Figure(
                        data=create_fig_data(lambda x: -np.imag(x),FT_data,tickers),
                        layout=layout_for_FT
                    )
                    fig_im.update_layout({"yaxis":dict(title=f'-Im({data_name})')})
                    
                    st.subheader('Real Part',text_alignment='center')
                    st.plotly_chart(fig_re,width='stretch',config={'responsive': True},key=f're_FFT_{t_init:.3f}_{t_end:.3f}_{it}_{data_name}')
                    st.subheader('Imaginary Part',text_alignment='center')
                    st.plotly_chart(fig_im,width='stretch',config={'responsive': True},key=f'im_FFT_{t_init:.3f}_{t_end:.3f}_{it}_{data_name}')

            t_init,t_init_loc=t_end,t_end_loc