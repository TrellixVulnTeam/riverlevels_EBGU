import streamlit as st
import requests, json 
import pprint
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from matplotlib import mlab
import scipy
from geopy.geocoders import Nominatim

import validators

from data import UK_river_stations, Scotland_river_stations, Wales_river_stations, Uk_Scotland_Wales

# Setting Page Layout to Wide
st.set_page_config(
    page_title="RiverLevelsUk",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add Disebar 
#user_river_input = st.sidebar.text_input("Enter River and section. Example:", "river-exe-exeter-trews-weir")
#river_name_section = user_river_input

# Multiselect test
country = st.sidebar.selectbox('Select Country:', Uk_Scotland_Wales) # Select Country 

# Select County 
county = st.sidebar.selectbox('Select County:', Uk_Scotland_Wales[country]) # Select Country 

# Select Monitoring Section  
#print(Uk_Scotland_Wales[country][county])

selected_county = Uk_Scotland_Wales[country][county]

list_of_monitoring_sections_names = [x[0] for x in selected_county]

monitoring_section = st.sidebar.selectbox('Select Monitoring Section:', list_of_monitoring_sections_names) # Select monitoring section 

# Get Monitoring section URL
for i in selected_county:
    if monitoring_section in i:
        monitoring_section_url = i[1]
        break

# Add title 
st.title(monitoring_section.title())

# Need to check both circumstance (with county in url and without )
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
url = (f"{monitoring_section_url}/data/json")

json_data = requests.get(url=url).json()

# Location 
river_location = json_data['info']['name']
st.markdown(f"**Location:** {river_location}")

# Watercourse
watercourse = json_data['info']['watercourse']
st.markdown(f"**Watercourse:** {watercourse}")

# Len of json data
json_data_len = len(json_data['levels'])

# Current level of last item in json object
current_level = json_data['levels'][json_data_len-1]['avg_level']

# Current level recorded. 
current_level_recorded = json_data['levels'][json_data_len-1]['record_date']

# Current level 
st.markdown(f"**Current level:** {current_level}m, recorded on *{current_level_recorded}* ")

# Insert Map

geolocator = Nominatim(user_agent="riverlevels")

location = geolocator.geocode(f"{river_location}, UK")

if location is None:
    st.markdown("<h2 style='text-align: center; color: red;'>There is no map location for this monitoring spot!</h2>", unsafe_allow_html=True)

else:
    lat = location.latitude
    lon = location.longitude

    map_df = pd.DataFrame({
        'location' : [location,],
        'lat' : lat,
        'lon' : lon
    })
    st.map(map_df)


# Get levels only 
json_levels = json_data['levels']

# DataFram Header
st.subheader("Historical Data")
st.text("")

# Create Pandas DataFrame
df = pd.DataFrame.from_dict(json_levels)

# DataFrame strings to floats. 
df["max_level"] = pd.to_numeric(df["max_level"], downcast="float")
df["min_level"] = pd.to_numeric(df["min_level"], downcast="float")
df["avg_level"] = pd.to_numeric(df["avg_level"], downcast="float")

# Round df values
decimals = 1    
df['max_level'] = df['max_level'].apply(lambda x: round(x, decimals))
df['max_level'] = df['max_level'].round(2)
df['min_level'] = df['min_level'].apply(lambda x: round(x, decimals))
df['avg_level'] = df['avg_level'].apply(lambda x: round(x, decimals))


# Centre DataFrame using columns 
data_fame_col1, data_fame_col2, data_fame_col3 = st.beta_columns([1,2,1])

with data_fame_col2:
    # Show DataFrame
    st.write(df, use_container_width=True)

# Write Pandas DataFrame to site
#if st.checkbox('view_data'):

# Max High 
max_high = df["max_level"].max()

# Typical High 
typical_high = df["max_level"].mean()

# Min Low 
min_low = df["min_level"].min()

# Tpical Low 
typical_low = df["max_level"].min()


# DataFram Header
st.subheader("Long Term Gague Measurements")

# Time Series Plot 
fig = px.line(df, x='record_date', y=['avg_level'], height=600)

fig.add_hline(y=typical_high, line=dict(
                        color='red',
                        width=5
                    ),)
fig.add_hline(y=typical_low, line=dict(
                        color='green',
                        width=5
                    ),)

fig.update_layout(
    yaxis_range=[min_low,max_high], 
    xaxis_title="Date",
    yaxis_title="Gague (m)",
    legend_title="",)

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)


# Plot figure to streamlit
st.plotly_chart(fig,  use_container_width=True)

x = df["avg_level"]

# DataFram Header
st.subheader("Percentile exceedance of gauge")
st.text("")

col1, col2 = st.beta_columns((2,1))


# Percentile Chart

with col1:

    percentiles = [1,10,20,30,40,50,60,70,80,90,95,99]

    gauges = []

    for i in percentiles:
        p = np.percentile(x,i)
        gauges.append(p)


    percentile_figure = px.line( x=percentiles, y=gauges, title="percentile chart")

    percentile_figure.update_layout(
        title=None,
        xaxis_title="Percentile",
        yaxis_title="Gague (m)",
        legend_title="",
         margin=dict(
        l=50,
        r=0,
        b=100,
        t=0,
        pad=4
    ),
  
        )

    st.plotly_chart(percentile_figure, use_container_width = True)


with col2: 
    # Table for Percentile Chart
    
    test_fig = go.Figure(data=[go.Table(header=dict(values=['Percentiles', 'Gauge (m)']),
                 cells=dict(
                     values=[percentiles, gauges],
                     font_size=12,
                     height=27,))
                     ])

    test_fig.update_layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=4
            ),
                )
    
    
    st.plotly_chart(test_fig, use_container_width = True)



# Write all json data to page
#st.write(json_data)


