import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from data import df1, df2, filter_df, resources, df_from_path, xth_infection_date
import plotly.graph_objects as go
import plotly.express as px
import datetime
import numpy as np
import dash_ui as dui
import datetime

# Define stylesheets to be used
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://codepen.io/rmarren1/pen/mLqGRg.css'
    ]


# Define some constants to be used throughout
CONFIRMED_COLOUR = 'rgba(102, 153, 255, 0.8)'
RECOVERED_COLOUR = 'rgba(52, 189, 45, 0.8)'
DEATHS_COLOUR = 'rgba(255, 102, 102, 0.8)'
FONT = "Courier New, monospace"

TOOLBAR_BUTTONS = [
  "zoom2d", "pan2d", "select2d", "lasso2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
  "hoverClosestCartesian", "hoverCompareCartesian",
  "zoom3d", "pan3d", "resetCameraDefault3d", "resetCameraLastSave3d", "hoverClosest3d",
  "orbitRotation", "tableRotation",
  "zoomInGeo", "zoomOutGeo", "resetGeo", "hoverClosestGeo",
  "toImage",
  "sendDataToCloud",
  "hoverClosestGl2d",
  "hoverClosestPie",
  "toggleHover",
  "resetViews",
  "toggleSpikelines",
  "resetViewMapbox"
]

def add_buttons_to_default(buttons=["toImage", "resetViews", "resetViewMapbox", "resetGeo", "resetScale2d"], hide_buttons=TOOLBAR_BUTTONS):
    for button in buttons:
        hide_buttons.remove(button)
    return hide_buttons

CHOSEN_BUTTONS = add_buttons_to_default()

MINIMALIST_CONFIG ={
    "displaylogo": False,
    "modeBarButtonsToRemove": CHOSEN_BUTTONS,
}

headline_df = df_from_path(resources['worldwide-aggregated'])
current_date = headline_df.iloc[len(headline_df)-1][0]
current_confirmed = headline_df.iloc[len(headline_df)-1][1]
current_recovered = headline_df.iloc[len(headline_df)-1][2]
current_deaths = headline_df.iloc[len(headline_df)-1][3]

# def generate_table(dataframe, max_rows=999):
#     return html.Table([
#         html.Thead(
#             html.Tr([html.Th(col) for col in ["Country","Population","Province","Last updated","Cases","Deaths"]])
#         ),
#         html.Tbody([
#             html.Tr([
#                 html.Td(dataframe.iloc[i][col]) for col in [1,3,4,5,8,9]
#             ]) for i in range(min(len(dataframe), max_rows))
#         ])
#     ])

# # Create the world map
# def generate_map(df):
#     fig = go.Figure(go.Scattergeo())
#     fig.update_geos(
#         projection_type="natural earth",
#         showcountries=True,
#         countrycolor='rgb(40,40,40)'
#         )
#     fig.update_layout(
#         height=500, 
#         margin={"r":0,"t":0,"l":0,"b":0},
#         showlegend=False,
#         )

#     for location in range((len(df))):
#         # Sort out the naming of each plot point 
#         # (some are just countries, some are country provinces)
#         has_province = True if len(df.iloc[location][4])>1 else False
        
#         location_name = df.iloc[location][1]
#         if has_province:
#             location_name += f" ({df.iloc[location][4]})"

#         # Plot confirmed cases in each area
#         fig.add_trace(go.Scattergeo(
#             lon=[float(df.iloc[location][7])],
#             lat=[df.iloc[location][6]],
#             text=f"{location_name}: {df.iloc[location][8]:,} confirmed",
#             name=location_name + " - confirmed",
#             marker=dict(
#                 size=int(df.iloc[location][8]**(0.5))/10 + 5,
#                 color='rgba(102, 153, 255, 0.8)',
#                 line_color='rgb(40,40,40)',
#                 line_width=0,
#             )
#         ))

#         # Plot deaths in each area
#         fig.add_trace(go.Scattergeo(
#             lon=[float(df.iloc[location][7])],
#             lat=[df.iloc[location][6]],
#             text=f"{location_name}: {df.iloc[location][9]:,} dead",
#             name=location_name + " - deaths",
#             marker=dict(
#                 size=int(df.iloc[location][9]**(0.5))/10 + 2,
#                 color=DEATHS_COLOUR,
#                 line_color='rgb(40,40,40)',
#                 line_width=0,
#             )
#         ))
#     return fig


# Create a world map and plot cases, recoveries and/or deaths
def generate_map_w_options(df, plot_cases=True, plot_recoveries=True, plot_deaths=True):
    latest_date = df.iloc[len(df)-1][2]
    df = filter_df(df,"Date",latest_date)
    
    fig = go.Figure(go.Scattergeo())
    fig.update_geos(
        projection_type="natural earth",
        showcountries=True,
        countrycolor='rgb(40,40,40)'
        )
    
    titletext = "<b>Confirmed"
    if plot_cases:
        titletext += " cases"
    if plot_recoveries:
        titletext += " recoveries"
    if plot_deaths:
        titletext += " deaths"
    titletext += (" " + latest_date)
    titletext += "</b>"
    
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
        font=dict(
            family=FONT,
            size=12,
        ),
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
                    color=CONFIRMED_COLOUR,
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
                    color=DEATHS_COLOUR,
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
                    color=RECOVERED_COLOUR,
                    line_color='rgb(40,40,40)',
                    line_width=0,
                )
            ))

    return fig


# # Plot a horizontal bar chat showing death rates
# def generate_horizontal_bar(df, max_rows=30,cases_cutoff=100):
#     if df.empty():
#         return None
#     top_labels = ['Death rate']
#     colours = []    
#     # Get a list of colours that change as you change values being plotted
#     for row in range(max_rows):
#         colours.append(f'rgb(255,{194/max_rows*(max_rows-row)+92},{153/max_rows*(max_rows-row)})')
    
#     x_data = []
#     y_data = []
#     y_label = []

#     # Gather the data from the dataframe
#     for location in range((len(df))):
#         has_province = True if len(df.iloc[location][4])>1 else False
            
#         location_name = df.iloc[location][1]
#         if has_province:
#             location_name += f" ({df.iloc[location][4]})"

#         if location_name == 'Canada (Diamond Princess)':
#             continue

#         cases = df.iloc[location][8]
#         if cases == 0:
#             cases+=1
#         deaths = df.iloc[location][9]

#         if cases > cases_cutoff:
#             death_rate = deaths/cases
#             x_data.append(death_rate)
#             y_data.append(location_name)
#             y_label.append(f"{death_rate*100:.1f}% ({deaths:,}/{cases:,})")

#     # Sum the total cases & total deaths, calc avg death rate
#     total_cases = df.sum(axis=0)[8]
#     total_deaths = df.sum(axis=0)[9]
#     average_death_rate = total_deaths / total_cases

#     # Add avg death rate to dataset
#     x_data.append(average_death_rate)
#     y_data.append("Average")
#     y_label.append(f"{average_death_rate*100:.1f}% ({total_deaths:,}/{total_cases:,})")

#     # Sort the axes
#     x_data, y_data, y_label = (list(t) for t in zip(*sorted(zip(x_data, y_data, y_label))))

#     # Trim data to the amount of max_rows specified
#     if max_rows > len(x_data):
#         x_data = x_data[len(x_data)-max_rows:len(x_data)]
#         y_data = y_data[len(y_data)-max_rows:len(y_data)]
#         y_label = y_label[len(y_label)-max_rows:len(y_label)]

#     # Change the colour of the average item
#     colours[y_data.index('Average')] = 'red'

#     # Plot the graph
#     fig = go.Figure()
#     fig.add_trace(go.Bar(
#         x=x_data,
#         y=y_data,
#         text=y_label,
#         textposition="outside",
#         name="Death rate summary",
#         orientation='h',
#         marker=dict(
#             color=colours,
#             line=dict(
#                 color='rgba(38, 24, 74, 0.8)',
#                 width=1)
#         )
#     ))

#     fig.update_xaxes(range=[0, 1])

#     fig.update_layout(
#         title=f"Worst death rates ({cases_cutoff}+ cases)",
#         barmode='stack',
#         margin={"r":0,"t":30,"l":0,"b":0},
#         height=18*max_rows,
#         xaxis=dict(
#             tickformat=".1%",
#         ),
#         font=dict(
#             family=FONT,
#             size=12,
#         )
#         )

#     fig.update_yaxes(tickfont=dict(size=10),)
#     return fig


# Plot death rate bar chart by country level
def generate_deathrates_by_country(resources=resources, max_rows=30, min_cases=100, min_deaths=50, date=False):
    df = df_from_path(resources['countries-aggregated'])
    
    # If no date is given, take the latest
    if not date:
        date = df.iloc[len(df)-1,0] 
    df = filter_df(df, "Date", date)
    
    # Set up for the data
    x_data = []
    y_data = []
    y_label = []

    # Gather the data from the dataframe
    for location in range((len(df))):            
        location_name = df.iloc[location][1]
        # Acronymize location name if it's more than 1 word and is too long
        if len(location_name.split(" ")) > 1 and len(location_name) > 13:
            location_abbv = ""
            for word in location_name.split(" "):
                location_abbv += word[0]
            location_name = location_abbv

        cases = df.iloc[location][2]
        if cases == 0:
            cases+=1
        deaths = df.iloc[location][4]

        if cases > min_cases and deaths > min_deaths:
            death_rate = deaths/cases
            x_data.append(death_rate)
            y_data.append(location_name)
            y_label.append(f"{death_rate*100:.1f}% ({deaths:,}/{cases:,})")

    num_rows = min(max_rows, len(x_data))

    # Get a list of colours that change as you change values being plotted
    colours = []
    for row in range(num_rows+1):
        colours.append(f'rgb(255,{194/num_rows*(num_rows-row)+92},{153/num_rows*(num_rows-row)+20})')

    # Sum the total cases & total deaths, calc avg death rate
    total_cases = df.sum(axis=0)[2]
    total_deaths = df.sum(axis=0)[4]
    average_death_rate = total_deaths / total_cases

    # Add avg death rate to dataset
    x_data.append(average_death_rate)
    y_data.append("Average")
    y_label.append(f"{average_death_rate*100:.1f}% ({total_deaths:,}/{total_cases:,})")

    # Sort the axes
    x_data, y_data, y_label = (list(t) for t in zip(*sorted(zip(x_data, y_data, y_label))))

    # Trim data to the amount of max_rows specified
    x_data = x_data[len(x_data)-max_rows:len(x_data)]
    y_data = y_data[len(y_data)-max_rows:len(y_data)]
    y_label = y_label[len(y_label)-max_rows:len(y_label)]

    # Change the colour of the average item
    try:
        colours[y_data.index('Average')] = 'rgb(102, 153, 255)'
    except:
        print(f"Average not in top {num_rows}")

    # Plot the graph
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=y_data[::-1],
        y=x_data[::-1],
        text=y_label[::-1],
        # textposition="outside",
        name="Death rate summary",
        orientation='v',
        marker=dict(
            color=colours[::-1],
            line=dict(
                color='rgba(38, 24, 74, 0.8)',
                width=1)
        )
    ))

    fig.update_yaxes(range=[0, 0.2])

    fig.update_layout(
        title={
            'text': f"<b>Death rates ({min_cases}+ cases, {min_deaths}+ deaths)</b>",
            'x': 0.5,
            'xanchor': 'center',
        },
        barmode='stack',
        margin={"r":15,"t":30,"l":10,"b":10, "pad":5},
        width=18*num_rows,
        yaxis=dict(
            tickformat=".1%",
        ),
        xaxis_tickangle=-90,
        font=dict(
            family=FONT,
            size=12,
        )
        )

    fig.update_yaxes(tickfont=dict(size=12),)
    return fig


# Time series graph with lines for confirmed, recovered and deaths
def generate_world_ts_options(resources=resources, plot_confirmed=True, plot_recovered=True, plot_deaths=True):
    df = df_from_path(resources['worldwide-aggregated']) 
    
    # Add data
    date = df['Date'].tolist()
    confirmed = df['Confirmed'].tolist()
    recovered = df['Recovered'].tolist()
    deaths = df['Deaths'].tolist()

    fig = go.Figure()

    # Create and style traces
    if plot_confirmed:
        fig.add_trace(go.Scatter(x=date, y=confirmed, name='Cases',
                                line=dict(color=CONFIRMED_COLOUR, width=2)))
    if plot_recovered:
        fig.add_trace(go.Scatter(x=date, y=recovered, name = 'Recoveries',
                                line=dict(color=RECOVERED_COLOUR, width=2)))
    if plot_deaths:
        fig.add_trace(go.Scatter(x=date, y=deaths, name='Deaths',
                                line=dict(color=DEATHS_COLOUR, width=2)))

    # Edit the layout
    fig.update_layout(
        title={
            'text': f"<b>Global confirmed numbers over time</b>",
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.95,
        },
        margin={"r":10,"t":40,"l":10,"b":5},
        font=dict(
            family=FONT,
            size=12,
        ),
        xaxis_title='Date',
        yaxis_title='Confirmed numbers',
        hovermode='x')

    fig.update_yaxes(nticks=10)
    fig.update_xaxes(nticks=10)

    return fig

# Create a time series for different countries where we have "day 0" etc. 
# instead of actual dates - this is better for comparability
def generate_comparable_time_series(
        countries=["China", "United Kingdom", "Italy", "Spain", "Iran", "US", "Korea, South"], 
        df=df_from_path(resources['countries-aggregated']),
        xth_infection=100, 
        plot_confirmed=True, 
        plot_recovered=False, 
        plot_deaths=False
        ):
    
    fig = go.Figure()

    for country in countries:

        hth_date = xth_infection_date(country, xth_infection, df)
        
        # Filter the dataframe for country and date of 100th infection
        country_df = df.loc[df["Country"] == country]
        country_df = country_df[country_df['Date'] >= hth_date]

        x_axis_data = []
        y_axis_data = country_df['Confirmed'].tolist()

        for i in range(len(y_axis_data)):
            x_axis_data.append(i)

        fig.add_trace(go.Scatter(x=x_axis_data, y=y_axis_data, name=country))
   
    # Edit the layout
    fig.update_layout(
        title={
            'text': f"<b>Confirmed cases over time (day 0 = {xth_infection:,} infections)</b>",
            'x': 0.5,
            'xanchor': 'center',
        },
        margin={"r":10,"t":30,"l":10,"b":0},
        font=dict(
            family=FONT,
            size=12,
        ),
        xaxis_title=f'Days since {xth_infection}th infection',
        yaxis_title='Confirmed cases',
        hovermode='x')

    fig.update_yaxes(nticks=10)
    fig.update_xaxes(nticks=10)

    return fig


# 
def generate_datatable(df=df_from_path(resources['countries-aggregated']),date=False):

    # If no date is given, take the latest
    if not date:
        date = df.iloc[len(df)-1,0] 
    df = filter_df(df, "Date", date)

    # Filter out the date column
    df = df[['Country', 'Confirmed', 'Recovered', 'Deaths']]

    return df

df_datatable = generate_datatable()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Define the grid 
grid = dui.Grid(_id="grid", num_rows=12, num_cols=12, grid_padding=0)


# Add elements to the grid
grid.add_element(col=1, row=1, width=4, height=4, element=dcc.Graph(
    id='World map of confirmed cases',
    config=MINIMALIST_CONFIG,
    figure=generate_map_w_options(df2, plot_recoveries=False, plot_deaths=False),
    style={"height": "100%", "width": "100%"}
))

grid.add_element(col=5, row=1, width=4, height=4, element=dcc.Graph(
    id='World map of confirmed recoveries',
    config=MINIMALIST_CONFIG,
    figure=generate_map_w_options(df2, plot_cases=False, plot_deaths=False),
    style={"height": "100%", "width": "100%"}
))

grid.add_element(col=9, row=1, width=4, height=4, element=dcc.Graph(
    id='World map of confirmed deaths',
    config=MINIMALIST_CONFIG,
    figure=generate_map_w_options(df2, plot_cases=False, plot_recoveries=False),
    style={"height": "100%", "width": "100%"}
))


grid.add_element(col=1, row=5, width=3, height=4, element=dash_table.DataTable(
    id="Table",
    columns=[{"name": i, "id": i} for i in df_datatable.columns],
    data=df_datatable.to_dict('records'),
    sort_action="native",
    sort_by=[{"column_id": "Confirmed", "direction": "desc"}],
))



grid.add_element(col=4, row=5, width=3, height=4, element=html.Div(
    [
        html.H4(
            ["Covid-19 dashboard"],
            style={"font-weight": "bold"}
        ),
        html.H6("Worldwide headline figures:"),
        html.Div([
            html.H6(
                [f"Confirmed: {current_confirmed:,}"],
                style={"color": CONFIRMED_COLOUR, "font-weight": "bold"}
            ),
            html.H6(
                [f"Recovered: {current_recovered:,}"],
                style={"color": RECOVERED_COLOUR, "font-weight": "bold"}
            ),
            html.H6(
                [f"Deceased: {current_deaths:,}"],
                style={"color": DEATHS_COLOUR, "font-weight": "bold"}
            ),
            html.P(
                [f"Data accurate as at {current_date}"]
            ),
            html.P(
                ["Created by Christian Kneller"]
            ),
            html.P(
                [
                    "Source code available at ",
                    html.A("github", href="https://github.com/ChrisKneller/covid-dashboard/", target="_blank")
                ]
            )

        ])
    ],
    style={
        "font-family": FONT, 
        "text-align":"center", 
        "background-color": "white", 
        "height": "100%",
        "display": "flow-root"},
))

grid.add_element(col=7, row=5, width=6, height=4, element=dcc.Graph(
    id="Comparable time series",
    config=MINIMALIST_CONFIG,
    figure=generate_comparable_time_series(xth_infection=1000),
    style={"height": "100%", "width": "100%"}
))

grid.add_element(col=1, row=9, width=7, height=4, element=dcc.Graph(
    id="Overall time series",
    config=MINIMALIST_CONFIG,
    figure=generate_world_ts_options(),
    style={"height": "100%", "width": "100%"}
))

grid.add_element(col=8, row=9, width=5, height=4, element=dcc.Graph(
    id="Death rates",
    config=MINIMALIST_CONFIG,
    figure=generate_deathrates_by_country(max_rows=500),
    style={"height": "100%", "width": "100%",}
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