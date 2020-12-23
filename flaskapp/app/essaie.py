

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn import linear_model, tree, neighbors

df = px.data.tips()
X = df.total_bill.values[:, None]
X_train, X_test, y_train, y_test = train_test_split(
    X, df.tip, random_state=42)

models = {'Regression': linear_model.LinearRegression}

app = dash.Dash(__name__)

app.layout = html.Div([
    html.P("Select Model:"),
    dcc.Dropdown(
        id='model-name',
        options=[{'label': x, 'value': x} 
                 for x in models],
        value='Regression',
        clearable=False
    ),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"), 
    [Input('model-name', "value")])
def train_and_display(name):
    
    dataX = [24.26038, 22.17001, 23.293, 23.05609, 20.31677, 21.24933, 22.09729, 23.59164]
    X_train = np.array(dataX)
    Y_train = np.arange(1, len(dataX)+1)
    
    coeficientes = np.polyfit(Y_train,X_train,1)
    polinomio = np.poly1d(coeficientes)
    ys = polinomio(Y_train)
    
    fig = go.Figure([
        go.Scatter(x=Y_train.squeeze(), y=X_train, 
                   name='Temperaturas', mode='markers'),
        # go.Scatter(x=X_test.squeeze(), y=y_test, 
        #            name='test', mode='markers'),
        go.Scatter(x=Y_train, y=ys, name='Regresión')])
                  

    return fig

app.run_server(debug=True)