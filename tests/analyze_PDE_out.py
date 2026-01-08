import pde


#data=pde.FileStorage('symulacja.hdf5')
import glob
#intereting_files=glob.glob('Sol*_with_*ref*')
intereting_files=['Solutution_with_a_-1.hdmf5','Solutution_with_a_1.hdmf5']
print(intereting_files)

#data=pde.FileStorage('out_file.hdf5')


import matplotlib.pyplot as plt
import numpy as np


fig,ax=plt.subplots(len(intereting_files))
for y,file in enumerate(intereting_files):
    data=pde.FileStorage(file)
    for x in np.arange(data.data.shape[-1]):
        ax[y].plot(data.times[:],(data.data[:,0,x])+x)
    ax[y].set_ylabel('A')
    ax[y].set_title(file)
    ax[y].set_xlim((0,100))

plt.show()
