import numpy as np
import pandas as pd
import streamlit as st
import pickle

# ----------- UTILS FOR FORECASTS ----------------


@st.cache(show_spinner=False)
def load_dataset():
    return pd.read_csv(r'data/finaldataset.csv')

@st.cache(show_spinner=False)
def process_dataset(df):
    df['InspectionDate'] = pd.to_datetime(df['InspectionDate'])
    df['InspectionYear'] = df['InspectionDate'].dt.year
    df["repairingcostsaved"]=df["repairingcostassumed"]-df["prepairingcostassumed"]
    #df.loc[df['repairingcostsaved'] < 0, 'repairingcostsaved'] = 0
    df["Lossineurossaved"]=df["Lossineuros"]-df["pLossineuros"]
    #df.loc[df['Lossineurossaved'] < 0, 'Lossineurossaved'] = 0
    df["carbonfootprintsaved"]=df["carbonfootprintemitted"]-df["pcarbonfootprintemitted"]
    #df.loc[df['carbonfootprintsaved'] < 0, 'carbonfootprintsaved'] = 0
    return df
