import pde


#data=pde.FileStorage('symulacja.hdf5')
import glob
intereting_files=glob.glob('Solutution_with_a_-1.-*imp*.hdmf5')
print(intereting_files)
data=pde.FileStorage(intereting_files[0])


import matplotlib.pyplot as plt
import numpy as np


plt.figure(0) # analyze amplitude evolution
for y,file in enumerate(intereting_files):
    data=pde.FileStorage(file)
    print(data.data[:,0,0].shape)
    for x in np.arange(data.data.shape[-1]):
        plt.plot(data.times[:],(data.data[:,0,x])+x)
    plt.ylabel('A')
    plt.xlabel('t')


plt.figure(1) #analyze phase evolution
for y,file in enumerate(intereting_files):
    data=pde.FileStorage(file)
    for x in np.arange(data.data.shape[-1]):
        plt.plot(data.times[:],(data.data[:,1,x])+x)
    plt.ylabel('phi')
    plt.xlabel('t')


plt.figure(2) # show the amplitude profile at the end
for y,file in enumerate(intereting_files):
    data=pde.FileStorage(file)
    t_f=data.data.shape[0]
    for t in [0,t_f//2,t_f-1]:
        plt.plot(data.data[t,0,:])
    plt.ylabel('A(x)')
plt.show()

