import numpy as np
"""
params_name_dict={
    'a': ['a- parameter',np.arange(-1.,0.04,0.01),-0.6],
    'b':['b-parameter',np.arange(0,0.1,0.01),0.08],
    'c_A':['c_A',np.arange(0,1,0.01),0.02],
    'c_phi':['c_phi',np.arange(0,1,0.01),0.02],
    'Gamma_A':['Gamma_A',np.arange(0,1,0.01),0],
    'Gamma_phi':['Gamma_phi',np.arange(0,1,0.01),0],
    'kappa':['kappa', np.arange(0,1.2,0.01),1],
    'm_A':['m_A', np.arange(0.01,2,0.01),1],
    'm_phi':['m_phi', np.arange(0.01,2,0.01),1],
    'q_0':['CDW wave vector', np.arange(1.,3.,0.1),1.5],
    'N':['System size', np.arange(40),6],
    't_max': ['max evolution time', np.arange(10,200,1),12],
}
"""

params_name_dict={
    'a': ['a- parameter',np.arange(-100.,10,1),-100],
    'b':['b-parameter',np.arange(0,1.,0.1),0.2],
    'c_A':['c_A',np.arange(0,10,1.),2.],
    'c_phi':['c_phi',np.arange(0,1,0.01),0.11],
    'Gamma_A':['Gamma_A',np.arange(0,300,20),240],
    'Gamma_phi':['Gamma_phi',np.arange(0,100,10),40],
    'kappa':['kappa', np.arange(0,1.2,0.01),0.14],
    'm_A':['m_A', np.arange(1,200,1),100],
    'm_phi':['m_phi', np.arange(1,200,1),110],
    'q_0':['CDW wave vector', np.arange(1.,7,0.1),5.9],
    'N':['System size', np.arange(40),6],
    't_max': ['max evolution time', np.arange(10,200,1),12],
}

