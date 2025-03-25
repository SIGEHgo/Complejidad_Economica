import pandas as pd
from dash import dcc
import re
import plotly.express as px
##Corregir los nombres de los renglones seleccionados. 
##Debe actualizarse si se hace el cambio de unidad de medida. 
def generateTimeSeries(df_estatal, n_array, unidad):
    if unidad == 'personal':
        columnas = slice(1, 19)
        fig = px.line(title="ICE histórico. Promedio de personal", labels={"x": "Año", "y": "ICE a nivel estatal"})

    else:
        columnas = slice(19, 37)
        fig = px.line(title="ICE histórico. Número de Unidades Económicas", labels={"x": "Año", "y": "ICE a nivel estatal"})
    for n in n_array:
        row = df_estatal.iloc[n, columnas]
        colnames = row.index
        numbers_and_chars = [re.findall(r'(\d+)-?(\w+)?', colname) for colname in colnames]
        x_axis_labels = ['-'.join(match[0]) for match in numbers_and_chars]
        fig.add_scatter(x=x_axis_labels, y=row.values, mode='lines', name=f"{df_estatal.iloc[n]['NOM_MUN']}")
    
    fig.update_layout(showlegend=True, plot_bgcolor='white', xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
    
    return fig