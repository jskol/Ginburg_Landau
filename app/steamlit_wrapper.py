import streamlit as st
import os,sys
curr_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(curr_dir)
import numpy as np
from equation_class.GL_equations_params import params_name_dict


## Create a sidebar to set the parameters of the model
params={} #initiate empty dict of params
with st.sidebar:
    with st.expander('model parameters'):
        for k,v in list(params_name_dict.items())[:-2]:
            slider=st.select_slider(v[0],options=[x for x in v[1]],value=v[2],format_func=lambda x: f'{x:.2f}')
            params[k]=slider

    for k,v in list(params_name_dict.items())[-2:]:
        slider=st.select_slider(v[0],options=[x for x in v[1]],value=v[2],format_func=lambda x: f'{x:.2f}')
        params[k]=slider

    with st.expander('impurity'):
        imp_loc=st.select_slider('Impurity location',options=np.arange(0,params['N'],0.1),value=round(0.5*params['N'],1))
        imp_stength=st.select_slider('Impurity strength',options=np.arange(0,1,0.1),value=0,format_func=lambda x: f'{x:.2f}')
        params['impurity']=f'-{imp_stength} *exp(-(x-{imp_loc})**2 )/(1**2)'

    with st.expander('Driving'):
        driving_str=st.select_slider('Pulse strength',options=np.arange(-1., 1.1, 0.1),value=0.,format_func=lambda x: f'{x:.2f}')
        pulse_max=st.select_slider('Pulse time',options=np.arange(0,params['t_max'],params['t_max']*0.1),value=0.,format_func=lambda x: f'{x:.2f}')

        add_Joule=st.toggle('Joule heating',value=False)


## Now the main page
#Title
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>G-L simulation</h1>", unsafe_allow_html=True)

#initiate Solver for PDE
from equation_class.PDE_class import GL_equations_set
GL_PDE=GL_equations_set(params,params['t_max'],0.1,10)
GL_PDE.set_driving(f'{driving_str}*exp(-0.5*(t- {pulse_max})**2)*cos(2.*(t - {pulse_max}))')
A0=np.sqrt(-params['a']/(2.*params['b'])) if params['a']<0 and params['b']!= 0 else 0
GL_PDE.set_bc(A_0=A0)
shift = 0.1  if A0==0 else 0.1
GL_PDE.set_init_state(f'{A0}-0.05*({A0}+{shift})*sin(x*{np.pi}/{params["N"]})')
if add_Joule:
    params['a']=f'{params["a"]}*(1-{driving_str}*exp(-0.5*(t - {pulse_max})**2))'

GL_PDE.set_equations()

#Solve the thing

if 'PDE_res' not in st.session_state:
    st.session_state.PDE_res=None

left,center,right=st.columns(3)
if center.button('Run Simulation',width='stretch'):
    with center.spinner('Calculating',width='stretch'):
        st.session_state.PDE_res = GL_PDE.solve()

    from Streamlit_funcs.save_button import generate_save_button,generate_download_button
    from Streamlit_funcs.time_evolution import add_time_evolution_slider
    add_time_evolution_slider(st.session_state.PDE_res) # show the time evolution
    generate_download_button(st.session_state.PDE_res) # allow for downloading -> button





