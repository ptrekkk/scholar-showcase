import streamlit as st


def set_start_up_message(msg):
    st.session_state['show_message'] = "Settings saved."


def show_start_up_message():
    if 'show_message' in st.session_state:
        st.toast(st.session_state['show_message'])
        del st.session_state['show_message']
