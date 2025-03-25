import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def espacio_producto(datos_path, anio):
    datos=pd.read_csv('Datos/Complejidad Csv/Espacio Producto Hidalgo/'+'grafo_hgo_'+datos_path+'.csv')

    # Crear el grafo
    G = nx.from_pandas_edgelist(
        datos, 
        source='nodo1', 
        target='nodo2',
        edge_attr='peso_arista', 
        create_using=nx.Graph()
    )

    # DataFrame de nodos con sus pesos
    nodos1 = datos[['nodo1', 'peso_nodo1']].rename(columns={'nodo1': 'nodo', 'peso_nodo1': 'peso'})
    nodos2 = datos[['nodo2', 'peso_nodo2']].rename(columns={'nodo2': 'nodo', 'peso_nodo2': 'peso'})
    nodos = pd.concat([nodos1, nodos2])
    nodos.drop_duplicates(inplace=True)
    nodos = nodos.sort_values(by="nodo", ascending=True)

    # DataFrame de afinidad
    afinidad1 = datos[['nodo1', 'nodo1_afinidad']].rename(columns={'nodo1': 'nodo','nodo1_afinidad': 'afinidad'})
    afinidad2 = datos[['nodo2', 'nodo2_afinidad']].rename(columns={'nodo2': 'nodo','nodo2_afinidad': 'afinidad'})
    afinidad = pd.concat([afinidad1, afinidad2])
    afinidad.drop_duplicates(inplace=True)
    afinidad = afinidad.sort_values(by="afinidad", ascending=True)


    # DataFrame de nombre de la actividad
    nombre1 = datos[['nodo1', 'nodo1_nombre']].rename(columns={'nodo1': 'nodo','nodo1_nombre': 'nombre'})
    nombre2 = datos[['nodo2', 'nodo2_nombre']].rename(columns={'nodo2': 'nodo','nodo2_nombre': 'nombre'})
    nombre = pd.concat([nombre1, nombre2])
    nombre.drop_duplicates(inplace=True)
    nombre = nombre.sort_values(by="nombre", ascending=True)

    # DataFrame del nombre del sector
    sector1 = datos[['nodo1', 'nodo1_dos_digitos_nombre']].rename(columns={'nodo1': 'nodo','nodo1_dos_digitos_nombre': 'sector'})
    sector2 = datos[['nodo2', 'nodo2_dos_digitos_nombre']].rename(columns={'nodo2': 'nodo','nodo2_dos_digitos_nombre': 'sector'})
    sector = pd.concat([sector1, sector2])
    sector.drop_duplicates(inplace=True)
    sector = sector.sort_values(by="sector", ascending=True)


    def espacios(cadena):
        opciones = {
            "Agricultura, cría y explotación de animales, aprovechamiento forestal, pesca y caza": "Agricultura, cría <br> y explotación de animales, <br> aprovechamiento forestal, <br> pesca y caza",
            "Generación, transmisión, distribución y comercialización de energía eléctrica, suministro de agua y de gas natural por ductos al consumidor final": "Generación, transmisión, <br> distribución y comercialización de <br> energía eléctrica, suministro de agua <br> y de gas natural por ductos <br> al consumidor final",
            "Transportes, correos y almacenamiento": "Transportes, correos <br> y almacenamiento",
            "Información en medios masivos": "Información en <br> medios masivos",
            "Servicios financieros y de seguros": "Servicios financieros <br> y de seguros",
            "Servicios inmobiliarios y de alquiler de bienes muebles e intangibles   ": "Servicios inmobiliarios y <br> de alquiler de bienes <br> muebles e intangibles   ",
            "Servicios profesionales, científicos y técnicos":  "Servicios profesionales, <br> científicos y técnicos",
            "Dirección y administración de grupos empresariales o corporativos": "Dirección y administración <br> de grupos empresariales <br> o corporativos",
            "Servicios de apoyo a los negocios y manejo de residuos, y servicios de remediación": "Servicios de apoyo a los negocios <br> y manejo de residuos, <br> y servicios de remediación",
            "Servicios de salud y de asistencia social": "Servicios de salud y <br> de asistencia social",
            "Servicios de esparcimiento culturales y deportivos, y otros servicios recreativos": "Servicios de esparcimiento <br> culturales y deportivos, <br> y otros servicios recreativos",
            "Servicios de alojamiento temporal y de preparación de alimentos y bebidas": "Servicios de alojamiento temporal <br> y de preparación de alimentos <br> y bebidas",
            "Otros servicios excepto actividades gubernamentales": "Otros servicios excepto <br> actividades gubernamentales",
            "Actividades legislativas, gubernamentales, de impartición de justicia y de organismos internacionales y extraterritoriales": "Actividades legislativas, <br> gubernamentales, de impartición de justicia <br> y de organismos internacionales <br> y extraterritoriales"
        }
        return opciones.get(cadena.strip(), cadena)

    color = sector.copy()
    color['dos'] = color['sector'].astype(str).apply(lambda x: x[:25] + '...' if len(x) > 25 else x)


    sector['sector'] = sector['sector'].apply(lambda x: espacios(str(x)) if pd.notna(x) else x)




    # Asignar atributos a los nodos en el grafo a partir de diccionarios
    peso_dict = nodos.set_index('nodo')['peso'].to_dict()
    nx.set_node_attributes(G, peso_dict, 'peso')

    afinidad_dict = afinidad.set_index('nodo')['afinidad'].to_dict()
    nx.set_node_attributes(G, afinidad_dict, 'afinidad')

    color_dict = color.set_index('nodo')['dos'].to_dict()
    nx.set_node_attributes(G, color_dict, 'dos')

    nombre_dict = nombre.set_index('nodo')['nombre'].to_dict()
    nx.set_node_attributes(G, nombre_dict, 'nombre')

    sector_dict = sector.set_index('nodo')['sector'].to_dict()
    nx.set_node_attributes(G, sector_dict, 'sector')

    # Calcular posiciones con spring_layout
    pos = nx.spring_layout(G, seed=1)

    # Crear trazado de aristas
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, 
        y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines',
        showlegend=False
    )

    # Extraer coordenadas y propiedades de los nodos
    node_x = []
    node_y = []
    pesos_nodos = []
    colores = []        # Aquí guardamos el valor "dos"
    nombres = []
    sectores = []       # Guardaremos el valor del sector
    node_ids = []       # Guardamos el identificador del nodo
    afinidades = []     # Guardaremos el valor de afinidades

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        peso = G.nodes[node].get('peso', 0)
        pesos_nodos.append(peso)

        valor_dos = G.nodes[node].get('dos', None)
        colores.append(valor_dos)

        nombre = G.nodes[node].get('nombre', '')
        nombres.append(nombre)

        sector = G.nodes[node].get('sector', '')
        sectores.append(sector)
        
        node_ids.append(node)

        afinidad = G.nodes[node].get('afinidad', 0)
        afinidades.append(afinidad)

    # Escalar pesos para definir tamaños de nodos
    scaler = MinMaxScaler(feature_range=(10, 30))
    node_sizes = scaler.fit_transform(np.array(pesos_nodos).reshape(-1, 1)).flatten()

    # Diccionario para mapear valores a colores específicos
    color_map = {
        'Agricultura, cría y explo...': '#4CAF50', 'Minería': '#FF9800', 'Generación, transmisión, ...': '#FFEB3B', 'Construcción': '#9E9E9E', 'Industrias manufactureras': '#2196F3',
        'Industrias manufactureras': '#2196F3', 'Industrias manufactureras': '#2196F3', 'Comercio al por mayor': '#E91E63', 'Comercio al por menor': '#F06292', 'Transportes, correos y al...': '#00BCD4',
        'Transportes, correos y al...': '#00BCD4', 'Información en medios mas...': '#673AB7', 'Servicios financieros y d...': '#388E3C', 'Servicios inmobiliarios y...': '#CDDC39', 'Servicios profesionales, ...': '#FFC107',
        'Dirección y administració...': '#FF5722', 'Servicios de apoyo a los ...': '#795548', 'Servicios educativos': '#9C27B0', 'Servicios de salud y de a...': '#F44336', 'Servicios de esparcimient...': '#8E24AA',
        'Servicios de alojamiento ...': '#FFA726', 'Otros servicios excepto a...': '#607D8B', 'Actividades legislativas,...': '#424242'
    }


    ### Para hacer bien la paleta de colores interactiva

    # Lista para almacenar las trazas de nodos separadas por categoría ("dos")
    node_traces = []

    # Se obtienen todas las categorías únicas que estén en el diccionario de colores
    categorias = sorted({valor for valor in colores if valor in color_map})

    # Se recorre cada categoría
    for categoria in categorias:
        # Se obtienen los índices de los nodos que pertenecen a la categoría actual
        indices = [i for i, valor in enumerate(colores) if valor == categoria]
        # Se prepara la información personalizada para mostrar en el hover
        custom_data_trace = [[nombres[i], node_ids[i], afinidades[i], pesos_nodos[i], sectores[i]] for i in indices]
        
        # Se crea la traza de la categoría usando go.Scatter
        trace = go.Scatter(
            x=[node_x[i] for i in indices],
            y=[node_y[i] for i in indices],
            mode='markers',
            hoverinfo='none',
            customdata=custom_data_trace,
            marker=dict(
                size=[node_sizes[i] for i in indices],
                color=color_map.get(categoria, 'black'),
                line_width=2
            ),
            # Parámetros importantes para la interactividad:
            legendgroup=str(categoria),  # Agrupa esta traza con su categoría
            name=str(categoria)          # Nombre que aparecerá en la leyenda
        )
        # Se agrega la traza a la lista
        node_traces.append(trace)


    # Crear la figura y agregar las trazas
    fig = go.Figure(
        data=[edge_trace] + node_traces,
        layout=go.Layout(
            title={
                "text": "Espacio Producto en Hidalgo <br><span style='font-size:14px;'> (" + anio + ") </span>",
                "x": 0.5,
                "xanchor": "center"
            },
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )

    fig.update_traces(
        hovertemplate=
            "<b>Actividad:</b> %{customdata[0]}<br>" +
            "<b>Código:</b> %{customdata[1]}<br>" +
            "<b>Afinidad:</b> %{customdata[2]:.2f}<br>" +
            "<b>Personal:</b> %{customdata[3]}<br>" +
            "<extra>%{customdata[4]}</extra>",
        marker=dict(showscale=False),
        selector=dict(mode='markers')
    )

    fig.update_layout(
        legend_title=dict(text="Sector")
    )

    fig.update_layout(
        autosize=True,
        width=None,
        height=None
        )
    return(fig)


def espacio_hidalgo_red(datos_path, anio):
    datos=pd.read_csv('Datos/Complejidad Csv/Red Hidalgo por Municipio/'+'Red_Hidalgo_'+datos_path+'.csv')
    G = nx.from_pandas_edgelist(
        datos, 
        source='nodo1_nombre', 
        target='nodo2_nombre', 
        edge_attr='peso_arista', 
        create_using=nx.Graph()
    )

    # DataFrame de nodos con sus pesos
    nodos1 = datos[['nodo1_nombre', 'peso_nodo1']].rename(columns={'nodo1_nombre': 'nodo', 'peso_nodo1': 'peso'})
    nodos2 = datos[['nodo2_nombre', 'peso_nodo2']].rename(columns={'nodo2_nombre': 'nodo', 'peso_nodo2': 'peso'})
    nodos = pd.concat([nodos1, nodos2])
    nodos.drop_duplicates(inplace=True)
    nodos.sort_values(by="nodo", ascending=True, inplace=True)

    # DataFrame de etiquetas
    datos['nodo1_abr'] = datos['nodo1'].apply(lambda x: f"{x:03d}")
    datos['nodo2_abr'] = datos['nodo2'].apply(lambda x: f"{x:03d}")
    etiquetas1 = datos[['nodo1_nombre', 'nodo1_abr']].rename(columns={'nodo1_nombre': 'nodo', 'nodo1_abr': 'etiquetas'})
    etiquetas2 = datos[['nodo2_nombre', 'nodo2_abr']].rename(columns={'nodo2_nombre': 'nodo', 'nodo2_abr': 'etiquetas'})
    etiqueta = pd.concat([etiquetas1, etiquetas2])
    etiqueta.drop_duplicates(inplace=True)
    etiqueta.sort_values(by="etiquetas", ascending=True, inplace=True)

    # DataFrame de color
    color1 = datos[['nodo1_nombre', 'nodo1_region']].rename(columns={'nodo1_nombre': 'nodo', 'nodo1_region': 'region'})
    color2 = datos[['nodo2_nombre', 'nodo2_region']].rename(columns={'nodo2_nombre': 'nodo', 'nodo2_region': 'region'})
    color = pd.concat([color1, color2])
    color.drop_duplicates(inplace=True)
    color.sort_values(by="nodo", ascending=True, inplace=True)

    # Asignar atributos a los nodos en el grafo
    peso_dict = nodos.set_index('nodo')['peso'].to_dict()
    nx.set_node_attributes(G, peso_dict, 'peso')

    etiqueta_dict = etiqueta.set_index('nodo')['etiquetas'].to_dict()
    nx.set_node_attributes(G, etiqueta_dict, 'etiquetas')

    color_dict = color.set_index('nodo')['region'].to_dict()
    nx.set_node_attributes(G, color_dict, 'region')

    # Posición de los nodos
    pos = nx.spring_layout(G, seed=1)

    # Crear trazado de aristas
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y, 
        line=dict(width=0.5, color='#888'), 
        hoverinfo='none', 
        mode='lines', 
        showlegend=False
    )

    # Extraer coordenadas y propiedades de los nodos
    node_x, node_y = [], []
    pesos_nodos, etiquetas, colores = [], [], []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        pesos_nodos.append(G.nodes[node].get('peso', 0))
        etiquetas.append(G.nodes[node].get('etiquetas', ''))
        colores.append(G.nodes[node].get('region', ''))

    # Escalar los pesos para definir tamaños visibles
    scaler = MinMaxScaler(feature_range=(10, 30))
    node_sizes = scaler.fit_transform(np.array(pesos_nodos).reshape(-1, 1)).flatten()

    # Diccionario para mapear valores a colores
    color_map = {
        "Región Actopan": "blue",
        "Región Apan": "orange",
        "Región Huejutla": "green",
        "Región Huichapan": "red",
        "Región Ixmiquilpan": "purple",
        "Región Jacala": "brown",
        "Región Mineral de la Reforma": "pink",
        "Región Pachuca": "gray",
        "Región Tizayuca": "olive",
        "Región Tula": "cyan",
        "Región Tulancingo": "crimson",
        "Región Zacualtipán": "black"
    }

    # Crear trazas de nodos separadas por categoría
    node_traces = []
    categorias = sorted({valor for valor in colores if valor in color_map})
    nombres = list(G.nodes)

    for categoria in categorias:
        indices = [i for i, valor in enumerate(colores) if valor == categoria]
        custom_data_trace = [[nombres[i], pesos_nodos[i], colores[i]] for i in indices]
        
        trace = go.Scatter(
            x=[node_x[i] for i in indices],
            y=[node_y[i] for i in indices],
            mode='markers+text',  # Incluye los labels y los markers
            customdata=custom_data_trace,
            text=[etiquetas[i] for i in indices],
            textposition='bottom center',
            marker=dict(
                size=[node_sizes[i] for i in indices],
                color=color_map.get(categoria, 'black'),
                line_width=2
            ),
            legendgroup=str(categoria),
            name=str(categoria)
        )
        node_traces.append(trace)

    # Crear la figura
    fig = go.Figure(
        data=[edge_trace] + node_traces,
        layout=go.Layout(
            title={
                "text": "Espacio de Entidades en Hidalgo <br><span style='font-size:14px;'> (" + anio + " ) </span>",
                "x": 0.5,
                "xanchor": "center"
            },
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )

    # Actualizar todas las trazas (sin selector) para aplicar el hovertemplate
    fig.update_traces(
        hovertemplate=
            "<b>Municipio:</b> %{customdata[0]}<br>" +
            "<b>Número de empleados:</b> %{customdata[1]}<br>" +
            "<extra>%{customdata[2]}</extra>",
        marker=dict(showscale=False)
    )

    fig.update_layout(
        legend_title=dict(text="Región:")
    )
    fig.update_layout(
        autosize=True,
        width=None,
        height=None,
        dragmode='pan'
    )
    return(fig)
