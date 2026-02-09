import os,sys
import numpy as np
from dataclasses import dataclass 
curr_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(curr_dir))
from equation_class.PDE_class import GL_equations_set

@dataclass
class SimDetails:
    t_step:float=0.1
    x_points_per_unit:int=10


def init_PDE(params:dict[str, float|str],sym_details: SimDetails):

    GL_PDE=GL_equations_set(params,params['t_max'],sym_details.t_step,sym_details.x_points_per_unit) #create instance
    GL_PDE.set_driving(str(params['driving'])) # update driving pulse
    #Set boundary conditions
    A0=np.sqrt(-float(params['a'])/(2.*float(params['b']))) if float(params['a'])<0 and params['b']!= 0 else 0
    GL_PDE.set_bc(A_0=A0)
    #set initial state
    shift = 0.1  if A0==0 else 0.1
    GL_PDE.set_init_state(f'{A0}-0.005*({A0}+{shift})*sin(x*{np.pi}/{params["N"]})')
    if params['Joule']:
        params['a']=f'{params["a"]}*(1-{params["driving"]})'
    #define equations
    GL_PDE.set_equations()
    return GL_PDE