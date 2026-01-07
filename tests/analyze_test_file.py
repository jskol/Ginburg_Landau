import numpy as np
import matplotlib.pyplot as plt



if __name__=="__main__":
    data=np.loadtxt('test_file.dat')
    #plt.plot(data[:,0],data[:,2])
    #plt.plot(data[:,0],data[:,-2])
    for t in np.arange(100):
        plt.plot(data[t,1:])
    
    plt.show()
