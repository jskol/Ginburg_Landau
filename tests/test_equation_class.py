import os,sys

cur_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.dirname(cur_dir)
sys.path.append(parent_dir)

from app.equation_class.equation_class import GL_equations,MissingGLComponents
import numpy as np

import pytest


@pytest.fixture(scope="session")
def cannon():
    def _cannon(t,y,params):
        x_dot=y[2]
        y_dot=y[3]
        x_dot_dot=-params["k"]*(x_dot)**2/params["mass"]
        y_dot_dot=-params["g"]/params["mass"]-params["k"]*(y_dot)**2/params["mass"] 
        return [x_dot,y_dot,x_dot_dot,y_dot_dot]
    return _cannon

@pytest.fixture(scope="function")
def hit_ground():
    def _hit_ground(t,y,params):
        return y[1]
    _hit_ground.terminal=True
    _hit_ground.direction=-1
    return _hit_ground

@pytest.fixture(scope="function")
def GL(cannon, hit_ground):
    params={
        "mass": 1.0,
        "g": 9.81,
        "k": 0.5,
    }
    GL_params=GL_equations(params)   

    v=40
    ang=np.pi/3
    init_cond=[0,0,v*np.cos(ang),v*np.sin(ang)]
    
    GL_params.set_time_span(7.5,0.01)
    GL_params.set_boundary_condtions(init_cond)
    GL_params.set_equations(cannon)
    GL_params.set_events(hit_ground)
    
    return GL_params

missing_scenarios = [
    ("parameters", "params", {}),
    ("Boundary conditions", "boundary_conditions", []),
    ("Timespan", "time_span", ()),
    ("function", "equations", None)
]

@pytest.mark.parametrize("label, att, val",missing_scenarios)
def test_missing_elements(GL,label,att,val):
    setattr(GL,att,val)

    with pytest.raises(MissingGLComponents) as e:
       GL.solve_eq()
       assert label in str(e.value)
    


if __name__=="__main__":
    ''''
    Simple test on a 2-d shoot with 
    air-resitance controlled by "k"
    '''

    params={
        "mass": 1.0,
        "g": 9.81,
        "k": 0.5,
    }
    GL_params=GL_equations(params)
    
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