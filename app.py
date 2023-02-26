import streamlit as st
from streamlit_option_menu import option_menu
from forecast import render_forecast
from dashboard import render_dashboard
from creators import render_creators

st.set_page_config(page_title=None, page_icon=None, layout="wide")

selected = option_menu(
    menu_title= None,
    options= ['Strategy', 'Dashboard', 'Creators'],
    icons=['graph-up', 'clipboard-data'],
    menu_icon= "cast",
    default_index= 0,
    orientation='horizontal',)

if selected == 'Strategy':
    st.write('')
    render_forecast()
elif selected == 'Dashboard':
    render_dashboard()

elif selected == 'Creators':
    render_creators()