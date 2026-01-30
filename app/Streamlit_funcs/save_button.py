import pde
import streamlit as st
import os,time

def save_PDE_to_file( pde_solution:pde.storage.memory.MemoryStorage,out_name:str ='out.hdmf5' )->None:
    file_storage=pde.FileStorage(out_name)
    st.text(f'Data saved as {out_name}')
    file_storage.start_writing( pde_solution[0])

    for field,current_time in zip(pde_solution,pde_solution.times):
        file_storage.append(field, time=current_time)
    file_storage.end_writing()

#legacy
def generate_save_button(pde_solution:pde.storage.memory.MemoryStorage, out_name:str ='out.hdmf5')->None:
    if st.button(label='Prepare data'):
        save_PDE_to_file(pde_solution,out_name)

@st.fragment
def generate_download_button(pde_solution:pde.storage.memory.MemoryStorage)->None:
    #Create locally the out-file
    # Make download button    
    col1,col2=st.columns(2)
    with col2:
        out_name=st.text_input("Pass the output file name")

    with col1:
        left,right=st.columns(2)
        if left.button(label='Prepare data for download'):
            if not out_name:
                out_name='temp'
            out_name += '.hdmf5'
            
            save_PDE_to_file(pde_solution,out_name)    
            with open(out_name, "rb") as f:
                right.download_button(
                    label='Download data',
                    data=f,
                    on_click='ignore',
                    type='primary',
                    file_name=out_name,
                    mime="application/x-hdmf5"
                )
            os.remove(out_name)
        