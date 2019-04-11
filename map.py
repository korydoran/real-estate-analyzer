import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline

mapbox_access_token = 'pk.eyJ1Ijoia29yeWRvcmFuIiwiYSI6ImNqc3FxOGEyNzBuMDM0M294cXAwMHpzdG4ifQ.T2c7SfQC1_ND6Y1XTo6Rww'

df = pd.read_csv('eugene_02282019_all.csv')
#print (df)
df['text'] = df['0'] + ' ' + df['1'] + ', ' + df['2']
data = [
    go.Scattermapbox(
        lon = df['longs'],
        lat = df['lats'],
       ## text = df['text'] + ', ',
        mode = 'markers',
        marker = dict(
            size = 8,
            ),
        text = df['text']


        )]

layout = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=44.0521,
            lon=-123.0868
        ),
        pitch=0,
        zoom=10
    ),
)



fig = dict(data=data, layout=layout)
#py.iplot(fig, filename='Multiple Mapbox')
plotly.offline.plot( fig,  filename='eugenemapgood.html' )

