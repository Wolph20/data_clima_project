
from datetime import date
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import requests, json
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans
import plotly.graph_objects as go

def extr_list(data, reg):
    for item in data:
        if item['Antena']==reg:
            return item['Temp_values']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

us_cities = pd.read_csv("procesdata.csv")
region = us_cities['Antena'].unique()

app.layout = html.Div(children=[
    
                html.Div(id='my-output'),
    
                html.H1(children='Bienvenido'),

                html.Div(children='''
                    Un servicio web para consultar información sobre cultivos.
                '''),
    
                html.Div([
                    dcc.Input(
                    id='lat1', 
                    type='text', 
                    placeholder='Latitud 1',
                    value=''
                    )
                ],style={'padding':5, 'display':'inline-flex'}),
                
                html.Div([
                    dcc.Input(
                    id='long1', 
                    type='text', 
                    placeholder='Longitud 1',
                    value=''
                    )
                ],style={'padding':5, 'display':'inline-flex'}),
                
                html.Div([
                    dcc.Input(
                    id='lat2', 
                    type='text', 
                    placeholder='Latitud 2',
                    value=''
                    )
                ],style={'padding':5, 'display':'inline-flex'}),
                
                html.Div([
                    dcc.Input(
                    id='long2', 
                    type='text', 
                    placeholder='Longitud 2',
                    value=''
                    )
                ],style={'padding':5, 'display':'inline-flex'}),
                
                html.Div([
                    dcc.Input(
                    id='lat3', 
                    type='text', 
                    placeholder='Latitud 3',
                    value=''
                    )
                ],style={'padding':5, 'display':'inline-flex'}),
                
                html.Div([
                    dcc.Input(
                    id='long3', 
                    type='text', 
                    placeholder='Longitud 3',
                    value=''
                    )
                ],style={'padding':5, 'display':'inline-flex'}), 
               
                html.Div([
                    dcc.Input(
                    id='fech_ini', 
                    type='text', 
                    placeholder='Fecha de inicio',
                    value='24/01/2019'
                    )
                ],style={'padding':5, 'display':'inline-flex'}),
                html.Div([
                    dcc.Input(
                    id='fech_fin', 
                    type='text', 
                    placeholder='Fecha de termino',
                    value='31/01/2019'
                    )
                ],style={'padding':5, 'display':'inline-flex'}),
                html.Div([
                    dcc.Input(
                    id='prod', 
                    type='text', 
                    placeholder='Producto',
                    value=''
                    )
                ],style={'padding':5, 'display':'inline-flex'}),  
        

            html.Button('submit', id='bt1'),
            html.Br(),
            
            dcc.Graph(style={
            'textAlign': 'center'},
            id='example-graph'
            ),
            html.H2(children='Regressión lineal'),
            html.P("Selecciona un región:"),
            dcc.Dropdown(
                id='reg',
                options=[{'label': i, 'value': i} for i in region],
                value='MONCLOVA'
            ),
            
            html.Br(),
            dcc.Graph(style={
            'textAlign': 'center'},
            id='regresion-graph'
            )
              
    
], style={'padding':50})


@app.callback(
              Output('example-graph', 'figure'),
              [Input('bt1', 'n_clicks')],
              [State('lat1', 'value'), State('long1', 'value'),
               State('lat2', 'value'), State('long2', 'value'),
               State('lat3', 'value'), State('long3', 'value'),
               State('fech_ini', 'value'), State('fech_fin', 'value'),
               State('prod', 'value')])

def update_figure(n_clicks, lat1, long1, lat2, long2, lat3, long3, fech_ini, fech_fin, prod):
    data = {
        "lat1":lat1,
        "long1":long1,
        "lat2":lat2,
        "long2":long2,
        "lat3":lat3,
        "long3":long3,
        "fech_ini":fech_ini,
        "fech_fin":fech_fin,
        "prod":prod,
       }
    
    url = "http://148.247.204.81:6654/consume"
    token = "Bearer, asn,jdijijineen,dnadanancja"
    _headers = {'Content-Type': 'application/json', 'Authorization': token}
    response = requests.post(url, data=json.dumps(data), headers= _headers)
    Re = json.loads(response.content)
    data = Re['results']
    
    import csv
    csv_columns = ['Antena','Latitud','Longitud','Temperatura media','Humedad','Precipitacion','Cultivo','Fiabilidad de siembra']

    csv_file = "procesdata.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in data:
                writer.writerow(data)
    except IOError:
        print("I/O error")
    
    us_cities = pd.read_csv("procesdata.csv")
    
    kmeans = KMeans(n_clusters=4, random_state=0).fit(us_cities[['Fiabilidad de siembra']])
    b=kmeans.labels_
    # print(b)
    
    fig1 = px.scatter_mapbox(us_cities, lat="Latitud", lon="Longitud", hover_name="Antena", hover_data=["Temperatura media","Humedad","Precipitacion","Cultivo","Fiabilidad de siembra"], zoom=4, height=700,width=1000,color=kmeans.labels_)
    fig1.update_layout(mapbox_style="open-street-map")
    
    # url_reg = "http://148.247.204.81:6654/regression"
    # response_reg = requests.get(url_reg)
    # Re_reg = json.loads(response_reg.content)
    # data_reg = Re_reg['results']
    
    # # dataX = [24.26038, 22.17001, 23.293, 23.05609, 20.31677, 21.24933, 22.09729, 23.59164]
    # dataX = extr_list(data_reg, reg)
    # X_train = np.array(dataX)
    # Y_train = np.arange(1, len(dataX)+1)
    
    # coeficientes = np.polyfit(Y_train,X_train,1)
    # polinomio = np.poly1d(coeficientes)
    # ys = polinomio(Y_train)
    
    # fig2 = go.Figure([
    #     go.Scatter(x=Y_train.squeeze(), y=X_train, 
    #                name='Temperaturas', mode='markers'),
    #     # go.Scatter(x=X_test.squeeze(), y=y_test, 
    #     #            name='test', mode='markers'),
    #     go.Scatter(x=Y_train, y=ys, name='Regresión')])
    
    
    return fig1


if __name__ == '__main__':
    app.run_server(debug=True)