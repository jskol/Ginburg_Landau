import sys,os
cur_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.dirname(cur_dir)
sys.path.append(parent_dir)
from equation_class.equation_class import GL_factory
from GL_equations_def import equations_for_GL,set_param_dict
import numpy as np

if __name__=="__main__":

    '''
    ( Irrelevent :D )
    For 2H-NbSe2 the lattice constant is a_0 ~ 0.344 [nm]
    and in Nature paper they use q_0 = 5.9 [rad/nm] 
    thus 1/q0 ~0.17 -> setting a=1 -> 1/q0 ~0.5 -> q0~2
    '''
    GL=GL_factory("IPV")
    # Initiate parameters
    GL.params=set_param_dict()

    # Define a light pulse profile
    #GL.set_driving(lambda x:100*np.exp(-0.5* (x- 1.5)**2)*np.cos(2.*(x - 1.5)))
    
    # set initial state with fixed boundaries
    phi_0=0.*np.pi
    bc=[]
    for site in np.arange(GL.params['N']):
        temp=[np.cos(GL.params['q_0']*GL.params[f'x_{site}']+phi_0),phi_0 ,0.,0.]
        bc += [el for el in temp]
    
    #import matplotlib.pyplot as plt
    #plt.plot(bc[::4])

    GL.set_boundary_condtions(bc)
    GL.set_time_span(180,0.05)
    GL.set_equations(equations_for_GL)#lambda t,y,*args : equations_for_GL(t,y,GL.params,GL.driving))
    sol=GL.solve_eq()

    out_data=[sol.t]
    for x in np.arange(len(sol.y),step=4):
        out_data.append(sol.y[x])

    out_data=np.column_stack(tuple(out_data))
    np.savetxt('test_file.dat',out_data)

    
    
    import matplotlib.pyplot as plt
    for x in np.arange(len(sol.y),step=4):
        plt.plot(sol.t,sol.y[x]+0.5*x,label=f'{x//4}')
      
    
    
    



    plt.xlabel('t')
    plt.ylabel('site')
    plt.show()
    



