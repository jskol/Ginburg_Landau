import numpy as np

params_name_dict={
    'a': ['a- parametaer',np.arange(-0.1,0.1,0.01),0.04],
    'b':['b-parameter',np.arange(0,0.1,0.01),0.0],
    'c_A':['c_A',np.arange(0,1,0.01),0],
    'c_phi':['c_phi',np.arange(0,1,0.01),0],
    'Gamma_A':['Gamma_A',np.arange(0,1,0.01),0],
    'Gamma_phi':['Gamma_phi',np.arange(0,1,0.01),0],
    'kappa':['kappa', np.arange(0,1.2,0.01),1],
    'm_A':['m_A', np.arange(0.01,2,0.01),1],
    'm_phi':['m_phi', np.arange(0.01,2,0.01),1],
    'N':['System size', np.arange(20),12],
    't_max': ['max evolution time', np.arange(10,200,1),12],
    'q_0':['CDW wave vector', np.arange(1.,3.,0.1),1.5]
}

