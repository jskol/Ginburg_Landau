import sys,os
cur_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.dirname(cur_dir)

from app.equation_class.equation_class import GL_equations

import numpy as np

if __name__=="__main__":

    GL=GL_equations()
    GL.params['m_A']=1
    GL.params['m_phi']=1
    GL.params['a']=0.1
    GL.params['b']=0.1
    GL.params['U']=0.1
    GL.params['x']=0.1
    GL.params['q_0']=0.4
    GL.params['c_A']=0.1
    GL.params['DA_Dx']=0.1
    GL.params['Gamma_A']=0.1
    GL.params['c_phi']=0.1
    GL.params['Dphi_Dx']=0.1
    GL.params['Gamma_phi']=0.1
    GL.params['kappa']=0.1

    GL.set_driving(lambda x:np.exp[-0.5* (x- 5)**2]*np.cos(2*(x - 5)))

    def equations(t,y,params,driving):
        '''
        We need 2*2 eq
        '''    
        A_dot=y[2]
        phi_dot=y[3]
        
        A_dot_dot=(\
             -2*params['a']*y[0]\
                -4*params['b']*y[0]**3\
                    -params['U']*np.cos(params['x']*params['q_0']+y[1])\
                        -2.0*params['c_A']*params['DA_Dx']\
                            -2.0*params['c_phi']*y[0]*params['D_phi_Dx']**2\
                                  -params['Gamma_A']*A_dot\
                    )/params['m_A']
        phi_dot_dot=(\
            params['U']*y[0]*np.sin(params['q_0']*params['x'] + y[1])\
                -2.*params['c_phi']* y[0]**2*params['Dphi_Dx']\
                    -params['Gamma_phi']*phi_dot\
                          + params['kappa']*driving(t)\
                    )/params['m_phi']

        return [A_dot,phi_dot,A_dot_dot,phi_dot_dot]