import streamlit as st
import numpy as np
import os,sys,pde
curr_dir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(curr_dir))
from equation_class.GL_equations_params import params_name_dict


# run_button functionalities ##
def restart_run_button():
    st.session_state.run_button_active=True

def disable_run_button():
    st.session_state.run_button_active=False
    st.session_state.run_calc=True


def restart_to_file():
    restart_run_button()
    #st.session_state.to_file =not st.session_state.to_file

@st.fragment
def sidebar_content(params: dict[str,float|str]):
    with st.expander('model parameters'):
        for k,v in list(params_name_dict.items())[:-2]:
            slider=st.select_slider(v[0],options=[x for x in v[1]],value=v[2],format_func=lambda x: f'{x:.2f}',on_change=restart_run_button)
            params[k]=slider
            
    for k,v in list(params_name_dict.items())[-2:]:
        slider=st.select_slider(v[0],options=[x for x in v[1]],value=v[2],format_func=lambda x: f'{x:.2f}',on_change=restart_run_button)
        params[k]=slider

    with st.expander('impurity'):
        # store the value so that its not reset after N is changed
        if 'imp_loc' not in st.session_state:
            st.session_state.imp_loc=round(0.5*params['N'],1)
        
        imp_loc=st.multiselect(
            "Choose impurity/s location/s",
            options=np.arange(0,params['N'],0.1),
            placeholder="x location(s)",
            format_func=lambda x: f'{x:.1f}',
            accept_new_options=True,
            default=[round(params['N']//2,1)],
            on_change=restart_run_button
        )
        imp_stength=st.select_slider('Impurity strength',options=np.arange(-200,200,1),value=125,format_func=lambda x: f'{x:.2f}',on_change=restart_run_button)
        if imp_loc:
            imp_str=''.join([f'-{imp_stength} *exp(-(x-{imp_x})**2 )/(1**2)' for imp_x in imp_loc])
        else:
            imp_str='0'
        params['impurity']=imp_str

    with st.expander('Driving'):
        driving_str=st.select_slider('Pulse strength',options=np.arange(-4.1, 4.1, 0.1),value=0.,format_func=lambda x: f'{x:.2f}',on_change=restart_run_button)
        # store the value so that its not reset after t_max is changed
        if 'pulse_max' not in st.session_state:
            st.session_state.pulse_max=0.
        pulse_max=st.select_slider('Pulse time',options=np.arange(0,params['t_max'],0.1),
            value=round(st.session_state.pulse_max,1),format_func=lambda x: f'{x:.2f}',on_change=restart_run_button)
        st.session_state.pulse_max=pulse_max 

        params['driving']=f'{driving_str}*exp(-0.5*(t- {pulse_max})**2)*cos(2.*(t - {pulse_max}))'
        
        add_Joule=st.toggle('Joule heating',value=False,on_change=restart_run_button,help='a-parameter (controlling the CDW) becomes linked with the driving')
        params['Joule']=add_Joule
    
        
    #Run Calc button
    if st.button('Run Simulation',width='stretch',type='primary',disabled=not st.session_state.run_button_active,on_click=disable_run_button):
        st.rerun()
 


import h5py

def file_uploader():
    uploaded_file = st.file_uploader(
        "Upload data", 
        accept_multiple_files=False,
        type="hdmf5"
    )
    class storage_mock:
        def __init__(self,times,data):
            self.times=times
            self.data=data
    

    if uploaded_file is not None:
        try:
            with h5py.File(uploaded_file, 'r') as f:
                keys = list(f.keys())
                print(keys)
                storage=storage_mock(f['times'][:],f['data'][:])
                st.session_state.PDE_res=storage
            
            st.session_state.has_data=True
        
        except Exception as e:
            st.error(f"Błąd podczas odczytu pliku: {e}")
 
def download_sidebar():

    def toggle_action():
        print(f'toggle is {st.session_state.to_file}')
        if st.session_state.to_file and st.session_state.has_data:
            st.session_state.needs_rerun=True 
        st.session_state.run_button_active=True
        

   # Heavy calculations -> do not store in memory
    st.toggle('Save results directly to file',value=False,key='to_file',on_change=toggle_action,
                                       help='Preferred for larger calculations, but can be problematic on free domains')        

    if st.session_state.needs_rerun:
        st.rerun()

    print(st.session_state.to_file, " ", st.session_state.needs_rerun)
    if 'was_downloaded' not in st.session_state:
            st.session_state.was_downloaded=False

    def download_click():
        st.session_state.to_file=False
        st.session_state.was_downloaded=True
        st.session_state.run_button_active=True
        

    if st.session_state.to_file and st.session_state.has_data:
        out_name='out.hdmf5'
        try :
            with open(out_name, "rb") as f:
                st.download_button(
                        label='Download data',
                        data=f,
                        on_click=download_click,
                        type='primary',
                        file_name=out_name,
                        mime="application/x-hdmf5",
                        key='Download_sidebar'
                )

            if st.session_state.was_downloaded:
                try:
                    os.remove(out_name)
                except FileNotFoundError:
                    print('File not Found')
                finally:
                    st.session_state.was_downloaded=False
                    st.session_state.has_data=False            
        except FileNotFoundError:
            st.rerun()