import os,sys

cur_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.dirname(cur_dir)
sys.path.append(parent_dir)

from app.equation_class.equation_class import GL_equations

from scipy.integrate import solve_ivp
import numpy as np
if __name__=="__main__":
    
    
    params={
        "mass": 1.0,
        "g": 9.81,
        "k": 0.5,
    }
    GL_params=GL_equations(params)
    #GL_params.set_driving(lambda x,y: 0.)

    def cannon(t,y,params):
            x_dot=y[2]
            y_dot=y[3]
            x_dot_dot=-params["k"]*(x_dot)**2/params["mass"]
            y_dot_dot=-params["g"]/params["mass"]-params["k"]*(y_dot)**2/params["mass"] 
            return [x_dot,y_dot,x_dot_dot,y_dot_dot]
    
    def hit_ground(t,y,params):
          return y[1]
    
    hit_ground.terminal=True
    hit_ground.direction=-1

    v=40
    ang=np.pi/3
    init_cond=[0,0,v*np.cos(ang),v*np.sin(ang)]
    
    GL_params.set_time_span(7.5,0.01)
    GL_params.set_boundary_condtions(init_cond)
    GL_params.set_equations(cannon)
    GL_params.set_events(hit_ground)
    sol=GL_params.solve_eq()

    print(f'Solved eqs from {sol.t[0]} to {sol.t[-1]}')
    import matplotlib.pyplot as plt
    plt.plot(sol.y[0],sol.y[1])
    plt.show()