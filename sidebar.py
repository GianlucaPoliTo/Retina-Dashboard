import pandas as pd
import streamlit as st

def space_sidebar(n):
    for i in range(n):
        st.sidebar.text("")
    return

def load_sidebar(**kwargs):

    st.sidebar.write(
        """
        # Configuration
        """
    )
    space_sidebar(3)
    width = st.sidebar.slider("Main Graph Width", min_value=180, max_value=1920, value=1024)
    height = st.sidebar.slider("Main Graph Height", min_value=180, max_value=1920, value=720)
    space_sidebar(2)
    data = st.sidebar.checkbox("Print Description Table")
    space_sidebar(2)
    st.sidebar.text("Macro Filters:")
    space_sidebar(1)
    PT = st.sidebar.multiselect("Payload Type Filter", kwargs["pt"])
    IP_s = st.sidebar.multiselect("IP Src Filter", kwargs["ip_s"])
    IP_d = st.sidebar.multiselect("IP Dst Filter", kwargs["ip_d"])
    LONG = st.sidebar.text_input("Duration", value=0)
    return width, height, data, PT, IP_s, IP_d, LONG