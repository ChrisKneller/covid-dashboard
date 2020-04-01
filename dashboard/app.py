import dash
import dash_core_components as dcc
import dash_html_components as html
from data import df1, df2, filter_df
import plotly.graph_objects as go
import datetime
import numpy as np
import dash_ui as dui

# print(df)

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://codepen.io/rmarren1/pen/mLqGRg.css'
    ]

grid = dui.Grid(_id="grid", num_rows=12, num_cols=12, grid_padding=0)

def generate_table(dataframe, max_rows=999):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in ["Country","Population","Province","Last updated","Cases","Deaths"]])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in [1,3,4,5,8,9]
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

# Create the world map
def generate_map(df):
    fig = go.Figure(go.Scattergeo())
    fig.update_geos(
        projection_type="natural earth",
        showcountries=True,
        countrycolor='rgb(40,40,40)'
        )
    fig.update_layout(
        height=500, 
        margin={"r":0,"t":0,"l":0,"b":0},
        showlegend=False,
        )

    for location in range((len(df))):
        # Sort out the naming of each plot point 
        # (some are just countries, some are country provinces)
        has_province = True if len(df.iloc[location][4])>1 else False
        
        location_name = df.iloc[location][1]
        if has_province:
            location_name += f" ({df.iloc[location][4]})"

        # Plot confirmed cases in each area
        fig.add_trace(go.Scattergeo(
            lon=[float(df.iloc[location][7])],
            lat=[df.iloc[location][6]],
            text=f"{location_name}: {df.iloc[location][8]:,} confirmed",
            name=location_name + " - confirmed",
            marker=dict(
                size=int(df.iloc[location][8]**(0.5))/10 + 5,
                color='rgba(102, 153, 255, 0.8)',
                line_color='rgb(40,40,40)',
                line_width=0,
            )
        ))

        # Plot deaths in each area
        fig.add_trace(go.Scattergeo(
            lon=[float(df.iloc[location][7])],
            lat=[df.iloc[location][6]],
            text=f"{location_name}: {df.iloc[location][9]:,} dead",
            name=location_name + " - deaths",
            marker=dict(
                size=int(df.iloc[location][9]**(0.5))/10 + 2,
                color='rgba(255, 102, 102, 0.8)',
                line_color='rgb(40,40,40)',
                line_width=0,
            )
        ))
    return fig


def generate_map_w_options(df, plot_cases=True, plot_recoveries=True, plot_deaths=True):
    
    latest_date = df.iloc[len(df)-1][2]
    df = filter_df(df,"Date",latest_date)
    
    fig = go.Figure(go.Scattergeo())
    fig.update_geos(
        projection_type="natural earth",
        showcountries=True,
        countrycolor='rgb(40,40,40)'
        )
    
    titletext = "Confirmed"
    if plot_cases:
        titletext += " cases"
    if plot_recoveries:
        titletext += " recoveries"
    if plot_deaths:
        titletext += " deaths"
    titletext += (" " + latest_date)
    
    fig.update_layout(
        title={
            'text': titletext,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            },
        height=500, 
        margin={"r":5,"t":10,"l":5,"b":0},
        showlegend=False,
        )

    for location in range((len(df))):
        # Sort out the naming of each plot point 
        # (some are just countries, some are country provinces)
        has_province = True if df.iloc[location][6] else False
        
        location_name = df.iloc[location][1]
        if has_province:
            location_name += f" ({df.iloc[location][6]})"

        if plot_cases:
            # Plot confirmed cases in each area
            confirmed = 0 if np.isnan(df.iloc[location][0]) else df.iloc[location][0]
            fig.add_trace(go.Scattergeo(
                lon=[float(df.iloc[location][5])],
                lat=[df.iloc[location][4]],
                text=f"{location_name}: {confirmed:,.0f} confirmed",
                name=location_name + " - confirmed",
                marker=dict(
                    size=int(confirmed**(0.5))/10,
                    color='rgba(102, 153, 255, 0.8)',
                    line_color='rgb(40,40,40)',
                    line_width=0,
                )
            ))

        if plot_deaths:
            # Plot deaths in each area
            deaths = 0 if np.isnan(df.iloc[location][3]) else df.iloc[location][3]
            if deaths == 0:
                continue
            fig.add_trace(go.Scattergeo(
                lon=[float(df.iloc[location][5])],
                lat=[df.iloc[location][4]],
                text=f"{location_name}: {deaths:,.0f} dead",
                name=location_name + " - deaths",
                marker=dict(
                    size=int(deaths**(0.5))/10,
                    color='rgba(255, 102, 102, 0.8)',
                    line_color='rgb(40,40,40)',
                    line_width=0,
                )
            ))

        if plot_recoveries:
        # Plot recoveries in each area
            recoveries = 0 if np.isnan(df.iloc[location][7]) else df.iloc[location][7]
            if recoveries == 0:
                continue
            fig.add_trace(go.Scattergeo(
                lon=[float(df.iloc[location][5])],
                lat=[df.iloc[location][4]],
                text=f"{location_name}: {recoveries:,.0f} recovered",
                name=location_name + " - recoveries",
                marker=dict(
                    size=int(recoveries**(0.5))/10,
                    color='rgba(52, 189, 45, 0.8)',
                    line_color='rgb(40,40,40)',
                    line_width=0,
                )
            ))

    return fig



def generate_horizontal_bar(df, max_rows=50):
    top_labels = ['Death rate']
    colours = []    
    # Get a list of colours that change as you change values being plotted
    for row in range(max_rows):
        colours.append(f'rgb(255,{194/max_rows*(max_rows-row)+92},{153/max_rows*(max_rows-row)})')
    
    x_data = []
    y_data = []
    y_label = []

    # Gather the data from the dataframe
    for location in range((len(df))):
        has_province = True if len(df.iloc[location][4])>1 else False
            
        location_name = df.iloc[location][1]
        if has_province:
            location_name += f" ({df.iloc[location][4]})"

        if location_name == 'Canada (Diamond Princess)':
            continue

        cases = df.iloc[location][8]
        if cases == 0:
            cases+=1
        deaths = df.iloc[location][9]

        death_rate = deaths/cases
        x_data.append(death_rate)
        y_data.append(location_name)
        y_label.append(f"{death_rate*100:.1f}% ({deaths:,} deaths, {cases:,} cases)")

    # Sum the total cases & total deaths, calc avg death rate
    total_cases = df.sum(axis=0)[8]
    total_deaths = df.sum(axis=0)[9]
    average_death_rate = total_deaths / total_cases

    # Add avg death rate to dataset
    x_data.append(average_death_rate)
    y_data.append("Average")
    y_label.append(f"{average_death_rate*100:.1f}% ({total_deaths:,} deaths, {total_cases:,} cases)")

    # Sort the axes
    x_data, y_data, y_label = (list(t) for t in zip(*sorted(zip(x_data, y_data, y_label))))

    # Trim data to the amount of max_rows specified
    x_data = x_data[len(x_data)-max_rows:len(x_data)]
    y_data = y_data[len(y_data)-max_rows:len(y_data)]
    y_label = y_label[len(y_label)-max_rows:len(y_label)]

    # Change the colour of the average item
    colours[y_data.index('Average')] = 'red'

    # Plot the graph
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x_data,
        y=y_data,
        text=y_label,
        textposition="outside",
        name="Death rate summary",
        orientation='h',
        marker=dict(
            color=colours,
            line=dict(
                color='rgba(38, 24, 74, 0.8)',
                width=1)
        )
    ))

    fig.update_xaxes(range=[0, 1])

    fig.update_layout(
        title="Plot Title",
        barmode='stack',
        margin={"r":0,"t":0,"l":0,"b":0},
        height=18*max_rows,
        xaxis=dict(
            tickformat=".1%"
        )
        )
    return fig
    



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Use this if not using grid layout
# app.layout = html.Div(children=[

#     html.H1(children='Covid-19 tracker'),
#     html.H2(children='World map'),
#     dcc.Graph(
#         id='World map',
#         config={
#             "displaylogo": False,
#         },
#         figure=generate_map(df1)
#         ),

#     dcc.Graph(
#         id='World map with recoveries',
#         config={
#             "displaylogo": False,
#         },
#         figure=generate_map_w_recoveries(df2)
#         ),

#     html.H2(children='Death rates'),
#     dcc.Graph(
#         id="Death rates",
#         config={
#             "displaylogo": False,
#         },
#         figure=generate_horizontal_bar(df1),
#     ),

#     html.H2(children='Raw data'),
#     generate_table(df1)
# ])

# grid.add_element(col=1, row=1, width=4, height=4, element=html.Div(children=[
#     html.H5(children="Confirmed", style={"height": "8%"}),
#     dcc.Graph(
#         id='World map of confirmed cases',
#         config={
#             "displaylogo": False,
#         },
#         figure=generate_map_w_options(df2, plot_recoveries=False, plot_deaths=False),
#         style={"height": "80%"}
#     )
#     ],
#     # style={"height": "100%", "width": "100%"}
# ))

grid.add_element(col=1, row=1, width=4, height=4, element=dcc.Graph(
    id='World map of confirmed cases',
    config={
        "displaylogo": False,
    },
    figure=generate_map_w_options(df2, plot_recoveries=False, plot_deaths=False),
    style={"height": "100%", "width": "100%"}
))

grid.add_element(col=5, row=1, width=4, height=4, element=dcc.Graph(
    id='World map of confirmed recoveries',
    config={
        "displaylogo": False,
    },
    figure=generate_map_w_options(df2, plot_cases=False, plot_deaths=False),
    style={"height": "100%", "width": "100%"}
))

grid.add_element(col=9, row=1, width=4, height=4, element=dcc.Graph(
    id='World map of confirmed deaths',
    config={
        "displaylogo": False,
    },
    figure=generate_map_w_options(df2, plot_cases=False, plot_recoveries=False),
    style={"height": "100%", "width": "100%"}
))

grid.add_element(col=1, row=5, width=12, height=6, element=dcc.Graph(
    id="Death rates",
    config={
        "displaylogo": False,
    },
    figure=generate_horizontal_bar(df1),
    style={"background-color": "green", "height": "100%", "width": "100%"}
))

grid.add_element(col=1, row=9, width=9, height=2, element=html.Div(
    style={"background-color": "orange", "height": "100%", "width": "100%"}
))

grid.add_element(col=10, row=9, width=3, height=2, element=html.Div(
    style={"background-color": "purple", "height": "100%", "width": "100%"}
))

app.layout = html.Div(
    dui.Layout(
        grid=grid,
    ),
    style={
        'height': '100vh',
        'width': '100vw'
    }
)


if __name__ == '__main__':
    app.run_server(debug=True)