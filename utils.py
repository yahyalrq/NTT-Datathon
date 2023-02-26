import numpy as np
import pandas as pd
import streamlit as st
import pickle

# ----------- UTILS FOR FORECASTS ----------------


@st.cache(show_spinner=False)
def load_dataset():
    return pd.read_csv(r'finaldataset.csv')

@st.cache(show_spinner=False)
def process_dataset(df):
    df['InspectionDate'] = pd.to_datetime(df['InspectionDate'])
    df['InspectionYear'] = df['InspectionDate'].dt.year
    df["repairingcostsaved"]=df["repairingcostassumed"]-df["prepairingcostassumed"]
    df["Lossineurossaved"]=df["Lossineuros"]-df["pLossineuros"]
    df["carbonfootprintsaved"]=df["carbonfootprintemitted"]-df["pcarbonfootprintemitted"]
    return df
