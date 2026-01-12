import numpy as np
import sys,os
cur_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.dirname(cur_dir)
sys.path.append(parent_dir)
from equation_class.PDE_class import GL_equations_set


params={}
params['N']=12 #number of points in space
params['q_0']=2.*np.pi/3.9 #CDW wave vector
params['m_A']=1.
params['m_phi']=1. # should be similar to m_A

# Relative strenghts are important here
params['a']=-1.0
params['b']=0.02 
# when only a and b this terms gives  aditional modulation
# on top of the harmonic-oscillator type solution

#Coupling to the density gradient
params[f'c_A']=0#1
params[f'c_phi']=0#.1 # order of magniture smaller then the one for A
# I do not see a drastic change with c_i

#Damping 
params[f'Gamma_A']=0#.1
params[f'Gamma_phi']=0#.01 # order of magniture smaller then damping of A
# pulse strenght
params[f'kappa']=0.5

mid=params['N']//2
import itertools

for a_val,imp in list(itertools.product([-1.0,1.0],[f'0',f'-0.9 *exp(-(x-{mid})**2 )/(1**2)'])):
    #Impurity -> traps CDW and imprints a new node in CDW profile
    params['impurity']=imp
    params['a']=a_val
    # 'impurity' traps ("damps") oscillations at the impurity -> give a node to CDW


    mu,sig,pulse_max=10,0.25,5
    #Joule heating model
    #params['a']=f'-1.-5.*exp(-0.5*(t - {pulse_max})**2)'
    #params['a']=f'-1+ 10*exp(-(log(t+0.1)-{mu})**2/(2*{sig}**2))/((t+0.1)*{sig})' # for future

    GL_PDE=GL_equations_set(params,140,0.1,10)
    GL_PDE.set_driving(f'exp(-0.5*(t- {pulse_max})**2)*cos(2.*(t - {pulse_max}))')

    for ref in [True,False]:
        GL_PDE.set_init_state()
        GL_PDE.set_bc(A_0=0)
        a_val=params['a']
        out_name=f'Solutution_with_'
        for k,v in params.items():
            if k != 'impurity' or (k=='impurity' and v==f'0'):
                out_name += f'{k}_{v}_'
            else:
                out_name +=f'{k}_func_'

        if ref:
            GL_PDE.set_equations_ref()
            out_name+='_ref'
        else:
            GL_PDE.set_equations()

        print(GL_PDE.equations.rhs)
        res = GL_PDE.solve(file=f'{out_name}.hdmf5')
