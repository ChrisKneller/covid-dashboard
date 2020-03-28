import dash
import dash_core_components as dcc
import dash_html_components as html
from data import df
import plotly.graph_objects as go

# print(df)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def generate_table(dataframe, max_rows=999):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

fig = go.Figure(go.Scattergeo())
fig.update_geos(
    projection_type="natural earth",
    showcountries=True,
    countrycolor='rgb(40,40,40)')
fig.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})

# fig.add_trace(go.Scattergeo(
#     lon=[25.006],
#     lat=[13.963],
#     text='Hi Emma!',
#     name='Test entry',
#     marker=dict(
#         size=15,
#         color='rgb(239,0,255)',
#         line_width=0.5
#     )
# ))

# Plot confirmed cases in each area
for location in range((len(df)+1)):
    try:
        fig.add_trace(go.Scattergeo(
            lon=[float(df.iloc[location][7])],
            lat=[df.iloc[location][6]],
            text=f"{df.iloc[location][1]} ({df.iloc[location][4]}): {df.iloc[location][8]} confirmed",
            name=df.iloc[location][1],
            marker=dict(
                size=int(df.iloc[location][8]**(0.5))/10 + 5,
                color='rgb(51,102,255)',
                line_color='rgb(40,40,40)',
                line_width=0.5,
            )
        ))
    except:
        pass

# Plot deaths in each area
for location in range((len(df)+1)):
    try:
        fig.add_trace(go.Scattergeo(
            lon=[float(df.iloc[location][7])],
            lat=[df.iloc[location][6]],
            text=f"{df.iloc[location][1]} ({df.iloc[location][4]}): {df.iloc[location][9]} dead",
            name=df.iloc[location][1],
            marker=dict(
                size=int(df.iloc[location][9]**(0.5))/10 + 2,
                color='red',
                line_color='rgb(40,40,40)',
                line_width=0.5,
            )
        ))
    except:
        pass


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.H1(children='Covid-19 tracker'),
    html.H2(children='World map'),
    dcc.Graph(
        id='World map?',
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