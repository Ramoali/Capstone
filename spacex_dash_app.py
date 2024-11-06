# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Create the app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # Task 1: Dropdown to select launch site
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC 4E', 'value': 'VAFB SLC 4E'},
                     {'label': 'KSC LC 39A', 'value': 'KSC LC 39A'},
                     {'label': 'CCAFS SLC 40', 'value': 'CCAFS SLC 40'}
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site",
                 style={'width': '50%', 'padding': '3px', 'font-size': '20px', 'margin': '20px'}),

    # Task 2: Pie chart to show the total successful launches count for selected site
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    # Task 3: Slider to select payload range
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=0,
                    max=10000,
                    step=1000,
                    marks={0: '0', 1000: '1000', 2000: '2000', 3000: '3000', 4000: '4000', 5000: '5000', 6000: '6000', 7000: '7000', 8000: '8000', 9000: '9000', 10000: '10000'},
                    value=[min_payload, max_payload]),

    # Task 4: Scatter plot for correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# Task 2: Callback to update the success-pie-chart based on launch site selection
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Grouping by the success/failure outcome for all sites
        site_data = spacex_df.groupby('class').size().reset_index(name='count')
    else:
        # Filter data based on the selected site
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site].groupby('class').size().reset_index(name='count')

    # Create the pie chart
    fig = px.pie(site_data, names='class', values='count', title=f'Success vs Failed launches for {selected_site}')
    return fig

# Task 4: Callback to update the success-payload-scatter-chart based on launch site and payload selection
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Filter data based on the selected launch site
    if selected_site == 'ALL':
        filtered_data = spacex_df
    else:
        filtered_data = spacex_df[spacex_df['Launch Site'] == selected_site]

    # Further filter the data based on payload range
    filtered_data = filtered_data[(filtered_data['Payload Mass (kg)'] >= payload_range[0]) & 
                                  (filtered_data['Payload Mass (kg)'] <= payload_range[1])]

    # Create the scatter chart
    fig = px.scatter(filtered_data, x='Payload Mass (kg)', y='class', color='class',
                     title=f'Success vs Payload Mass for {selected_site} (Payload Mass: {payload_range[0]} - {payload_range[1]} kg)',
                     labels={'class': 'Success/Failure', 'Payload Mass (kg)': 'Payload Mass (kg)'})
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
