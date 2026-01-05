import sys,os
cur_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.dirname(cur_dir)
sys.path.append(parent_dir)
from equation_class.equation_class import GL_equations

import numpy as np
from scipy.interpolate import Akima1DInterpolator

if __name__=="__main__":

    def equations_for_GL(t,y,params,driving,solver):
        '''
        state vector will contain
        n*2*2 variables:
        1) n- number of sites to analyze
        2) 2- phase( phi) + amplitude(A)
        3) 2- their time derivatie (phi_dot)+(A_dot) 
        
        Return:
        the time derivate of the state-vector dydt
        ''' 
        dydt=[]

        '''
        start with the interpolation of order-parameters 
        '''
        # 1)Extract position list
        pos_list=[params[f'x_{site}'] for site in np.arange(params['N'])]
        # 2) Extract space-dependent amplitude
        A_list=[y[site*4] for site in np.arange(params['N'])]
        # 3) Extract space-dependent phase
        phi_list=[y[site*4+1] for site in np.arange(params['N'])]
        
        '''
        # Add edges
        pos_list.insert(0,-float(pos_list[1]-pos_list[0]))
        A_list.append(A_list[0]) # add Right edge at the end
        phi_list.append(phi_list[0]) # add Right edge at the end
        pos_list.append(2*pos_list[-1]-pos_list[-2]) # add edge at the end
        A_list.insert(0,A_list[-2]) # add Left edge "-2" not "-1" because of the append
        phi_list.insert(0,phi_list[-2]) # add Left edge "-2" not "-1" because of the append
        '''

        # 4) Do interpolation
        A_inter=Akima1DInterpolator(pos_list,A_list,method="makima")
        phi_inter=Akima1DInterpolator(pos_list,phi_list,method="makima")
        # 5) get picewise smooth first derivative
        DA_Dx=A_inter.derivative()
        Dphi_Dx=phi_inter.derivative()
        
        '''
        Iterate over lattice sites
        '''
        # skip looking-up common variables
        q_0=params['q_0']
        

        for site in np.arange(params['N']):
            # Temporal variables just for clarity
            Amp=y[site*4]
            phi=y[site*4+1]
            pos=params[f'x_{site}']
            

            # Get derivatives
            Amp_dot=y[site*4+2]
            phi_dot=y[site*4+3]
            
            DAmp_Dx_x=DA_Dx(pos)
            Dphi_Dx_x=Dphi_Dx(pos)
            U_val=params[f'U_{site}']

            Amp_dot_dot=(-U_val*np.cos(pos*q_0+phi)\
                -2.*params[f'a_{site}']*Amp\
                -4.*params[f'b_{site}']*(Amp**3)\
                -2.*params[f'c_A_{site}']*(DAmp_Dx_x)\
                -2.*params[f'c_phi_{site}']*Amp*(Dphi_Dx_x**2)\
                -params[f'Gamma_A_{site}']*Amp_dot\
                )/params[f'm_A_{site}']
            phi_dot_dot=(U_val*Amp*np.sin(q_0*pos + phi)\
                    -2.*params[f'c_phi_{site}']* (Amp**2) *Dphi_Dx_x\
                    -params[f'Gamma_phi_{site}']*phi_dot\
                    + params[f'kappa_{site}']*driving(t)\
                    )/params[f'm_phi_{site}']
            
            temp_vec=[Amp_dot,phi_dot,Amp_dot_dot,phi_dot_dot]

            if solver=="IVP":
                dydt += [el for el in temp_vec]
            elif solver=="BVP":
                dydt.append(temp_vec)
            else:
                raise ValueError("Solver unknown")
        
        # Additional step for BVP solver
        if solver=="BVP":
            dydt=np.array(dydt)

        return dydt
            
    
    '''
    ( Irrelevent :D )
    For 2H-NbSe2 the lattice constant is a_0 ~ 0.344 [nm]
    and in Nature paper they use q_0 = 5.9 [rad/nm] 
    thus 1/q0 ~0.17 -> setting a=1 -> 1/q0 ~0.5 -> q0~2
    '''


    GL=GL_equations({})
    # Initiate parameters
    # Global parameters
    GL.params['N']=37 #number of points in space
    GL.params['q_0']=2.*np.pi/4. #CDW wave vector
    space_resolution=1

    for site in np.arange(GL.params['N']): 


        GL.params[f'm_A_{site}']=1.
        GL.params[f'm_phi_{site}']=1. # should be similar to m_A
        
        # Relative strnghts are important here
        GL.params[f'a_{site}']=1
        GL.params[f'b_{site}']=0.2   

        #Location in space        
        GL.params[f'x_{site}']=(space_resolution*site)

        #Impurity
        GL.params[f'U_{site}']=-0.9*np.exp((-(float(GL.params[f'x_{site}'])-(GL.params['N'])*0.5)**2)/(0.01**2))
        
        #Coupling to the density gradient
        GL.params[f'c_A_{site}']=1
        GL.params[f'c_phi_{site}']=0.1 # order of magniture smaller then the one for A
        #Damping 
        GL.params[f'Gamma_A_{site}']=1
        GL.params[f'Gamma_phi_{site}']=0.1 # order of magniture smaller then damping of A
        # pulse strenght
        GL.params[f'kappa_{site}']=0.5

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
    GL.set_equations(lambda t,y,*args : equations_for_GL(t,y,GL.params,GL.driving,solver="IVP"))
    sol=GL.solve_eq(solver_type="IVP")

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
    



