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
    
    # df.iloc[location][5] = f"{df.iloc[location][5]:%Y-%m-%d %H:%M}"

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
            color='rgb(51,102,255)',
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
            color='red',
            line_color='rgb(40,40,40)',
            line_width=0,
        )
    ))



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.H1(children='Covid-19 tracker'),
    html.H2(children='World map'),
    dcc.Graph(
        id='World map',
        config={
            "displaylogo": False,
        },
        figure=fig
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
    html.H2(children='Raw data'),
    generate_table(df)
])

if __name__ == '__main__':
    app.run_server(debug=True)