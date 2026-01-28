import pde
import streamlit as st
def generate_save_button(pde_solution)->st.button:
    def save_results():
        nonlocal pde_solution
        #pde_solution.to_file('test.hdmf5')
        st.text('Result saved')
        
    return st.button('Save',on_click=save_results)
