import streamlit as st
import numpy as np
import os,sys
curr_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(curr_dir))
import numpy as np
from equation_class.GL_equations_params import params_name_dict


# run_button functionalities ##
def restart_run_button():
    st.session_state.run_button_active=True
def disable_run_button():
    st.session_state.run_button_active=False
    st.session_state.run_calc=True

def restart_to_file():
    restart_run_button()
    st.session_state.to_file =not st.session_state.to_file

@st.fragment
def sidebar_content(params: dict[str,float|str]):
    with st.expander('model parameters'):
        for k,v in list(params_name_dict.items())[:-2]:
            slider=st.select_slider(v[0],options=[x for x in v[1]],value=v[2],format_func=lambda x: f'{x:.2f}',on_change=restart_run_button)
            params[k]=slider
            
    for k,v in list(params_name_dict.items())[-2:]:
        slider=st.select_slider(v[0],options=[x for x in v[1]],value=v[2],format_func=lambda x: f'{x:.2f}',on_change=restart_run_button)
        params[k]=slider

    with st.expander('impurity'):
        # store the value so that its not reset after N is changed
        if 'imp_loc' not in st.session_state:
            st.session_state.imp_loc=round(0.5*params['N'],1)
        
        imp_loc=st.multiselect(
            "Choose impurity/s location/s",
            options=np.arange(0,params['N'],0.1),
            placeholder="x location(s)",
            format_func=lambda x: f'{x:.1f}',
            accept_new_options=True,
            default=[round(params['N']//2,1)],
            on_change=restart_run_button
        )
        imp_stength=st.select_slider('Impurity strength',options=np.arange(-200,200,1),value=125,format_func=lambda x: f'{x:.2f}',on_change=restart_run_button)
        if imp_loc:
            imp_str=''.join([f'-{imp_stength} *exp(-(x-{imp_x})**2 )/(1**2)' for imp_x in imp_loc])
        else:
            imp_str='0'
        params['impurity']=imp_str

    with st.expander('Driving'):
        driving_str=st.select_slider('Pulse strength',options=np.arange(-1., 1.1, 0.1),value=0.,format_func=lambda x: f'{x:.2f}',on_change=restart_run_button)
        # store the value so that its not reset after t_max is changed
        if 'pulse_max' not in st.session_state:
            st.session_state.pulse_max=0.
        pulse_max=st.select_slider('Pulse time',options=np.arange(0,params['t_max'],0.1),
            value=round(st.session_state.pulse_max,1),format_func=lambda x: f'{x:.2f}',on_change=restart_run_button)
        st.session_state.pulse_max=pulse_max 

        params['driving']=f'{driving_str}*exp(-0.5*(t- {pulse_max})**2)*cos(2.*(t - {pulse_max}))'
        
        add_Joule=st.toggle('Joule heating',value=False,on_change=restart_run_button)
        params['Joule']=add_Joule
    
    st.session_state.to_file=st.toggle('Save results directly to file',value=False,on_change=restart_to_file,
                                       help='Preferred for larger calculations, but can be problematic on free domains')

    

    #Run Calc button
    if st.button('Run Simulation',width='stretch',type='primary',disabled=not st.session_state.run_button_active,on_click=disable_run_button):
        st.rerun()

