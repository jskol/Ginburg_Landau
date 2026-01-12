import pde


#data=pde.FileStorage('symulacja.hdf5')
import glob
#intereting_files=glob.glob('Sol*_with_*ref*')
intereting_files=[
    'Solutution_with_N_12_q_0_1.6110731556870734_m_A_1.0_m_phi_1.0_'+\
        'a_-1.0_b_0.02_c_A_0_c_phi_0_Gamma_A_0_Gamma_phi_0_kappa_0.5_impurity_func_.hdmf5',
    'Solutution_with_N_12_q_0_1.6110731556870734_m_A_1.0_m_phi_1.0_'+\
        'a_-1.0_b_0.02_c_A_0_c_phi_0_Gamma_A_0_Gamma_phi_0_kappa_0_impurity_func_.hdmf5',
    
    ]
print(intereting_files)

#data=pde.FileStorage('out_file.hdf5')


import matplotlib.pyplot as plt
import numpy as np


fig,ax=plt.subplots(len(intereting_files))
res=[]
for y,file in enumerate(intereting_files):
    data=pde.FileStorage(file)
    temp=[]
    for x in np.arange(data.data.shape[-1]):
        ax[y].plot(data.times[:],(data.data[:,0,x])+x)
        temp.append((data.data[:,0,x])+x)
    res.append(temp)
    ax[y].set_ylabel('A(x)')
    ax[y].set_title(file)
    ax[y].set_ylim((0,120))



plt.figure('comp')
# without the impurity driving has no effect on the amplitude
for el in np.arange(len(res[0])):
    plt.plot(res[0][el]-res[1][el])


plt.show()
