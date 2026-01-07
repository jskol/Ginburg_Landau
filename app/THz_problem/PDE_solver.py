import numpy as np
import sys,os
cur_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.dirname(cur_dir)
sys.path.append(parent_dir)
from equation_class.PDE_class import GL_equations_set


params={}
params['N']=8 #number of points in space
params['q_0']=2.*np.pi/4. #CDW wave vector
params['m_A']=1.
params['m_phi']=1. # should be similar to m_A

# Relative strenghts are important here
params['a']=1
params['b']=0.2   

#Impurity
mid=params['N']//2
params['impurity']=f'-0.9 *exp(-(x-{mid})**2 )/(1**2)'

#Coupling to the density gradient
params[f'c_A']=1
params[f'c_phi']=0.1 # order of magniture smaller then the one for A
#Damping 
params[f'Gamma_A']=1.
params[f'Gamma_phi']=0.1 # order of magniture smaller then damping of A
# pulse strenght
params[f'kappa']=0.5


mu=10
sig=0.25
params['a']='-1.-5.*exp(-0.5*(t - 13)**2)'
#f'-1+ 10*exp(-(log(t+0.1)-{mu})**2/(2*{sig}**2))/((t+0.1)*{sig})'
GL_PDE=GL_equations_set(params,100,0.1,8,80)
pulse_max=10
GL_PDE.set_driving(f'exp(-0.5*(t- {pulse_max})**2)*cos(2.*(t - {pulse_max}))')



GL_PDE.set_init_state()
GL_PDE.set_bc()
GL_PDE.set_equations()
a_val=params['a']
res = GL_PDE.solve(file=f'Solutution_with_a_{a_val}.hdmf5')

#res.plot()
