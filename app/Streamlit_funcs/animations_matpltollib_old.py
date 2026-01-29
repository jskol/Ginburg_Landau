import pde
q0=[
    '1.0649466622338282','3.141592653589793','1.5707963267948966'
    ]

interesting_file_name=f'Solutution_with_N_12_q_0_{q0[0]}_m_A_1.0_m_phi_1.0_'+\
    'b_0.005_'+\
        'c_A_0.001_c_phi_0.001'+\
            '_Gamma_A_0_Gamma_phi_0_kappa_0.0_impurity'
t0=25
#a0=f'a_4.0_'
a0=f'a_-0.1_'
#a0=f'a_-0.1*(1.-0.5*exp(-0.5*(t - 25)**2))_'
intereting_files=[f'{interesting_file_name}{imp}{a0}_t0_{t0}.hdmf5' for imp in ['_0_','_func_']]

print(intereting_files)
data=pde.FileStorage(intereting_files[1])


import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider


t_step=0.1
fig,sub=plt.subplots(2,sharex=True)#1,len(intereting_files),num='Amplitude evolution')
for y,file in enumerate(intereting_files[:1]):
    data=pde.FileStorage(file)
    N_range=data.data.shape[-1]
    t_steps=data.data.shape[0]
    def time_ev(t):
        return data.data[t,0,:],data.data[t,1,:]
    
    line_A, = sub[0].plot(np.arange(N_range), time_ev(0)[0], lw=2)
    line_F, = sub[1].plot(np.arange(N_range), time_ev(0)[1], lw=2)

    sub[0].set_xlabel('A(x)')
    sub[0].set_xlabel('phi(x)')
    sub[0].set_ylabel('x')
    sub[0].set_xlim(0,N_range)
    sub[0].set_ylim(-5,5)
    fig.subplots_adjust(bottom=0.25)
    # Make a horizontal slider to control the frequency.
    axfreq = fig.add_axes([0.25, 0.1, 0.65, 0.03])
    time_slider = Slider(
        ax=axfreq,
        label='time',
        valmin=0,
        valmax=t_steps,
        valinit=0,
        valstep=1
    )
    def update(val):
        new_data=time_ev(time_slider.val)
        line_A.set_ydata(new_data[0])
        line_F.set_ydata(new_data[1])
        fig.canvas.draw_idle()

    time_slider.on_changed(update)
    plt.show()