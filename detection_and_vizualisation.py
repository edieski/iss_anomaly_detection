import plotly.graph_objs as go
import plotly.io as pio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from statsmodels.tsa.arima_model import ARIMA

# Set up the initial figure and traces
fig = go.Figure()
fig.add_trace(go.Scatter(x=[], y=[], name='Data'))
fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name='Prediction'))
fig.add_trace(go.Scatter(x=[], y=[], mode='markers', marker=dict(color='red'), name='Anomaly'))

# Set up the axis labels and title
fig.update_xaxes(title_text='Date')
fig.update_yaxes(title_text='Value')
fig.update_layout(title_text='Real-time Forecasting')

# Define the update function for the animation
def update(frame):
    # Retrieve the time series data from the database
    sql = "SELECT * FROM mytable WHERE timestamp > %s"
    data = pd.read_sql(sql, connection, params=[frame], index_col='timestamp', parse_dates=True)

    if len(data) > 0:
        # Preprocess the data
        data = (data - data.mean()) / data.std() # normalize the data

        # Train the ARIMA model
        model = ARIMA(data, order=(1, 1, 1))
        model_fit = model.fit()

        # Make a prediction for the next time step
        prediction = model_fit.forecast(steps=1)[0][0]

        # Plot the data and predictions
        fig.data[0].x = data.index
        fig.data[0].y = data.values
        fig.data[1].x = [frame, frame + pd.Timedelta(hours=1)]
        fig.data[1].y = [prediction, prediction]

        # Highlight any values that exceed a threshold
        threshold = 2.0
        diff = abs(data.values - prediction)
        anomalies = data.index[diff > threshold]
        if len(anomalies) > 0:
            fig.data[2].x = anomalies
            fig.data[2].y = data.loc[anomalies]
        else:
            fig.data[2].x = []
            fig.data[2].y = []

    return fig

# Set up the animation
fig.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=[dict(label='Play', method='animate', args=[None, {'frame': {'duration': 10000, 'redraw': True}, 'fromcurrent': True, 'transition': {'duration': 0}}]), dict(label='Pause', method='animate', args=[[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}])])])
frames = []
start_date = datetime.now()
for i in range(10):
    frames.append(dict(data=[], name=start_date + timedelta(seconds=10 * i)))
fig.frames = frames
fig.update_layout(transition={'duration': 0})

# Save the animation as an HTML file
pio.write_html(fig, file='realtime_forecasting.html', auto_open=True)

# Close the database connection
connection.close()
