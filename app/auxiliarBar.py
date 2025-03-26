import pandas as pd
from dash import html, dcc
import plotly.graph_objects as go

def createBarplot_industrias(df_industrial,año_sel,feature=None):
    if not feature:
        return [html.P("Selecciona un municipio")]
    nombre = feature["properties"]["CVE_MUN"]
    #df_industrial = pd.read_csv('Datos/CSVs//estatal_industrias_ballasaM.csv')
    row = df_industrial[df_industrial['cve_mun'] == int(nombre)].iloc[:, 2:]
    if row.empty:
        return [html.P(f"No data available for {nombre}")]
    data = row.iloc[0].to_dict()
    data = {k: (0 if pd.isna(v) else v) for k, v in data.items()}
    data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True)[:5])
    x = list(data.keys())
    y = list(data.values())
    
    y = [round(val, 2) if val >= 0.01 else "<0.01" for val in y]
    
    fig = go.Figure(
        data=go.Bar(
            x=y, 
            y=x,
            orientation='h',
            width=0.5,
            offset=-0.65,
            texttemplate="%{x}"
        ),
        layout={
            'title': {
                'text': f'Industrias con mayor personal en <br> {feature["properties"]["NOM_MUN"]} ({año_sel})',
                'font':{'size':10},
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
            },

            'height': 300,
            'yaxis': {'anchor': 'free', 'side': 'right'},
        }
    )
    return [dcc.Graph(figure=fig.update_layout(
    margin=dict(l=20, r=20, t=30, b=20),
), style={'height': '300px','width':'350px'})]