import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import datetime
import pydeck as pdk
from utils import load_dataset
from utils import process_dataset
import requests
import plotly.express as px
from datetime import datetime, date

################################################################
# JAVASCRIPT
################################################################
#[theme]
#base="dark"
#primaryColor="#cebc03"
#secondaryBackgroundColor="#0035bd"

def render_forecast():
    st.markdown(""" 
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        <link rel="stylesheet" href="../css/style.css">
        <link href='https://fonts.googleapis.com/css?family=Allerta Stencil' rel='stylesheet'>
    <style>
            h1{font-display: aligncenter;
                font-family: 'Allerta Stencil';
                color: white;}
    </style>
    <h1><center>Ozone Inspection Strategy</center></h1>
    </head>
    </html>
    """, unsafe_allow_html=True)
    
    with st.spinner('''Warming up the data...'''):
        df = load_dataset()
        df = df.drop(columns='Unnamed: 0')
        df=process_dataset(df)
    # get Spain provincial boundaries
    col = st.columns(3)
    start_date = col[0].date_input('Start Date', df["InspectionDate"].min())
    end_date = col[1].date_input('End Date', df["InspectionDate"].max())
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    mask = (df["InspectionDate"] >= start_datetime) & (df["InspectionDate"] <= end_datetime)
    filtered_df = df.loc[mask]
    # Filter data based on selected Start date and End date
    metric = col[2].selectbox('Metrics', ('Carbon footprint saved', 'Volume costs saved', 'Repairing costs saved','All'))
    if metric=="All":
        towns = filtered_df.groupby("Town")[["latitude", "longitude", "Lossineurossaved"]].agg({"latitude": "first", "longitude": "first", "Lossineurossaved": "sum"})
        towns = towns.reset_index()
        res = requests.get("https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/spain-provinces.geojson")
        # create a density heatmap on Mapbox with the incidence column
        fig = px.density_mapbox(towns, lat='latitude', lon='longitude', z='Lossineurossaved', radius=20,center=dict(lat=40, lon=-3), zoom=5,mapbox_style='carto-positron', opacity=1,hover_name='Town', hover_data=['Lossineurossaved'],color_continuous_scale='Magma')
        # add the provincial boundaries as a layer
        fig.update_layout(mapbox_layers=[{"sourcetype": "geojson","source": res.json(),"type": "line","color": "blue","line": {"width": 0.3},}],mapbox=dict(center=dict(lat=40, lon=-3),zoom=5,style="carto-positron"),margin={"r":0,"t":0,"l":0,"b":0},coloraxis_colorbar=dict(title="Loss in Euros saved in Millions of €",thicknessmode="pixels", thickness=20,lenmode="pixels", len=300,yanchor="middle", y=0.5,ticks="outside", ticksuffix=" €"),title=dict(text="Loss in euros saved within the selected timeline",font=dict(size=24)))
        fig.update_layout(width=1200, height=600)
        st.plotly_chart(fig)
    else:
        if metric=="Volume costs saved":
            metric="Lossineurossaved"
            metric_title= "Volume costs saved in Millions of €"
            color='blues'
            sufix_metrics=" €"
        elif metric=="Repairing costs saved":
            metric="repairingcostsaved"
            color='inferno'
            metric_title= "Repairing costs saved in 100k of €"
            sufix_metrics=" €"
        else:
            metric="carbonfootprintsaved"
            color= 'Greens'
            metric_title= "Carbon footprint saved in Tones of CO2"
            sufix_metrics= " Tones"
        towns = filtered_df.groupby("Town")[["latitude", "longitude", metric]].agg({"latitude": "first", "longitude": "first", metric: "sum"})
        towns = towns.reset_index()
        res = requests.get("https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/spain-provinces.geojson")
        # create a density heatmap on Mapbox with the incidence column
        fig = px.density_mapbox(towns, lat='latitude', lon='longitude', z=metric , radius=20,center=dict(lat=40, lon=-3), zoom=5,mapbox_style='carto-positron', opacity=1,hover_name='Town', hover_data=[metric],color_continuous_scale=color)
        # add the provincial boundaries as a layer
        fig.update_layout(mapbox_layers=[{"sourcetype": "geojson","source": res.json(),"type": "line","color": "blue","line": {"width": 0.3},}],mapbox=dict(center=dict(lat=40, lon=-3),zoom=5,style="carto-positron"),margin={"r":0,"t":0,"l":0,"b":0},coloraxis_colorbar=dict(title=f'{metric_title}',thicknessmode="pixels", thickness=20,lenmode="pixels", len=300,yanchor="middle", y=0.5,ticks="outside", ticksuffix=f'{sufix_metrics}'),title=dict(text="f'{metric}' within the selected timeline",font=dict(size=24)))
        fig.update_layout(width=1200, height=600)
        st.plotly_chart(fig, use_container_width=True)
    