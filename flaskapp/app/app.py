import requests, json
# import numpy as np
# import plotly.graph_objects as go
# import plotly.express as px
# from sklearn.model_selection import train_test_split
# from sklearn import linear_model, tree, neighbors
# import matplotlib.pyplot as plt

# dataX = [24.26038, 22.17001, 23.293, 23.05609, 20.31677, 21.24933, 22.09729, 23.59164]
# X_train = np.array(dataX)
# Y_train = np.arange(1, len(dataX)+1).reshape(-1, 1)

# model = linear_model.LinearRegression()
# model.fit(Y_train, X_train)

# x_range = np.linspace(X_train.max(), X_train.min(), 100)
# y_range = model.predict(x_range.reshape(-1, 1))

# print(x_range)
# print(y_range)

# # print(model.coef_)
# # print(model.intercept_)

# # plt.scatter(x=Y_train, y=X_train, color='green')
# plt.plot(x_range, y_range, color='blue')

# plt.ylabel('Días')
# plt.xlabel('Temperaturas')
# # plt.show()

# # [20.04749, 19.79544, 20.20349, 20.20184, 17.91934, 19.89279, 19.51328, 19.61279]
# # [24.26038, 22.17001, 23.293, 23.05609, 20.31677, 21.24933, 22.09729, 23.59164]

data = [{'Antena': 'MONCLOVA', 'Temp_values': [25.29181, 23.12988, 24.14536, 24.99347, 20.84778, 22.82306, 23.30865, 24.19189]}, {'Antena': 'VILLA LUIS GIL', 'Temp_values': [23.4]}, {'Antena': 'TEZONCUALPA', 'Temp_values': [11.70258]}, 
        {'Antena': 'CREDMOTOZINTLA', 'Temp_values': [19.51074, 19.42389, 19.13336, 19.19495, 18.56638, 18.77496, 18.12192, 18.21606]}, 
        {'Antena': 'PAREDON', 'Temp_values': [23.53238, 23.43976, 22.20782, 24.40271, 24.11414, 24.42255]}]

reg = "PAREDON"

def extr_list(data, reg):
    for item in data:
        if item['Antena']==reg:
            return item['Temp_values']

print(extr_list(data, reg))

url_reg = "http://127.0.0.1:6654/regression"
response_reg = requests.get(url_reg)
Re_reg = json.loads(response.content)
data_reg = Re_reg['results']

# dataX = [24.26038, 22.17001, 23.293, 23.05609, 20.31677, 21.24933, 22.09729, 23.59164]
dataX = extr_list(data_reg, reg)