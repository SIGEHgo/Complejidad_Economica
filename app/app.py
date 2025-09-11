import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, no_update
import dash_leaflet as dl
import json
from flask import Flask

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
print(df_industrial)
server = Flask(__name__)

app = dash.Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, 'app/assets/customICE.css'])
app.title = 'ICE'
####Lista de ids
#unidad_medida
#opcion_denue_semestre
#nav1-link
#nav2-link
#geojson
#store-map
#store-hist
#hideout_geojson
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
            html.P(explicaciones_breves.get('Complejidad Económica',''))
        ],
        title="Índice de Complejidad Económica de Entidades Goegráficas",
        style={'display':'block'},
        id='accordion-ice',item_id="1"
        ),
        dbc.AccordionItem(
        [
            html.P(explicaciones_breves.get('Afinidad contra Complejidad de Producto',''))
           
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
            html.P(explicaciones_breves.get('Conexión de Municipios',''))
            ,dbc.Button("Ver Espacio de Productos", id="open-xl", n_clicks=0, disabled=True, color="danger"),
            
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
    ),
    html.Div(
        children=[
            html.Img(
                src="./assets/Planeacion_SEDECO_Transparente.png",  
                style={
                    "height": "4vh",  # Tamaño del ícono
                }
            )
        ],
        style={ # Estilos CSS aplicados al Div
            "position": "absolute", # El elemento no ocupa espacio en el diseño habitual. Esto significa que otros elementos actúan como si el elemento "absoluto" no existiera.
            "bottom": "44vh",   # Posicionamiento desde el borde inferior
            "left": "5wh",     # Posicionamiento desde el borde izquierdo
            "z-index": "1000"   # Asegura que esté sobre otros elementos
        }
    )
    ],
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

app.layout = dbc.Container(
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
                                    children=[dcc.Graph(figure=auxiliarLine.generateTimeSeries(df_estatal, [47],'personal', corte=len(lista_de_opciones_unidades) + 1, maximo = 2*len(lista_de_opciones_unidades) + 1),style={'height':'41.5vh'},
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

                ####################  Puras Callbacks  ####################
#####################         Dropdown
#Esta es la más sencilla. Actualiza las opciones dependiendo de la elección de medida
#Consume el estado de la elección del año para conservarla
@app.callback([Output('opcion_denue_semestre','options'),Output('opcion_denue_semestre','value')],
              Input('unidad_medida','value'),State('opcion_denue_semestre','value'),prevent_initial_call=True)
def Dropdown_list(unidad_medida,eleccion):
    print("Se actualiza la unidad de medida: "+unidad_medida+' '+eleccion)
    if(unidad_medida=='personal'):
        return lista_de_opciones_personal,lista_de_opciones_personal[lista_de_opciones_unidades.index(eleccion)]
    else:
        return lista_de_opciones_unidades,lista_de_opciones_unidades[lista_de_opciones_personal.index(eleccion)]


####################        NAV
##Este es el que cambia el contenido dependiendo del click sobre el nav
#Recibe click sobre el navbar 
#Dependiendo del click, oculta lo necesario. 
@app.callback(
    [
        Output("page-content", "style"),
        Output("alt-content", "style"),
        Output("alt-content2", "style"),
        Output("alt-content3", "style"),
        Output("2-1", "style"),
        Output("contenedor-historico", "style"),
        Output("nav1-link", 'className'),
        Output("nav2-link", 'className'),
        Output("nav3-link", 'className'),
        Output("nav4-link", 'className'),
        Output("unidad_medida",'value'),
        Output("unidad_medida","options"),
        Output("accordion-ice","style"),
        Output("accordion-afinidad","style"),
        Output("accordion-diversidad","style"),
        Output("accordion-espacio-prod","style"),
    ],
    [
        Input("nav1-link", "n_clicks"),
        Input("nav2-link", "n_clicks"),
        Input("nav3-link", "n_clicks"),
        Input("nav4-link", "n_clicks"),
        State("unidad_medida",'value'),
        State("nav1-link", "className"),
        State("nav2-link", "className"),
        State("nav3-link", "className"),
        State("nav4-link", "className"),
    ],
    prevent_initial_call=True,
)
def render_content(nav_1_click, nav_2_click,nav_3_click_nav,nav_4_click_nav,unidad_medida,n1a,n2a,n3a,n4a):##Se puede mejorar. Se actualizan innecesariamente las classNames cuando se da click en un nav ya activo
    nav_clicked=re.search(r'\d+', dash.callback_context.triggered[0]['prop_id']).group()
    nav_actived=[n1a,n2a,n3a,n4a]##En tiempo pasado
    if("active" in nav_actived[int(nav_clicked)-1]):##Así evito una re-carga al dar click redundante
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update,no_update,no_update,no_update,no_update
    vacio=defStyle('none')
    block=defStyle('block')
    if 'nav1-link.n_clicks' in dash.callback_context.triggered[0]['prop_id']:
        #Nav 2 activo
        no_vacio=defStyle('map')
        if(unidad_medida!='personal'):
            return no_vacio, vacio,vacio,vacio,block,block, 'nav-link active', 'nav-link', 'nav-link','nav-link','personal',radio_items_original,block,vacio,vacio,vacio,
        else:
            return no_vacio, vacio,vacio,vacio,block,block, 'nav-link active', 'nav-link', 'nav-link','nav-link',no_update,radio_items_original,block,vacio,vacio,vacio,

    if 'nav2-link.n_clicks' in dash.callback_context.triggered[0]['prop_id']:
        #Nav 2 activo
        no_vacio=defStyle('nav2')
        if(unidad_medida!='personal'):
            return vacio, no_vacio, vacio, vacio, vacio, vacio, 'nav-link', 'nav-link active', 'nav-link', 'nav-link', 'personal', radio_items_personal,vacio,block,vacio,vacio
        else:
            return vacio, no_vacio, vacio, vacio, vacio, vacio, 'nav-link', 'nav-link active', 'nav-link', 'nav-link', no_update, radio_items_personal,vacio,block,vacio,vacio

    if 'nav3-link.n_clicks' in dash.callback_context.triggered[0]['prop_id']:
        #Nav 2 activo
        no_vacio=defStyle('nav3')
        if(unidad_medida!='personal'):
            return vacio, vacio,no_vacio,vacio,vacio,vacio, 'nav-link', 'nav-link', 'nav-link active','nav-link','personal',radio_items_personal,vacio,vacio,block,vacio,
        else:
            return vacio, vacio,no_vacio,vacio,vacio,vacio, 'nav-link', 'nav-link', 'nav-link active','nav-link',no_update,radio_items_personal,vacio,vacio,block,vacio,

    
    if 'nav4-link.n_clicks' in dash.callback_context.triggered[0]['prop_id']:
        #Nav 2 activo
        no_vacio=defStyle('nav2')
        if(unidad_medida!='personal'):
            return vacio, vacio,vacio,no_vacio,vacio,vacio, 'nav-link', 'nav-link', 'nav-link','nav-link active','personal',radio_items_personal,vacio,vacio,vacio,block
        else:
            return vacio, vacio,vacio,no_vacio,vacio,vacio, 'nav-link', 'nav-link', 'nav-link','nav-link active',no_update,radio_items_personal,vacio,vacio,vacio,block








##Este es el que se actualiza el contenido dependiendo de la eleccion del año. 
#Recibe la eleccion del año, el estado de los navs, y el hideout del geojson fijo
#Actualiza el geojson fijo (solo su data porque ahí trae Area que es el color)
#Además, revisa el estado de las navs y dependiendo de la activa, actualiza su respectiva visualización
@app.callback(
    [
        Output("geojson", "data", allow_duplicate=True),#Actualizaria el mapa geojson
        Output("interior-alt-content",'figure'),
        Output("interior-alt-content2",'figure'),
        Output("interior-alt-content3",'figure'),
        Output("store-afinidad",'data'),
        Output("store-diversidad",'data'),
        Output("store-espacio-prod",'data'),
        Output("open-xl",'color',allow_duplicate=True),
        Output("open-xl",'disabled',allow_duplicate=True),
        Output("df-industrial",'data')
    ],
    [
        Input('opcion_denue_semestre', 'value'),
        Input('nav1-link', 'className'),#Pasa de State a Input para  que cuando se haga un cambio de className desde otro callback, se active este
        Input('nav2-link', 'className'),
        Input('nav3-link', 'className'),
        Input('nav4-link', 'className'),
        State("store-afinidad",'data'),##Para revisar los años ultimos rendereados
        State("store-diversidad",'data'),
        State("store-espacio-prod",'data'),
    ],
    prevent_initial_call=True
)
def update_map_nav1(eleccion_año, nav1_class, nav2_class,nav3_class,nav4_class,afinidad_año,diversidad_año,espacio_prod_año):
    print("Cambio el className de los nav")
    #Vamos a renderear el contenido necesario.
    print(dash.callback_context.triggered[0]['prop_id'])
    if("opcion_denue_semestre" in dash.callback_context.triggered[0]['prop_id']):#Se activó por un cambio de año
        color_nuevo='danger'
        disabled_state=True
        if("2015" not in eleccion_año):
            year, semester = eleccion_año[-7:].split('-')
            formatted_year=(year+'B') if semester=='II' else year[1:]+'A' 
            nuevo_df_industrial={
                                    "data-frame": pd.read_csv("Datos/CSVs/Balassa_Modificado_Historico/Balassa_Mod_Nivel_Municipio_por_Grupos_"+formatted_year+".csv").to_dict("records"),
                                    "año_sel":formatted_year
                                }

        else:#2015
            nuevo_df_industrial={
                                    "data-frame": pd.read_csv("Datos/CSVs/Balassa_Modificado_Historico/Balassa_Mod_Nivel_Municipio_por_Grupos_"+'2015'+".csv").to_dict("records"),
                                    "año_sel":"2015"
                                }
    else:
        color_nuevo=no_update
        disabled_state=no_update
        nuevo_df_industrial=no_update

    if 'active' in nav1_class:#Si estamos en el nav 1 es porque cambió el nav (hacia nav1) o porquee estabamos en el nav1 y cambio el año
        map_default = auxiliarLeafltet.generateMapFromElection(eleccion_año, df_estatal, gdf_shapefile)
        return map_default, no_update, no_update,no_update       ,no_update,no_update,no_update,     color_nuevo,disabled_state, nuevo_df_industrial
    elif 'active' in nav2_class:#afinidad
        ##Aqui revisamos el año guardado en data. 
        if(afinidad_año[0]==eleccion_año):#no le muevas
            return no_update, no_update, no_update,no_update,      no_update,no_update,no_update,     color_nuevo,disabled_state, nuevo_df_industrial
        # Extract the year and semester from eleccion_año
        print("Entonces sí se actualiza")
        if("2015" not in eleccion_año):
            year, semester = eleccion_año[-7:].split('-')
            formatted_year=(year+'B') if semester=='II' else year[1:]+'A' 
            afinidad=auxiliarScatter.afinidad('6',formatted_year)
        else:#2015
            afinidad=auxiliarScatter.afinidad('6',"2015")
        return no_update, afinidad, no_update,no_update,       [eleccion_año],no_update,no_update,      color_nuevo,disabled_state, nuevo_df_industrial
    elif 'active' in nav3_class:
        if(diversidad_año[0]==eleccion_año):#no le muevas
            return no_update, no_update, no_update,no_update,           no_update,no_update,no_update,      color_nuevo,disabled_state, nuevo_df_industrial
        print("Entonces sí se actualiza")
        if("2015" not in eleccion_año):
            year, semester = eleccion_año[-7:].split('-')
            formatted_year=(year+'B') if semester=='II' else year[1:]+'A' 
            diversidad=auxiliarScatter.diversidad_municipal('6',formatted_year)
        else:#2015
            #diversidad=auxiliarNetwork.espacio_hidalgo_red(formatted_year,formatted_year)
            diversidad=auxiliarScatter.diversidad_municipal("6","2015")
        return no_update, no_update,diversidad,no_update,       no_update,[eleccion_año],no_update      ,color_nuevo,disabled_state, nuevo_df_industrial
    elif 'active' in nav4_class:
        if(espacio_prod_año[0]==eleccion_año):#no le muevas
            return no_update, no_update, no_update,no_update,         no_update,no_update,no_update      ,color_nuevo,disabled_state, nuevo_df_industrial
        print("Entonces sí se actualiza")
        if("2015" not in eleccion_año):
            year, semester = eleccion_año[-7:].split('-')
            formatted_year=(year+'B') if semester=='II' else year[1:]+'A' 
            #diversidad=auxiliarScatter.diversidad_municipal('4',formatted_year)
            #diversidad=auxiliarNetwork.espacio_hidalgo_red(formatted_year,formatted_year)
            espacio_fast=auxiliarNetwork.espacio_hidalgo_red(formatted_year,formatted_year)
        else:#2015
            #diversidad=auxiliarNetwork.espacio_hidalgo_red(formatted_year,formatted_year)
            espacio_fast=auxiliarNetwork.espacio_hidalgo_red("2015","2015")
        return no_update, no_update,no_update,espacio_fast,          no_update,no_update,[eleccion_año]      ,color_nuevo,disabled_state, nuevo_df_industrial


##Este es el que permite selecionar poligonos
#Modifica el geojson fijo
@app.callback(
    [Output("geojson", "hideout"), Output('hideout_geojson', 'data')],
    Input("geojson", "n_clicks"),
    State("geojson", "clickData"),
    State("hideout_geojson", "data"),
    prevent_initial_call=True)
def toggle_select(_, feature, hideout):
    if _ >0:
        selected = hideout["selected"]
        name = int(feature["properties"]["CVEGEO"]) - 13000 - 1
        if name in selected:
            selected.remove(name)
        else:
            selected.append(name)
        hideout["selected"] = selected
        return hideout, hideout
    else:
        return hideout, hideout

##Este es el que actualiza el time series
#Recibe el hideout del geojson fijo y la unidad de medida
#Actualiza el time series
@app.callback(
    Output("2-1", "children"),
    [Input("geojson", "hideout"),Input("unidad_medida","value")],
    prevent_initial_call=True
)
def timeSeriesGivenFeature(hideout,unidad_medida):
    selected = hideout["selected"]
    return dcc.Graph(figure=auxiliarLine.generateTimeSeries(df_estatal, selected,unidad_medida, corte=len(lista_de_opciones_unidades) + 1, maximo = 2*len(lista_de_opciones_unidades) + 1),style={'height':'41.5vh'},config={'displaylogo': False})  # You can format properties as needed




###Actualiza el barplot horizontal de industrias top5. 
#Recibe algún click sobre el mapa o su contenedor, Revisa los estados de los clicks sobre algún feature
#Actualiza la gráfica de top5 y los estilos necesarios. Reinicia los clicks si no se selecciona un feature
@app.callback(
    [Output("info", "children"), Output("info", "style"),Output("geojson",'n_clicks'),Output("map-container",'n_clicks')],
    [Input("map-container",'n_clicks'),
    State('geojson','n_clicks'),State("geojson",'clickData'),State("info", "style"),State("df-industrial",'data')],
    prevent_initial_call=True)
def update_info_and_style(n_click_container,click_map,feature, style,df_industrial):
    print("------------------------------------------------------------")
    print(pd.DataFrame(df_industrial["data-frame"]))
    print("numero de clicks en container: "+str(n_click_container))
    print("numero de clicks en geojson: "+str(click_map))
    if(n_click_container== click_map):##Fue un click afuera
        children = auxiliarBar.createBarplot_industrias( pd.DataFrame(df_industrial["data-frame"]),df_industrial['año_sel'],feature)
        style = {"position": "absolute", "top": "10px", "right": "10px", "zIndex": "1000", 'width': '350px', 'height': '400px'}
        return children, style,click_map,n_click_container
    else:
        children = []
        style = {"display": "none"}
    return children, style,0,0





###Carga en segundo plano el contenido de un modal que contiene la red de productos
#Recibe la actualización de un store. Es decir, cada que se actualice un año y se genere una nueva network de municipios
#Actualiza hijos y cambia el color de boton para cuando esté listo.
@app.callback(Output("modal-xl-espacio-prod",'children'),Output("open-xl",'color'),Output("open-xl",'disabled'),
              Input("store-espacio-prod",'data'))
def generarBigNetwork(stored_data):
    eleccion_año=stored_data[0]
    if("2015" not in eleccion_año):
            year, semester = eleccion_año[-7:].split('-')
            formatted_year=(year+'B') if semester=='II' else year[1:]+'A' 

            espacio_slow=auxiliarNetwork.espacio_producto(formatted_year,formatted_year)
    else:#2015
        espacio_slow=auxiliarNetwork.espacio_producto("2015","2015")
    return [html.P(explicaciones_breves.get('Espacio Producto','')),dcc.Graph(figure=espacio_slow,config={'scrollZoom': True,
                                         'modeBarButtonsToRemove': ["zoom","pan","resetScale","select","lasso2d","zoomIn","zoomOut"],
                                         'modeBarButtonsToAdd': [
                                        'drawopenpath',
                                        'eraseshape'
                                       ]})],'success',False


@app.callback(
    Output("modal-xl-espacio-prod", "is_open"),
    Input("open-xl", "n_clicks"),
    State("modal-xl-espacio-prod", "is_open"),
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open

if __name__ == "__main__":
    app.run()
