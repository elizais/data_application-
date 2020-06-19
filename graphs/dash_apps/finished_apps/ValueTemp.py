import dash
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash
import plotly.graph_objs as go
from graphs.models import Sensor


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
sensor = Sensor.objects.filter(characteristic__startswith='Температура')
sens = dict()
s = []
for i in range(len(sensor)):
    p = sensor[i].points.all()
    val = [p[j].value for j in range(len(p))]
    pub_date = [p[j].pub_date for j in range(len(p))]
    sens[str(sensor[i])] = {'point': val, 'date': pub_date, 'limit': [sensor[i].range_min, sensor[i].range_max]}
    s.append(str(sensor[i]))

app = DjangoDash('ValueTemp', external_stylesheets=external_stylesheets)

app.layout = html.Div([html.Div(
id="graph-container",
children=[
    html.H1('Данные температуры'),
    dcc.Graph(id='graph', animate=True, style={"backgroundColor": "#ffffff"}),
    html.Label('Адрес:'),
    dcc.Dropdown(
        id="line",
        options=[{"label": s[t], "value": s[t]} for t in range(len(s))],
        value=[s[0]],
        multi=True
    ),
    #html.Label('Поиск значений вышедших за пределы измерений'),
    #html.Button('Поиск', id='search', n_clicks=0)
]),])


@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('line', 'value')])
def update_figures(value):
    data = go.Figure()

    for l in range(len(value)):
        data.add_trace(go.Scatter(
            x=sens[value[l]]['date'],
            y=sens[value[l]]['point'],
            name=value[l],
            mode='lines',
            text=value[l]))
        datapoint = dict()
        datapoint['date'] = [sens[value[l]]['date'][z] for z in range(len(sens[value[l]]['date'])) if
                     sens[value[l]]['limit'][1] < sens[value[l]]['point'][z]
                             or sens[value[l]]['point'][z] < sens[value[l]]['limit'][0]]
        datapoint['point'] = [sens[value[l]]['point'][z] for z in range(len(sens[value[l]]['date'])) if
                     sens[value[l]]['limit'][1] < sens[value[l]]['point'][z]
                              or sens[value[l]]['point'][z] < sens[value[l]]['limit'][0]]

        data.add_trace(go.Scatter(
            x=datapoint['date'],
            y=datapoint['point'],
            name=value[l] + ' limit',
            mode='markers',
            marker=dict(color='red', size=10),
            ))

    data.update_layout(
        yaxis={'title': 'Температура'},
        showlegend=False,
        height=600,
        template="plotly_white"
        )

    return data #{'data': data, 'layout': layout}

