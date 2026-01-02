'''
Equation class will hold parameters and
the function describing the driving
'''
from typing import Callable
import numpy as np
from scipy.integrate import solve_ivp
#### Custom exceptions for the GL_equations class###
class MissingGLComponents(Exception):
    def __init__(self, message):
        self.message=message
        super().__init__(message)




class GL_equations:
    params={} # empty dict
    driving=lambda *args: 0. # By default
    boundary_conditions=[] #empty list
    time_span=()
    equations=None
    events=None
    def __init__(self,params_dict:dict[str,float]):
        '''
        Attach a dict of parameters
        to the G-L equations
        '''
        self.params=params_dict
    
    def set_driving(self, driving: Callable[[float | list[float]], float])->None:
        '''
        Overwrite the driving function
        '''
        self.driving=driving

    def set_boundary_condtions(self, BC_list:list[float])->None:
        '''
        Pass the list of boundary condtions
        '''
        self.boundary_conditions=BC_list

    def set_time_span(self,t_max:float, t_step:float)-> None:
        '''
        Pass t_max and t_step
        to get a tuple of 
        1) list [0,t_max]
        2) np.array of each timestamp
        '''
        time_stamps=np.arange(0,t_max, step=t_step)
        self.time_span=([0,t_max],time_stamps)

    def set_equations( self, equations: Callable[[float,float],list[float]]):
        self.equations=equations

    def set_events(self, event_func):
        self.events=event_func


    def solve_eq(self):
        if not self.boundary_conditions:
            raise MissingGLComponents("Missing Boundary conditions")
        
        if self.equations is None:
            raise MissingGLComponents("Missing function")

        if not self.time_span:
            raise MissingGLComponents("Missing timespan")
        
        if not self.params:
            raise MissingGLComponents("Missing parameters")

        res=solve_ivp(
            self.equations,
            t_span=self.time_span[0],
            t_eval=self.time_span[1],
            args=(self.params,),
            y0=self.boundary_conditions,
            events=self.events
        )
        return res

