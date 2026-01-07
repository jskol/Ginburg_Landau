import sys,os
cur_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.dirname(cur_dir)
sys.path.append(parent_dir)
from equation_class.equation_class import GL_factory
from GL_equations_def import equations_for_GL,set_param_dict
import numpy as np

if __name__=="__main__":

    GL=GL_factory("BVP")
    # Initiate parameters
    GL.params=set_param_dict()

    # Define a light pulse profile
    GL.set_driving(lambda x:100*np.exp(-0.5* (x- 1.5)**2)*np.cos(2.*(x - 1.5)))
    # set initial state with fixed boundaries
    phi_0=0.5*np.pi
    bc=[]
    for site in np.arange(GL.params['N']):
        temp=[np.cos(GL.params['q_0']*GL.params[f'x_{site}']+phi_0),phi_0 ,0.,0.]
        bc += [el for el in temp]
    

    GL.set_boundary_condtions(bc)
    GL.set_time_span(180,0.05)
    GL.set_equations(lambda t,y,*args : np.vstack(tuple(equations_for_GL(t,y,GL.params,GL.driving))))
    sol=GL.solve_eq()



    out_data=[sol.x]
    for x in np.arange(len(sol.y),step=4):
        out_data.append(sol.y[x])


    out_data=np.column_stack(tuple(out_data))
    np.savetxt('test_file.dat',out_data)

    import matplotlib.pyplot as plt
    #for x in np.arange(len(sol.y),step=4):
    #    plt.plot(sol.t,sol.y[x]+0.5*x,label=f'{x//4}')
    
    plt.plot(sol.t,sol.y[0])
    plt.plot(sol.t,sol.y[-4])
    plt.plot(sol.t,sol.y[4])
    plt.plot(sol.t,sol.y[-8])


    plt.xlabel('t')
    plt.ylabel('site')
    plt.show()
    



