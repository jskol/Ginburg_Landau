import streamlit as st
import os,sys
curr_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(curr_dir)
import numpy as np
from equation_class.GL_equations_params import params_name_dict


# run_button functionalities #####
if 'run_button_active' not in st.session_state:
    st.session_state.run_button_active=True
def restart_run_button():
    st.session_state.run_button_active=True

if 'run_calc' not in st.session_state:
    st.session_state.run_calc=False
def disable_run_button():
    st.session_state.run_button_active=False
    st.session_state.run_calc=True
############################################

# Create sidebar content as st.fragement
# this way any change there doesnt force the
# full reload of the page just this fragment
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
        imp_loc=st.select_slider('Impurity location',options=np.arange(0,params['N'],0.1),value=round(0.5*params['N'],1),on_change=restart_run_button)
        imp_stength=st.select_slider('Impurity strength',options=np.arange(0,1,0.1),value=0,format_func=lambda x: f'{x:.2f}',on_change=restart_run_button)
        params['impurity']=f'-{imp_stength} *exp(-(x-{imp_loc})**2 )/(1**2)'

    with st.expander('Driving'):
        driving_str=st.select_slider('Pulse strength',options=np.arange(-1., 1.1, 0.1),value=0.,format_func=lambda x: f'{x:.2f}',on_change=restart_run_button)
        pulse_max=st.select_slider('Pulse time',options=np.arange(0,params['t_max'],params['t_max']*0.1),value=0.,format_func=lambda x: f'{x:.2f}',on_change=restart_run_button)
        params['driving']=f'{driving_str}*exp(-0.5*(t- {pulse_max})**2)*cos(2.*(t - {pulse_max}))'
        
        add_Joule=st.toggle('Joule heating',value=False,on_change=restart_run_button)
        params['Joule']=add_Joule
    
    #Run Calc button
    if st.button('Run Simulation',width='stretch',type='primary',disabled=not st.session_state.run_button_active,on_click=disable_run_button):
        st.rerun()



## Create a sidebar to set the parameters of the model
with st.sidebar:
    params={} #initiate empty dict of params
    sidebar_content(params)

## Now the main page
#Title
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>G-L simulation</h1>", unsafe_allow_html=True)

#initiate Solver for PDE
from equation_class.PDE_class import GL_equations_set
GL_PDE=GL_equations_set(params,params['t_max'],0.1,10) #create instance
GL_PDE.set_driving(params['driving']) # update driving pulse
#Set boundary conditions
A0=np.sqrt(-params['a']/(2.*params['b'])) if params['a']<0 and params['b']!= 0 else 0
GL_PDE.set_bc(A_0=A0)
#set initial state
shift = 0.1  if A0==0 else 0.1
GL_PDE.set_init_state(f'{A0}-0.005*({A0}+{shift})*sin(x*{np.pi}/{params["N"]})')
if params['Joule']:
    params['a']=f'{params["a"]}*(1-{params["driving"]})'
#define equations
GL_PDE.set_equations()

#Solve the thing
if 'has_data' not in st.session_state:
    st.session_state.has_data=False


#if st.sidebar.button('Run Simulation',width='stretch',type='primary',disabled=not st.session_state.run_button_active,on_click=disable_run_button):
#    #st.session_state.run_button_active=False
#    with st.spinner('Calculating',width='stretch'):
#        st.session_state.PDE_res = GL_PDE.solve()
#    st.session_state.has_data=True
if st.session_state.run_calc:
    with st.spinner('Calculating',width='stretch'):
        st.session_state.PDE_res = GL_PDE.solve()
    st.session_state.has_data=True
    st.session_state.run_calc=False


if st.session_state.has_data:
    from Streamlit_funcs.save_button import generate_save_button,generate_download_button
    from Streamlit_funcs.time_evolution import add_time_evolution_slider
    add_time_evolution_slider(st.session_state.PDE_res) # show the time evolution
    generate_download_button(st.session_state.PDE_res) # allow for downloading -> button





