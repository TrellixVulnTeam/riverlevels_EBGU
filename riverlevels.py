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
country = st.sidebar.selectbox('Select Country:', Uk_Scotland_Wales) # Select Country #index=1 sets default to Scotland

# Select County 
if country == "England":
    county = st.sidebar.selectbox('Select County:', Uk_Scotland_Wales[country], index=9) # Select Country #index=9 sets default to Devon
else:
    county = st.sidebar.selectbox('Select County:', Uk_Scotland_Wales[country]) 


# Select Monitoring Section  

selected_county = Uk_Scotland_Wales[country][county]

list_of_monitoring_sections_names = [x[0] for x in selected_county]

if county == "Devon":
    monitoring_section = st.sidebar.selectbox('Select Monitoring Section:', list_of_monitoring_sections_names, index=68) # Select monitoring section #index=68 sets default to Trews Weir
else: 
    monitoring_section = st.sidebar.selectbox('Select Monitoring Section:', list_of_monitoring_sections_names) 

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
df = None
df = pd.DataFrame.from_dict(json_levels)

# DataFrame strings to floats. 
df["max_level"] = pd.to_numeric(df["max_level"], downcast="float")
df["min_level"] = pd.to_numeric(df["min_level"], downcast="float")
df["avg_level"] = pd.to_numeric(df["avg_level"], downcast="float")


# Creates Data Frame which shows values to 2 decimal places.

display_df = df[['max_level', 'min_level', 'avg_level']].copy()
   
display_df['max_level'] = display_df['max_level'].map('{:,.2f}'.format)
display_df['min_level'] = display_df['min_level'].map('{:,.2f}'.format)
display_df['avg_level'] = display_df['avg_level'].map('{:,.2f}'.format)

# Centre DataFrame using columns 
data_fame_col1, data_fame_col2, data_fame_col3 = st.beta_columns([1,2,1])

# Getting percnetile values for the plot. (Get gauge at percentile)

percentiles = [0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,0.99]
gauge_at_percentile = []

for i in percentiles[::-1]:
    gauge_probability = df.avg_level.quantile(i)
    gauge_at_percentile.append(gauge_probability)

with data_fame_col2:

    # Table for Data, using data from display_df data to two decimal places. 
    
    test_table = go.Figure(data=[go.Table(header=dict(values=['max_level (m)', 'min_level (m)', 'avg_level (m)']),
                 cells=dict(
                     values=[display_df['max_level'], display_df['min_level'], display_df['avg_level']],
                     font_size=12,
                     height=27,))
                     ])

    test_table.update_layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=4
            ),
                )
    
    st.plotly_chart(test_table, use_container_width = True)

# DataFram Header
st.subheader(f"Long Term Gague Measurements - {monitoring_section}")

# Time Series Plot 
fig = px.line(df, x='record_date', y=['avg_level'], height=600)


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

# Update Long Term Gauge Measurements Plot with updated max and min lines 

fig.add_hline(y=gauge_at_percentile[1],
                    line_dash="dot",
                    annotation_text=f"Q10: {round(gauge_at_percentile[1],2)}", 
                    annotation_position="bottom right",
                    annotation=dict(font_size=15, font_family="Arial Black"),
                    line=dict(
                        color='red',
                        width=5,
                    ),)
fig.add_hline(y=gauge_at_percentile[11],
                    line_dash="dot",
                    annotation_text=f"Q90: {round(gauge_at_percentile[11],2)}", 
                    annotation_position="bottom right", 
                    annotation=dict(font_size=15, font_family="Arial Black"),
                    line=dict(
                        color='green',
                        width=5
                    ),)

fig.update_layout(
    yaxis_range=[gauge_at_percentile[11]-0.5,gauge_at_percentile[0]+0.5], 
    xaxis_title="Date",
    yaxis_title="Gague (m)",
    legend_title="",)

# Plot figure to streamlit
st.plotly_chart(fig,  use_container_width=True)

x = df["avg_level"]

# DataFram Header
st.subheader(f"Flow Duration Curve - {monitoring_section}")
st.text("")

col1, col2 = st.beta_columns((2,1))

# Percentile Chart

with col1:

    # Percentile Chart

    sorted_df = None
    sorted_df = df.sort_values(by="avg_level", ascending=False)

    sorted_df['rank']=sorted_df['avg_level'].rank(method="min", ascending=False, na_option='bottom')

    num_events = len(sorted_df.index)

    exceedance_probability_column = []
    
    for row in sorted_df.values:
        exceedance_probability = (row[4]/(num_events+1))*100

        exceedance_probability_column.append(exceedance_probability)
    
    sorted_df['exceedance_probability'] = exceedance_probability_column

    sorted_df_by_probability = sorted_df.sort_values(by="exceedance_probability", ascending=True)

    x_axis_data = sorted_df_by_probability['exceedance_probability']
    y_axis_data = sorted_df_by_probability['avg_level']

    # Get gauge at percentile 

    percentiles = [0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,0.99]
    gauge_at_percentile = []

    for i in percentiles[::-1]:
        gauge_probability = sorted_df_by_probability.avg_level.quantile(i)
        gauge_at_percentile.append(gauge_probability)

    # Limit gauge at percentil to two decimal places

    gauge_at_percentile = [round(num, 2) for num in gauge_at_percentile]

    # Create percentile figure 

    new_percentile_figure = go.Figure(data=go.Scatter(x=x_axis_data, y=y_axis_data), layout_xaxis_range=[1,99], layout_yaxis_range=[gauge_at_percentile[11], gauge_at_percentile[0]])

    new_percentile_figure.update_layout(
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
    
    st.plotly_chart(new_percentile_figure, use_container_width = True)

with col2:

    # Table for Percentile Chart

    percentiles = [1,10,20,30,40,50,60,70,80,90,95,99]
    
    test_fig = go.Figure(data=[go.Table(header=dict(values=['Percentiles (%)', 'Gauge (m)']),
                 cells=dict(
                     values=[percentiles, gauge_at_percentile],
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

#### Create Footer ###

from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))

def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)

def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
    </style>
    """

    style_div = styles(
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        text_align="center",
        height="60px",
        opacity=1
    )

    style_hr = styles(
    )

    body = p()
    foot = div(style=style_div)(hr(style=style_hr), body)

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)
        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)

def footer():
    myargs = [
        "Made by ",
        link("https://github.com/TomNewton1", "@Thomas Newton"),
        br(),
        "Github ",
        link("https://github.com/TomNewton1/riverlevels", "repository"), image('https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png',
              width=px(19), height=px(19), margin= "0em", align="top"),
        br(),
        "Data Sourced from ",
        link("https://riverlevels.uk/", "riverlevels.uk"),
    ]
    layout(*myargs)


if __name__ == "__main__":
    footer()
