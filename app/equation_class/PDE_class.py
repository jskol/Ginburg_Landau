import pde



class GL_equations_set:
    params={} # empty dict
    driving:str ='0' # By default single element list with function returning zero
    boundary_conditions:dict[str,float]={}
    equations=None
    time_domain: tuple[float,float]=(100,1e-1) # tuple with t_max and t_mesh
    grid=None

    def __init__(self,params_dict:dict[str,float],t_max, t_mesh,x_mesh):
        '''
        Attach a dict of parameters
        to the G-L equations
        '''
        self.params=params_dict
        self.time_domain=(t_max,t_mesh)
        self.grid=pde.CartesianGrid([[0,self.params['N']]],[self.params['N']*x_mesh],periodic=False)
    
    def set_bc(self,
               A_0:float=1.,
               phi_0:float=0.,
               A_dot_0:float=0.,
               phi_dot_0:float=0.)->None:
        
        '''
        Sets boundary conditions
        has to be run before set_equations 
        to be accounted for
        '''
        self.boundary_conditions["A"]=A_0
        self.boundary_conditions["phi"]=phi_0
        self.boundary_conditions["A_dot"]=A_dot_0
        self.boundary_conditions["phi_dot"]=phi_dot_0


    def set_equations(self)->None:
        #If not specified define BC
        if self.boundary_conditions is None:
            print("Setting default BC")
            self.set_bc()

        eq=pde.PDE({
            "A" : "A_dot",
            "phi" : "phi_dot",
            "A_dot" : f"(\
                -{self.params['impurity']}*cos(x*{self.params['q_0']} + phi)\
                -2.*{self.params['a']}*A\
                -4.*{self.params['b']}*(A**3)\
                -2.*{self.params['c_A']}*diff(A,x)\
                -2.*{self.params['c_phi']}*A* (diff(phi,x)**2)\
                -{self.params['Gamma_A']}*A_dot)/{self.params['m_A']}",
            "phi_dot" : f"(\
                {self.params['impurity']}*A*sin({self.params['q_0']}*x + phi)\
                -2.*{self.params['c_phi']}*(A**2)*diff(phi,x)\
                -{self.params['Gamma_phi']}*phi_dot\
                +{self.params['kappa']}*{self.driving})/{self.params['m_phi']}"
            }
            ,bc={
                "A":{"value":self.boundary_conditions["A"]},
                "phi":{"value":self.boundary_conditions["phi"]},
                "A_dot":{"value":self.boundary_conditions["A_dot"]},
                "phi_dot":{"value":self.boundary_conditions["phi_dot"]}
            }
        )
        self.equations=eq

    def set_equations_ref(self)->None:
        #If not specified define BC
        if self.boundary_conditions is None:
            print("Setting default BC")
            self.set_bc()

        eq=pde.PDE({
            "A" : "A_dot",
            "phi" : "phi_dot",
            "A_dot" : f"(\
                -2.*{self.params['a']}*A\
                -4.*{self.params['b']}*(A**3)\
                -2.*{self.params['c_phi']}*A* (diff(phi,x)**2)\
                -{self.params['impurity']}*cos(x*{self.params['q_0']} + phi)\
                -2.*{self.params['c_A']}*diff(A,x)**2\
                -{self.params['Gamma_A']}*A_dot)/{self.params['m_A']}",
            "phi_dot" : f"(\
                {self.params['impurity']}*A*sin({self.params['q_0']}*x + phi)\
                +4.*{self.params['c_phi']}*A*diff(phi,x)*diff(A,x)\
                +2.*{self.params['c_phi']}*(A**2)*diff(phi,x)**2\
                -{self.params['Gamma_phi']}*phi_dot\
                +{self.params['kappa']}*{self.driving})/{self.params['m_phi']}"
            }
            ,bc={
                "A":{"value":self.boundary_conditions["A"]},
                "phi":{"value":self.boundary_conditions["phi"]},
                "A_dot":{"value":self.boundary_conditions["A_dot"]},
                "phi_dot":{"value":self.boundary_conditions["phi_dot"]}
            }
        )
        self.equations=eq


    def set_init_state(self,phi_0:float=0)->None:
        state=pde.FieldCollection(
            [
                pde.ScalarField.from_expression(self.grid, f"cos({self.params['q_0']}*x+{phi_0})"),
                pde.ScalarField.from_expression(self.grid, f"{phi_0}"),
                pde.ScalarField.from_expression(self.grid, "0"),
                pde.ScalarField.from_expression(self.grid, "0")
            ]
        )
        self.state=state

    def set_driving(self,func:str)->None:
        self.driving=func
    
    
    
    def solve(self,file='out_file.hdf5',solver_num:int =-2):
        #Registered solvers are:
        solvers_list=[
        'AdaptiveSolverBase',
        'adams–bashforth',
        'crank-nicolson',
        'euler',
        'explicit',
        'explicit_mpi',
        'implicit',
        'runge-kutta',
        'scip'
        ]
        storage=pde.FileStorage(file)
        if self.equations is None:
            self.set_equations()
        
        es = self.equations.solve(
            self.state, 
            t_range=self.time_domain[0],
              dt=self.time_domain[1], 
              tracker=storage.tracker(0.1),
              solver='runge-kutta',
              backend='numpy'#solvers_list[solver_num]
              )  # solve the PDE
        return es
