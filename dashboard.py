import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_dataset
from utils import process_dataset
import altair as alt
import requests
import plotly.graph_objs as go

def render_dashboard():
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
    <h1><center>Dashboard</center></h1>
    </head>
    </html>
    """, unsafe_allow_html=True)

    with st.spinner('''Warming up the dashboard's data...'''):
        df = load_dataset()
        df = df.drop(columns='Unnamed: 0')
        df=process_dataset(df)

    custom, predefined = st.tabs(["Make your own", "Predefined"])
    
    with custom:
        col1, col2, col3, col4 = st.columns(4)
        
        variable = col1.selectbox(
        'Select variable to measure',
        ('carbonfootprintsaved', 'Lossineurossaved', 'repairingcostsaved', 'predicted incidence'))

        top = col3.selectbox(
        'Select number of features',
        ('Top 10', 'Top 25', 'Top 50', 'Top 100', 'Top 1000'))

        if top == 'Top 10':
            topn = 10
        elif top == 'Top 25':
            topn = 25
        elif top == 'Top 50':
            topn = 50
        elif top == 'Top 100':
            topn = 100
        elif top == 'Top 1000':
            topn = 1000

        chart = col4.selectbox(
        'Select type of chart',
        ('Bar chart', 'Pie Chart'))

        group = col2.selectbox(
        'Select variable to group by',
        ('Province','None', 'Town',
        'InspectionYear'))
        if group != 'None':
            value = st.selectbox(
            'Select value to measure',
            ('Maximum', 'Minimum','Mean'))

        else:
            value = st.selectbox(
            'Select value to measure',
            ('Sum', 'Maximum', 'Minimum'))
        


        st.write('')
        
        if group == 'None':
            if chart == 'Bar chart':
                if value == 'Sum':
                    st.bar_chart(df[variable].value_counts().head(topn), height=500, use_container_width=True)
                if value == 'Maximum':
                    st.bar_chart(df[variable].sort_values(ascending = True).head(topn), height=500, use_container_width=True)
                if value == 'Minimum':
                    st.bar_chart(df[variable].sort_values(ascending = False).head(topn), height=500, use_container_width=True)
            elif chart == 'Pie Chart':
                if value == 'Sum':
                    extrabydensity = pd.cut(df[variable].value_counts().head(topn), 5).value_counts(sort=False).head(5)
                    fig = px.pie(extrabydensity, values=variable, names=extrabydensity.index.array.unique().astype('str'))
                    st.plotly_chart(fig, use_container_width=True)
                if value == 'Maximum':
                    extrabydensity = pd.cut(df[variable].sort_values(ascending = True).head(topn), 5).value_counts(sort=False).head(5)
                    fig = px.pie(extrabydensity, values=variable, names=extrabydensity.index.array.unique().astype('str'))
                    st.plotly_chart(fig, use_container_width=True)
                if value == 'Minimum':
                    extrabydensity = pd.cut(df[variable].sort_values(ascending = False).head(topn), 5).value_counts(sort=False).head(5)
                    fig = px.pie(extrabydensity, values=variable, names=extrabydensity.index.array.unique().astype('str'))
                    st.plotly_chart(fig, use_container_width=True)

        if group != 'None':
            if chart == 'Bar chart':
                if value == 'Mean':
                    st.bar_chart(df.groupby([group])[variable].mean().head(topn), height=500, use_container_width=True)
                if value == 'Maximum':
                    st.bar_chart(df.groupby([group])[variable].mean().sort_values(ascending = False).head(topn), height=500, use_container_width=True)
                if value == 'Minimum':
                    st.bar_chart(df.groupby([group])[variable].mean().sort_values(ascending = True).head(topn), height=500, use_container_width=True)
            elif chart == 'Pie Chart':
                if value == 'Mean':
                    extrabydensity = df.groupby([group])[variable].mean().head(topn)
                    fig = px.pie(extrabydensity, values=variable, names=extrabydensity.index.array.unique().astype('str'))
                    st.plotly_chart(fig, use_container_width=True)
                if value == 'Maximum':
                    extrabydensity = df.groupby([group])[variable].mean().sort_values(ascending = False).head(topn)
                    fig = px.pie(extrabydensity, values=variable, names=extrabydensity.index.array.unique().astype('str'))
                    st.plotly_chart(fig, use_container_width=True)
                if value == 'Minimum':
                    extrabydensity = df.groupby([group])[variable].mean().sort_values(ascending = True).head(topn)
                    fig = px.pie(extrabydensity, values=variable, names=extrabydensity.index.array.unique().astype('str'))
                    st.plotly_chart(fig, use_container_width=True)


    with predefined:
        
        col=st.columns(2)
        col1=col[0]
        col2=col[1]
        with col1:

            st.subheader('Top 20 Towns with the highest Gaz Loss Cost')
            
            top20twgc=df.groupby(["Town"])["Lossineuros"].mean().sort_values(ascending=False).head(20)
            top20twgc_sorted = top20twgc.sort_values()
            st.bar_chart(top20twgc_sorted, height=500, use_container_width=True)
        with col2:
            towns=df.groupby("Town")[["latitude", "longitude", "Lossineuros"]].agg({"latitude": "first", "longitude": "first", "Lossineuros": "mean"}).sort_values(by="Lossineuros", ascending=False).head(20)
            towns= towns.reset_index()
            res = requests.get("https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/spain-provinces.geojson")
            # create a density heatmap on Mapbox with the incidence column
            fig = px.density_mapbox(towns, lat='latitude', lon='longitude', z='Lossineuros', radius=60,center=dict(lat=40, lon=-3), zoom=5,mapbox_style='carto-positron', opacity=1,hover_name='Town', hover_data=['Lossineuros'],color_continuous_scale='Magma')
            # add the provincial boundaries as a layer
            fig.update_layout(mapbox_layers=[{"sourcetype": "geojson","source": res.json(),"type": "line","color": "blue","line": {"width": 0.3},}],mapbox=dict(center=dict(lat=40, lon=-3),zoom=5,style="carto-positron"),margin={"r":0,"t":0,"l":0,"b":0},coloraxis_colorbar=dict(title="Incidence",thicknessmode="pixels", thickness=20,lenmode="pixels", len=300,yanchor="middle", y=0.5,ticks="outside", ticksuffix=" Incidences"),title=dict(text="Pipe Gas Incidences by Province (2010-2020)",font=dict(size=24)))
            fig.update_layout(width=600, height=400)
            st.plotly_chart(fig)
        #my_dict = dict(zip(top20twgc['Town'], top20twgc['Lossineuros']))
        #sortedtowns = sorted(my_dict.items(), key=lambda x: x[1], reverse=True)
        #sortedtowns=dict(sortedtowns)

        """col1.altair_chart(alt.Chart(top20twgc).mark_bar().encode(
            x=alt.X('Town', sort=None),
            y='Lossineuros',
        ))"""


        st.subheader('Top 20 Costly Pipes')
        st.bar_chart(df.groupby(["PipeId"])["Lossineuros"].mean().sort_values(ascending=False).head(20), height=500, use_container_width=True)

        # create a DataFrame from the data
        # create a DataFrame from the data
        data = {'x': [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
                'y': [4.232157e+06, 8.754028e+06, 7.286916e+06, 8.783938e+06, 9.808856e+06, 6.291756e+06, 6.169941e+06, 6.028724e+06, 6.517783e+06],
                'y1': [2.581113e+06, 7.882824e+06, 6.861091e+06, 7.208642e+06, 8.830624e+06, 5.280194e+06, 4.789427e+06, 4.736429e+06, 5.177284e+06]}
        df = pd.DataFrame(data)

        # calculate the difference between y and y1
        diff = df['y'] - df['y1']

        # create traces for two sets of bars
        trace1 = go.Bar(x=df['x'], y=df['y'], name='Standard Strategy', marker=dict(color='red', opacity=0.5), width=0.4)
        trace2 = go.Bar(x=df['x'], y=df['y1'], name='Bayes Genes Strategy', marker=dict(color='green', opacity=1), width=0.4)

        # create the figure object and add the traces
        fig = go.Figure(data=[trace1, trace2])

        # calculate the difference between the two bar plots for each year
        diff = df['y'] - df['y1']
        cumulative_diff = [sum(diff[:i]) for i in range(1, len(diff)+1)]
        # create a trace for the difference bars
        trace3 = go.Bar(x=df['x'], y=diff, name='Difference', marker=dict(color='blue'), width=0.4)

        # add the frames to the figure
        frames = [go.Frame(data=[go.Bar(x=df['x'], y=df['y'], name='Standard Strategy', marker=dict(color='red', opacity=0.5), width=0.4),
                                go.Bar(x=df['x'], y=df['y1'], name='Bayes Genes Strategy', marker=dict(color='green', opacity=1), width=0.4),
                                go.Bar(x=df['x'], y=[0]*len(df), name='Difference', marker=dict(color='blue'), width=0.4, base=df['y1'])],
                        layout=go.Layout(title_text=f'Total Money Saved over 10 years: {diff:.2f}')) for diff in cumulative_diff]
        fig.frames = frames

        # add the animation buttons to the figure
        fig.update_layout(updatemenus=[{'type': 'buttons', 'buttons':
                                        [{'label': 'Play', 'method': 'animate', 'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True, 'transition': {'duration': 0}}]}, {'label': 'Pause', 'method': 'animate', 'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}]}]}])

        # update the layout with axis labels and title
        fig.update_layout(xaxis=dict(title='Year'), yaxis=dict(title='Gaz Leakage volume in Million €'), title='Comparison of Gaz Leakage Volume Loss in Million € between strategies')

        fig.update_layout(width=1350, height=600)
        # show the plot
        st.plotly_chart(fig, use_container_width=True)


        ##############################################################################################################################
        
        # create a DataFrame from the data
        data = {'x': [2012,2013,2014,2015,2016,2017,2018,2019,2020],
                'y': [34.032613,70.404732,58.600260,70.645290,78.880759,50.583559,49.608760,47.613030,51.779836],
                'y1': [17.183879,58.686933,53.608836,65.043593,70.355444,45.331962,40.533987,40.399639,44.114284]}
        data = pd.DataFrame(data)

        # create a stacked bar chart
        fig = go.Figure(data=[
            go.Bar(name='Bayes Genes Strategy', x=data['x'], y=data['y'], marker_color='red',opacity=0.5),
            go.Bar(name='Standard Strategy', x=data['x'], y=data['y1'], marker_color='green',opacity=1)
        ])

        diff = data['y'] - data['y1']
        cumulative_diff = [sum(diff[:i]) for i in range(1, len(diff)+1)]
        # create a trace for the difference bars
        trace3 = go.Bar(x=data['x'], y=diff, name='Difference', marker=dict(color='blue'), width=0.4)

        # add the frames to the figure
        frames = [go.Frame(data=[go.Bar(x=data['x'], y=data['y'], name='Standard Strategy', marker=dict(color='red', opacity=0.5), width=0.4),
                                go.Bar(x=data['x'], y=data['y1'], name='Bayes Genes Strategy', marker=dict(color='green', opacity=1), width=0.4),
                                go.Bar(x=data['x'], y=[0]*len(data), name='Difference', marker=dict(color='blue'), width=0.4, base=data['y1'])],
                        layout=go.Layout(title_text=f'Carbon Foot print reduced in tons of CO2 over 10 years: {diff:.2f}')) for diff in cumulative_diff]
        fig.frames = frames

        # add the animation buttons to the figure
        fig.update_layout(updatemenus=[{'type': 'buttons', 'buttons':
                                        [{'label': 'Play', 'method': 'animate', 'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True, 'transition': {'duration': 0}}]}, {'label': 'Pause', 'method': 'animate', 'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}]}]}])

        # update layout
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='CO2 emitted in Tons',
            title='Comparison of Carbon Footprint emitted in Tons of CO2 between strategies'
        )

        fig.update_layout(width=1000, height=600)
        # show the plot
        st.plotly_chart(fig, use_container_width=True)
        ########################################################################################################################

        # create a DataFrame from the data
        data = {'x': [2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020],
                'y': [ 854.675374,144786.244274,534733.809074,874932.392092,778690.496825,632780.470087,707766.169593,688486.445204,642022.133440,741444.699507,712478.037770],
                'y1': [854.675374,140147.507467,381028.689501,792284.008407,639223.057329,555808.344323,651871.609327,600739.379187,591560.285965,688237.076837,691139.569360]}
        data = pd.DataFrame(data)

        # create a line plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['x'], y=data['y'], name='Standard Strategy', mode='lines+markers', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=data['x'], y=data['y1'], name='Bayes Genes Strategy', mode='lines+markers', line=dict(color='green')))




        # set the axis labels and title
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Repairing Costs in €',
            title='Comparison of Repairing Costs in Euros between strategies'
        )

        fig.update_layout(width=1350, height=600)
        
        st.plotly_chart(fig, use_container_width=True)

# show the plot



        #col1.bar_chart(df[df['Extra-fuel']>=0]['Extra-fuel'], use_container_width=True)

    #st.subheader('Count of 20 Most Frequent Teledyne Weights')
    #st.bar_chart(df["TeledyneRampWeight"].value_counts().head(20), height=500, use_container_width=True)


        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs
        with kpi1:
            st.markdown('#### Gas Leakage Costs')
            st.markdown('# -9%')

        with kpi2:
            st.markdown('#### Carbon Footprint')
            st.markdown('# -10%')

        with kpi3:
            st.markdown('#### Repair Costs')
            st.markdown('# -8%')      
