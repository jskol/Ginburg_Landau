import pde

interesting_file_name='Solutution_with_N_12_q_0_1.6110731556870734_m_A_1.0_m_phi_1.0_'+\
        'a_-1.0_b_0.02_c_A_0_c_phi_0_Gamma_A_0_Gamma_phi_0_kappa_0.5_impurity'

add_imp=False
if add_imp:
    interesting_file_name+=f'_func_'
else:
    interesting_file_name+=f'_0_'


intereting_files=list(map(lambda x: f'{interesting_file_name}{x}.hdmf5',['','_ref']))


print(intereting_files)
data=pde.FileStorage(intereting_files[0])


import matplotlib.pyplot as plt
import numpy as np


t_step=0.1
fig,sub=plt.subplots(1,len(intereting_files),num='Amplitude evolution')
for y,file in enumerate(intereting_files):
    data=pde.FileStorage(file)
    N_range=data.data.shape[-1]
    print(data.data[:,0,0].shape)
    for t in np.arange(data.data.shape[0],step=10):
        #sub[y].plot(data.times[:],(data.data[:,0,x])+x)
        sub[y].plot(np.arange(N_range),3*data.data[t,0,:]+t)
    sub[y].set_xlabel('A(x)')
    sub[y].set_ylabel('t')
    sub[y].set_xlim(0,N_range-1)
    sub[y].set_ylim(-1,np.amax(data.data[-1,0,:])+t)
    sub[y].set_yticks(np.arange(data.data.shape[0],step=100),t_step*np.arange(data.data.shape[0],step=100))


plt.figure(1) #analyze phase evolution
fig,sub=plt.subplots(1,len(intereting_files),num="phase evolution")
for y,file in enumerate(intereting_files):
    data=pde.FileStorage(file)
    N_range=data.data.shape[-1]
    for t in np.arange(data.data.shape[0],step=10):
        #sub[y].plot(data.times[:],np.mod(data.data[:,1,x],2*np.pi)+x)
        sub[y].plot(np.arange(N_range),data.data[t,1,:]+t)        
    sub[y].set_xlabel('phi(x)')
    sub[y].set_ylabel('t')
    sub[y].set_xlim(0,N_range-1)
    sub[y].set_ylim(-1,np.amax(data.data[-1,1,:])+t)
    sub[y].set_yticks(np.arange(data.data.shape[0],step=100),t_step*np.arange(data.data.shape[0],step=100))



plt.figure(2) # show the amplitude profile at the end
fig,sub=plt.subplots(len(intereting_files),num='amplitude profile at chosen times')
for y,file in enumerate(intereting_files):
    data=pde.FileStorage(file)
    t_f=data.data.shape[0]
    for t in [0,t_f//2,t_f-1]:
        sub[y].plot(data.data[t,0,:],label=f't={t}')
    sub[y].set_ylabel('A(x)')
    sub[y].set_xlabel('x')
    sub[y].legend()
plt.figure(2) # show the amplitude profile at the end

fig,sub=plt.subplots(len(intereting_files),num='amplitude evolution at chosen points')
for y,file in enumerate(intereting_files):
    data=pde.FileStorage(file)
    x_f=data.data.shape[-1]
    for x in [0,x_f//2,x_f-1]:
        sub[y].plot(data.data[:,0,x],label=f'x={x}')
    sub[y].set_ylabel('A(x)')
    sub[y].set_xlabel('t')
    sub[y].legend()



plt.show()

