import streamlit as st

import pandas as pd

import geopandas as gpd

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import ipywidgets as widgets
from ipywidgets import interact

### CONFIG
st.set_page_config(
    page_title="Medical deserts",
    page_icon="👨‍⚕️",
    layout="wide"
)

### TITLE AND TEXT
st.title("Medical deserts statistics 👨‍⚕️")

st.markdown("""
    Welcome to the medical deserts dashboard ! Please find some useful statistics for France. Enjoy !!! Bla bla bla ! """)

### LOAD AND CACHE DATA
# URL of the CSV file of APL data
APL_URL = 'https://medical-deserts-project.s3.eu-north-1.amazonaws.com/map.csv'

@st.cache_resource # this lets the 
def load_data(url):
    data = pd.read_csv(url)
    return data

data_load_state = st.text('Loading data...')
data_apl = load_data(APL_URL)
data_load_state.text("") # change text from "Loading data..." to "" once the the load_data function has run

#### CREATE TWO COLUMNS
col1, col2 = st.columns(2)

with col1:
    ### APL pies

    # Define color mapping dictionary
    color_mapping = {
        "Commune carrencée (APL < 2.5)": "red",
        "Offre insuffisante (2.5 < APL < 4)": "orange",
        "Offre satisfaisante (APL > 4)": "green"
    }

    # Function to plot the pie chart based on the selected column
    def plot_pie_chart(column_name, fig, row, col):
        # Count occurrences of each value in the specified column
        column_counts = data_apl[column_name].value_counts().reset_index()
        column_counts.columns = [column_name, 'Count']
        
        # Create the pie chart
        fig_pie = go.Pie(labels=column_counts[column_name], values=column_counts['Count'])
        fig_pie.marker.colors = [color_mapping.get(val, "") for val in column_counts[column_name]]
        
        # Add the pie chart to the specified subplot position
        fig.add_trace(fig_pie, row=row, col=col)

    # Main function for Streamlit app
    def main():
        st.title("Pie Chart Dashboard")
        
        # Create a figure with three subplots arranged horizontally
        fig = make_subplots(rows=1, cols=3, specs=[[{'type':'pie'}, {'type':'pie'}, {'type':'pie'}]], horizontal_spacing=0.05, subplot_titles=("APL status (sans borne d'âge)", "APL status 65 et moins", "APL status 62 et moins"), row_titles=[""], shared_yaxes=False)
        
        # Plot each pie chart in its respective subplot
        plot_pie_chart("APL status (sans borne d'âge)", fig, 1, 1)
        plot_pie_chart("APL status 65 et moins", fig, 1, 2)
        plot_pie_chart("APL status 62 et moins", fig, 1, 3)
        
        # Update the layout to center the legend horizontally
        fig.update_layout(
            legend=dict(
                x=0.5,
                y=-0.1,
                xanchor='center',  # Center horizontally
                orientation="h"
            ), 
            #width=900,
            #height=600 
        )
        
        # Render the plotly figure using Streamlit's plotly_chart function
        st.plotly_chart(fig, use_container_width=True)

    # Call the main function to run the Streamlit app
    if __name__ == "__main__":
        main()

    ### Box graph

    # Main function for Streamlit app
    def box():
        st.title("Résumé des données APL")

        # Create the box plot
        fig = px.box(data_apl, 
                    y=["APL aux médecins généralistes de 62 ans et moins", 
                        "APL aux médecins généralistes de 65 ans et moins", 
                        "APL aux médecins généralistes (sans borne d'âge)"], 
                    title="Résumé des données APL")

        fig.update_yaxes(title="Score APL")
        fig.update_xaxes(title="")

        fig.update_layout(
            title=dict(
                x=0.5
            ), 
            #width=900,
            #height=600 
        )

        # Render the plotly figure using Streamlit's plotly_chart function
        st.plotly_chart(fig, use_container_width=True)

    # Call the main function to run the Streamlit app
    if __name__ == "__main__":
        box()

with col2:
### APL map

    colors = [(0.0, 'red'),     # Red for values <= 0
            (0.25, 'orange'), # Orange for values between 0 and 2
            (0.75, 'yellow'), # Yellow for values between 2 and 3
            (1.0, 'white')]   # Green for values >= 4

    # Create the custom colormap
    custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', colors)

    # Main function for Streamlit app
    def map(data_apl):
        st.title("Custom Data Plotting")

        # Create a dropdown menu with the available columns
        column_dropdown = st.selectbox('Choisir une colonne :', options=["APL aux médecins généralistes (sans borne d'âge)", 
                                                                        "APL aux médecins généralistes de 65 ans et moins",
                                                                        "APL aux médecins généralistes de 62 ans et moins"])

        # Plot the data using GeoPandas
        fig, ax = plt.subplots()
        data_apl.plot(column=column_dropdown, cmap=custom_cmap, legend=True, ax=ax)
        
        # Show a title
        ax.set_title(column_dropdown)
        
        # Remove axis
        ax.axis('off')
        
        # Show the map
        st.pyplot(fig, use_container_width=True)

    # Call the main function to run the Streamlit app
    if __name__ == "__main__":
        map(data_apl)

    
###########################################################################################################################
"""
### Data
DATA_URL = './data.csv'
def load_data():
    data = pd.read_csv(DATA_URL)
    data["dateRep"] = pd.to_datetime(data["dateRep"])
    data = data[(data['cases'] >= 0) & (data['deaths'] >= 0)]
    return data

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("") # change text from "Loading data..." to "" once the the load_data function has run

## Run the below code if the check is checked ✅
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data) 

st.markdown('### World analysis')
st.markdown('#### Cumulated cases')

data2 = data.loc[:, ['dateRep', 'cases']].groupby('dateRep').sum().reset_index()
data2['cumsum'] = data2['cases'].cumsum()
fig = px.area(data2, x='dateRep', y='cumsum')
st.plotly_chart(fig, use_container_width=True)

st.markdown('#### Death per country')
country = st.selectbox("Select a country you want to see deaths", data["countriesAndTerritories"].sort_values().unique())
min_date = data[(data["countriesAndTerritories"]==country)]['dateRep'].min()
max_date = data[(data["countriesAndTerritories"]==country)]['dateRep'].max()
with st.form('Death per country'):
    start_period = st.date_input("Select a start date", value=min_date, min_value=min_date, max_value=max_date)
    end_period = st.date_input("Select an end date", value=max_date, min_value=min_date, max_value=max_date)
    submit = st.form_submit_button("submit")

mask = (data["countriesAndTerritories"]==country) & (data["dateRep"]>=pd.to_datetime(start_period)) & (data["dateRep"]<=pd.to_datetime(end_period))
fig = px.line(data[mask].sort_values('dateRep'), x='dateRep', y='deaths')
st.plotly_chart(fig, use_container_width=True)

st.markdown('#### Map deaths')
data3 = data.loc[:, ['countriesAndTerritories', 'deaths']].groupby('countriesAndTerritories').sum().reset_index()
fig = px.choropleth(data3, 
                    locations='countriesAndTerritories', 
                    locationmode='country names',
                    color='deaths', 
                    hover_name='countriesAndTerritories', 
                    color_continuous_scale='reds' 
                   )


fig.update_layout(title='COVID-19 deaths',
                  geo=dict(showcoastlines=True,
                           projection_type='natural earth', 
                           center=dict(lat=50, lon=10), 
                           scope="europe",
                           ),
                  mapbox_style="carto-positron",
                 width= 600)

fig.update_geos(projection_scale=1.5)
st.plotly_chart(fig, use_container_width=True)
"""