
from scipy.interpolate import Akima1DInterpolator
import numpy as np

def equations_for_GL(t,y,params,driving):
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
    
    # Add reflection
    pos_list.insert(0, pos_list[0]-pos_list[1])
    pos_list.append(2*pos_list[-1]-pos_list[-2])
    A_list.insert(0,A_list[1])
    A_list.append(A_list[-2])
    phi_list.insert(0,phi_list[1])
    phi_list.append(phi_list[-2])

    # 4) Do interpolation
    A_inter=Akima1DInterpolator(pos_list,A_list,method="akima")
    phi_inter=Akima1DInterpolator(pos_list,phi_list,method="akima")
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
        
        # Get 1st derivatives
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
        
        dydt += [el for el in temp_vec]

    return dydt


def set_param_dict()->dict[str,int]:
    # Global parameters
    params={}
    params['N']=37 #number of points in space
    params['q_0']=2.*np.pi/4. #CDW wave vector
    space_resolution=1
    for site in np.arange(params['N']): 
        params[f'm_A_{site}']=1.
        params[f'm_phi_{site}']=1. # should be similar to m_A
       
        # Relative strenghts are important here
        params[f'a_{site}']=1
        params[f'b_{site}']=0.2   

        #Location in space        
        params[f'x_{site}']=(space_resolution*site)

        #Impurity
        params[f'U_{site}']=-0.9*np.exp((-(float(params[f'x_{site}'])-(params['N'])*0.5)**2)/(0.01**2))
        
        #Coupling to the density gradient
        params[f'c_A_{site}']=1
        params[f'c_phi_{site}']=0.1 # order of magniture smaller then the one for A
        #Damping 
        params[f'Gamma_A_{site}']=1
        params[f'Gamma_phi_{site}']=0.1 # order of magniture smaller then damping of A
        # pulse strenght
        params[f'kappa_{site}']=0.5
    
    return params