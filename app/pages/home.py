import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, no_update
import dash_leaflet as dl
import json
#Locales
import auxiliarLeafltet
import auxiliarLine
import auxiliarNetwork
import auxiliarScatter
import auxiliarBar
from auxiliarJS import info, classes, colorscale, style, style_handle, on_each_feature, defStyle
#Procesos
import pandas as pd
import geopandas as gpd
import numpy as np
import re
dash.register_page(__name__, path='/')

##Primeras ejecuciones 
df_estatal = pd.read_csv('Datos/CSVs/estatal.csv')
df_estatal.columns = [col.replace('.', '') for col in df_estatal.columns]
new_names = []
for name in df_estatal.columns:
    if name.endswith('A'):
        new_names.append(name[:-1] + '-I')
    elif name.endswith('B'):
        new_names.append(name[:-1] + '-II')
    else:
        new_names.append(name)
df_estatal.columns = new_names
#print(df_estatal.columns)
# Store the columns of the DataFrame into a list
columns_list = df_estatal.columns.tolist()
# Print the list of columns to check

lista_de_opciones_personal = [col for col in columns_list if 'Personal' in col]
lista_de_opciones_unidades = [col for col in columns_list if 'Unidades' in col]
gdf_shapefile=gpd.read_file('Datos/geojson_hgo.geojson')
gdf_shapefile= gdf_shapefile.sort_values(by='CVEGEO')
gdf_shapefile=gdf_shapefile.reset_index()
df_estatal['NOM_MUN'] = gdf_shapefile['NOM_MUN']

map_default=auxiliarLeafltet.generateMapFromElection(lista_de_opciones_personal[-1],df_estatal,gdf_shapefile)
df_industrial=pd.read_csv("Datos/CSVs/Balassa_Modificado_Historico/Balassa_Mod_Nivel_Municipio_por_Grupos_2024B.csv")
radio_items_original=[
                {'label': 'Promedio de personal', 'value': 'personal', },
                {'label': 'Unidades económicas', 'value': 'unidades',}]
radio_items_personal=[
                {'label': 'Promedio de personal', 'value': 'personal'},]


with open('Datos/Explicaciones breves.txt', encoding='utf-8') as f:
    explicaciones_breves = json.load(f)
accordion =  dbc.Accordion(
    [
        dbc.AccordionItem(###############     ICE
        [
            html.P(explicaciones_breves.get('Complejidad Económica','')),html.Button("Ver más...", style={'marginTop': 'auto','display':'none'})
        ],
        title="Índice de Complejidad Económica de Entidades Goegráficas",
        style={'display':'block'},
        id='accordion-ice',item_id="1"
        ),
        dbc.AccordionItem(
        [
            html.P(explicaciones_breves.get('Afinidad contra Complejidad de Producto','')),
            html.Button("Ver más...", style={'marginTop': 'auto','display':'none'})
        ],
        title="Afinidad vs. Complejidad de Productos",
        style={'display':'none'},
        id='accordion-afinidad',item_id="2"
        ),
        dbc.AccordionItem(
        [html.P(explicaciones_breves.get('Diversidad vs Ubicuidad',''))],
        title="Diversidad vs. Ubiquidad",
        style={'display':'none'},
        id='accordion-diversidad',item_id="3"
        ),
        dbc.AccordionItem(
        [ 
            
            dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Header")),
            ],
            id="modal-xl-espacio-prod",
            size="xl",
            is_open=False,
            ),
            html.P(explicaciones_breves.get('Conexión de Municipios','')),
            html.Hr(),
            html.P("Por otro lado, el Espcio de Productos es una red en la que cada nodo corresponde a un producto, y los nodos se conectan si existe una alta probabilidad de ser coproducidos")
            ,dbc.Button("Ver Espacio de Productos", id="open-xl", n_clicks=0, disabled=True, color="danger",style={"textAlign":"center","display":"block","margin":'0 auto'}),
            
        ],
        title="Espacio de Entidades",
        style={'display':'none'},
        id='accordion-espacio-prod',item_id="4"
        ),
    ],active_item=["1","2","3","4"]
    )
sidebar = html.Div(
    [
        html.H2("Visualizador geográfico"),
        html.Hr(),
        html.P("Índice de Complejidad Económica", className="lead"),
        html.Hr(),
        html.P("Unidad de medida:", className="lead", style={'fontSize': 'smaller'}),
        dcc.RadioItems(
            options=radio_items_original, value='personal', id='unidad_medida'),
        html.Hr(),
        html.P("Selecciona una edición del Directorio Estadístico Nacional de Unidades Económicas", className="lead", style={'fontSize': 'smaller'}),
        dcc.Dropdown(options=lista_de_opciones_personal, value=lista_de_opciones_personal[-1], id='opcion_denue_semestre'),
        html.Div(accordion, style={"margin-top": "auto"})  # Esto empuja el acordeón hacia abajo
    ],
    style={
        "height": "100vh",
        "display": "flex",
        "flex-direction": "column",
        "padding-left": "1vw",
        "padding-top": "2vw",
        "background-color": "#f8f9fa",
    },
)

##Dependiendo de la unidad de medida, se cambia el dropdown

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("ICE", href="#", id="nav1-link", className="nav-link active",n_clicks=0)),
        dbc.NavItem(dbc.NavLink("Afinidad", href="#", id="nav2-link", className="nav-link",n_clicks=0)),
        dbc.NavItem(dbc.NavLink("Diversidad/Ubicuidad", href="#", id="nav3-link", className="nav-link",n_clicks=0)),
        dbc.NavItem(dbc.NavLink("Espacio de Entidades", href="#", id="nav4-link", className="nav-link",n_clicks=0)),
    ],
    brand="",
    brand_href="#",
    color="primary",
    dark=True,
    style={'height':'5.5vh'},
    
)
geojson_fijo=dl.GeoJSON(
        data=map_default,
        style=style_handle,
        onEachFeature=on_each_feature,
        hideout=dict(selected=[47], classes=classes, colorscale=colorscale, style=style, colorProp="Area"),
        id="geojson",
        options=dict(interactive=False),
    )
content = html.Div(
    id="page-content",
    children=[dl.Map(id="map-container",
        center=[gdf_shapefile.geometry.centroid.y.mean(), gdf_shapefile.geometry.centroid.x.mean()],
        zoom=8,
        children=[dl.TileLayer(), 
                  geojson_fijo,info
                  ],
        style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block", 'opacity': 1,'z-index':'3'},
        className=''
    )],
    style={'width': '100%', 'height': '50vh'}
)
interior_alt_content=dcc.Graph(id='interior-alt-content',figure={},style={'height':'91.5vh', 'background-color':'lightgray'},
                                 config={'scrollZoom': True,
                                         'modeBarButtonsToRemove': ["zoom","pan","resetScale","select","lasso2d","zoomIn","zoomOut"],
                                         'modeBarButtonsToAdd': [
                                        'drawopenpath',
                                        'eraseshape'
                                       ]})
alt_content = html.Div(
    id="alt-content",
    children=interior_alt_content,
    style={'display':'none'}
)
interior_alt_content2=dcc.Graph(id='interior-alt-content2',figure={},style={'height':'71.5vh', 'background-color':'lightgray'},
                                 config={'scrollZoom': True,
                                         'modeBarButtonsToRemove': ["zoom","pan","resetScale","select","lasso2d","zoomIn","zoomOut"],
                                         'modeBarButtonsToAdd': [
                                        'drawopenpath',
                                        'eraseshape'
                                       ]})
alt_content_2 = html.Div(
    id="alt-content2",
    children=[interior_alt_content2,dcc.Graph(figure=auxiliarScatter.tabla(),style={'height':'20vh', 'background-color':'lightgray'})],
    style={'display':'none'}
)
interior_alt_content3=dcc.Graph(id='interior-alt-content3',figure={},style={'height':'91.5vh',  'background-color':'lightgray'},
                                 config={'scrollZoom': True,
                                         'modeBarButtonsToRemove': ["zoom","pan","resetScale","select","lasso2d","zoomIn","zoomOut"],
                                         'modeBarButtonsToAdd': [
                                        'drawopenpath',
                                        'eraseshape'
                                       ]})
alt_content_3 = html.Div(
    id="alt-content3",
    children=interior_alt_content3,
    style={'display':'none'}
)


layout=dbc.Container(
    [
        dbc.Row([
            dbc.Col(sidebar, width=3, style={"height": "100vh"},xs=12,sm=12,md=3,lg=3,xl=3,xxl=3),
            dbc.Col(
                [dcc.Store(id='df-industrial',data={
                                                        "data-frame": df_industrial.to_dict("records"),
                                                        "año_sel":"2024B"
                                                    }),
                    navbar,
                    dcc.Store(id='store-eleccion',modified_timestamp=-1),
                    dcc.Store(id="resize-trigger", data=False),##Este hará un window resize para solucionar el bug de leaflet
                    content,
                    
                    alt_content,
                    alt_content_2,
                    alt_content_3,
                    dcc.Store(id="store-map", data=map_default),
                    dcc.Store(id="hideout_geojson", data=dict(selected=[], classes=classes, colorscale=colorscale, style=style, colorProp="Area")),
                    dcc.Store(id='store-afinidad',data=[lista_de_opciones_unidades[-1],],modified_timestamp=-1),
                    dcc.Store(id='store-diversidad',data=[lista_de_opciones_unidades[-1],],modified_timestamp=-1),
                    dcc.Store(id='store-espacio-prod',data=[lista_de_opciones_unidades[-1],], modified_timestamp=-1),
                    dbc.Row(id='contenedor-historico',children=
                        [
                            dbc.Col(id="2-1", width=12,
                                    children=[dcc.Graph(figure=auxiliarLine.generateTimeSeries(df_estatal, [47],'personal'),style={'height':'41.5vh'},
                                                        config={'displaylogo': False})],
                                    style={'height':'41.5vh'},)
                        ],
                        className="g-0",
                        style={'height':'41.5vh'},
                    ),
                ],
                width=9,
                style={
                    "padding-top": "1.5vh",
                    "padding-bottom": "1.5vh",
                    "padding-left": "2vw",
                    "padding-right": "2vw",
                       }  # Agrega espacio a la derecha y padding interno
            ,xs=12,sm=12,md=9,lg=9,xl=9,xxl=9),
        ], className="g-0"),
    ],
    fluid=True,
    style={'height':'100vh','padding':'0'}
)