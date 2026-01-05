import numpy as np
import matplotlib.pyplot as plt



if __name__=="__main__":
    data=np.loadtxt('test_file.dat')
    plt.plot(data[:,0],data[:,1])
    plt.plot(data[:,0],data[:,-1])
    plt.show()
