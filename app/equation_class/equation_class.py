'''
Equation class will hold parameters and
the function describing the driving
'''
from typing import Callable,Any
import numpy as np
#### Custom exceptions for the GL_equations class###
class MissingGLComponents(Exception):
    def __init__(self, message):
        self.message=message
        super().__init__(message)


# Define parent class
class GL_equations:
    params={} # empty dict
    driving=[lambda *args: 0.] # By default single element list with function returning zero
    boundary_conditions: Any
    time_span: Any
    equations=None
    events=None

    def __init__(self,params_dict:dict[str,float]):
        '''
        Attach a dict of parameters
        to the G-L equations
        '''
        self.params=params_dict
    
    def set_driving(self, 
                    driving: 
                        list[Callable[[float | list[float]], float]]
                    )->None:
        '''
        Overwrite the driving-function-list
        '''
        self.driving=driving

    def set_boundary_condtions(self, BC_list : list[float])->None:
        '''
        Pass the list of boundary condtions
        '''
        self.boundary_conditions=BC_list
    
    def set_time_span(self,t_max:float, t_step:float)-> None:
        pass

    def set_equations( self, equations: Callable[[float,float,dict[str,float],Callable[float,float]],list[float]]
                      )->None:
        '''
        Contains the presciption for the time derivate
        of the state vector
        '''
        self.equations=lambda t,y,*args: equations(t,y,self.params,self.driving[0])

    def set_events(self, event_func):
        self.events=event_func

    '''
    This method will have proper solver appended
    in each class definition
    '''
    def solve_eq(self):
        if not self.boundary_conditions:
            raise MissingGLComponents("Missing Boundary conditions")
        if self.equations is None:
            raise MissingGLComponents("Missing function")

        if not self.time_span:
            raise MissingGLComponents("Missing timespan")
        
        if not self.params:
            raise MissingGLComponents("Missing parameters")



solver_names={}# will hold the available solvers
# Define a factory function 
def GL_factory(solver_name:str)->GL_equations | None:
    res=solver_names[solver_name]
    if res is None:
        raise Exception("Unknown solver")
    else:
        return res


# Define child classes
from scipy.integrate import solve_ivp
class GL_equations_IPV(GL_equations):
    # Overwrite the timespan to meet ipv solver criteria
    def set_time_span(self,t_max:float, t_step:float)-> None:
        '''
        Pass t_max and t_step
        to get a tuple of 
        1) list [0,t_max]
        2) np.array of each timestamp
        '''
        time_stamps=np.arange(0,t_max, step=t_step)
        self.time_span=([0,t_max],time_stamps)
    
    
    def solve_eq(self):
        super().solve_eq()
        res=solve_ivp(
            self.equations,
            t_span=self.time_span[0],
            t_eval=self.time_span[1],
            y0=self.boundary_conditions,
            events=self.events,
        )
        return res
#add to solver library
solver_names["IPV"]=GL_equations_IPV({})


from scipy.integrate import solve_bvp
class GL_equations_BVP(GL_equations):         
    def set_time_span(self,t_max:float, t_step:float)-> None:
        '''
        BVP solver takes a single numpy array
        with time stamps 
        '''
        self.time_span=np.arange(0,t_max, step=t_step)
    #Overwrite the set_equations
    # to transorm the functions into 
    # a proper form with each time slice
    # in one column

    def set_equations( self, equations: Callable[[float,float,dict[str,float],Callable[float,float]],list[float]]
                      )->None:
        self.equations=lambda t,y,*args: np.vstack(tuple(equations(t,y,self.params,self.driving)))
    
    def solve_eq(self):
        super().solve_eq()    
        res=solve_bvp(
            self.equations,
            x=self.time_span,
        )
        pass        
solver_names["BVP"]=GL_equations_BVP({})

