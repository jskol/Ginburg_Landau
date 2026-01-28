import streamlit as st
import os,sys
curr_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(curr_dir)
from equation_class.GL_equations_params import params_name_dict


## Create a sidebar to set the parameters of the model
params={} #initiate empty dict of params
with st.sidebar:
    for k,v in params_name_dict.items():
        slider=st.select_slider(v[0],options=[x for x in v[1]],value=v[2])
        params[k]=slider

## Now the main page

st.title('G-L simulation')
from equation_class.PDE_class import GL_equations_set
params['impurity']='0'
#mu,sig,pulse_max=10,0.25,5
#Joule heating model
#params['a']=f'-1.-5.*exp(-0.5*(t - {pulse_max})**2)'
#params['a']=f'-1+ 10*exp(-(log(t+0.1)-{mu})**2/(2*{sig}**2))/((t+0.1)*{sig})' # for future

GL_PDE=GL_equations_set(params,params['t_max'],0.1,10)
GL_PDE.set_driving(f'0')#f'exp(-0.5*(t- {pulse_max})**2)*cos(2.*(t - {pulse_max}))')
GL_PDE.set_init_state()
GL_PDE.set_bc(A_0=0)
GL_PDE.set_equations()

print(GL_PDE.equations.rhs)
res = GL_PDE.solve()
from Streamlit_funcs.save_button import generate_save_button
generate_save_button(res)





