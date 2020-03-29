import dash
import dash_core_components as dcc
import dash_html_components as html
from data import df
import plotly.graph_objects as go
import datetime

# print(df)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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
                color='rgb(102, 153, 255)',
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
                color='rgb(255, 102, 102)',
                line_color='rgb(40,40,40)',
                line_width=0,
            )
        ))
    return fig


def generate_horizontal_bar(df, max_rows=50):
    top_labels = ['Death rate']
    # colours = ['rgb(204, 204, 255)',] * max_rows
    colours = []    
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

    # Sort the two axes
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
        barmode='stack',
        margin={"r":0,"t":0,"l":0,"b":0},
        height=18*max_rows,
        xaxis=dict(
            tickformat=".1%"
        )
        )
    return fig
    



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.H1(children='Covid-19 tracker'),
    html.H2(children='World map'),
    dcc.Graph(
        id='World map',
        config={
            "displaylogo": False,
        },
        figure=generate_map(df)
        ),

    # html.Div(children='''
    #     Dash: A web application framework for Python.
    # '''),

    # dcc.Graph(
    #     id='example-graph',
    #     figure={
    #         'data': [
    #             {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
    #             {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
    #         ],
    #         'layout': {
    #             'title': 'Dash Data Visualization'
    #         }
    #     }
    # ),
    html.H2(children='Death rates'),
    dcc.Graph(
        id="Death rates",
        config={
            "displaylogo": False,
        },
        figure=generate_horizontal_bar(df),
    ),

    html.H2(children='Raw data'),
    generate_table(df)
])

if __name__ == '__main__':
    app.run_server(debug=True)