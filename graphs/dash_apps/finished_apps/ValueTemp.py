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
limit = []
for i in range(len(sensor)):
    p = sensor[i].points.all()
    val = [p[j].value for j in range(len(p))]
    pub_date = [p[j].pub_date for j in range(len(p))]
    sens[str(sensor[i])] = {'point': val, 'date': pub_date}
    s.append(str(sensor[i]))
    limit.append([sensor[i].range_min, sensor[i].range_max])

app = DjangoDash('ValueTemp', external_stylesheets=external_stylesheets)

app.layout = html.Div([html.Div(
id="graph-container",
children=[
    html.H1(children='Данные температуры'),
    dcc.Graph(id='graph', animate=True, style={"backgroundColor": "#ffffff"}),
    html.Label('Адрес:'),
    dcc.Dropdown(
        id="line",
        options=[{"label": s[t], "value": s[t]} for t in range(len(s))],
        value=[s[0]],
        multi=True
    ),
    html.Label('Поиск значений вышедших за пределы измерений'),
    html.Button('Поиск', id='search', n_clicks=0)
]),])


@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('line', 'value')])
def update_figures(value):
    data = []
    for l in range(len(value)):
        data.append(go.Scatter(
            x=sens[value[l]]['date'],
            y=sens[value[l]]['point'],
            name=value[l],
            mode='lines',
            visible=True,
            text=value[l]))
    layout = go.Layout(
        yaxis={'title': 'Температура'},
        showlegend=False,
        height=600,
        )

    return {'data': data, 'layout': layout}

