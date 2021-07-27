import streamlit as st
import requests, json 
import pprint
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from matplotlib.ticker import PercentFormatter
from matplotlib import mlab
import scipy
from geopy.geocoders import Nominatim



# Add Disebar 
user_river_input = st.sidebar.text_input("Enter River and section. Example:", "river-exe-exeter-trews-weir")
river_name_section = user_river_input

# Multiselect
user_river_input = st.sidebar.multiselect('Or choose from previous selections:', ['river-exe-exford', 'river-exe-tiverton-stoodleigh', 'river-avon-evesham'])

if user_river_input:
    river_name_section = user_river_input[-1]

# Add title 
st.title(river_name_section.title())


url = (f"https://riverlevels.uk/{river_name_section}/data/json")
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}


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

# Create Pandas DataFrame
df = pd.DataFrame.from_dict(json_levels)


# DataFrame strings to floats. 
df["max_level"] = pd.to_numeric(df["max_level"], downcast="float")
df["min_level"] = pd.to_numeric(df["min_level"], downcast="float")
df["avg_level"] = pd.to_numeric(df["avg_level"], downcast="float")

# Show DataFrame
st.write(df)

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


    

# Time Series Plot 
fig = px.line(df, x='record_date', y=['avg_level'], title='Long Term Gague Measurements', width=800, height=600)

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
st.plotly_chart(fig)

x = df["avg_level"]


# Cumulative Histograms

hist, bin_edges = np.histogram(x, bins=100, density=True)
cdf = np.cumsum(hist * np.diff(bin_edges))
cumm_fig = go.Figure(data=[
    go.Bar(x=bin_edges, y=hist, name='Histogram'),
    go.Scatter(x=bin_edges, y=cdf, name='CDF')
])

cumm_fig.update_layout(
    title="Frequency of Gague occurance",
    xaxis_title="Gague (m)",
    yaxis_title="Frequency",
    legend_title="",
    width=800, 
    height=600)


st.plotly_chart(cumm_fig)

# Write all json data to page
#st.write(json_data)


