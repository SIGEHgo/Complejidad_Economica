import plotly.express as px
import plotly.graph_objects as go

def tabla():
    df = pd.read_csv("Datos/Complejidad Csv/Diversidad y ubicuidad promedio de las clases de actividad economica/Hidalgo/dive_vs_ubi_2_mun.csv")
    df['CVE_MUN'] = df['CVE_MUN'].apply(lambda x: f"{x:03d}")
    # Crear la tabla con desplazamiento
    table = go.Figure(data=[go.Table(
        header=dict(values=["CVE MUN", "Municipio"],
                    fill_color='lightgray',
                    align='left'),
        cells=dict(values=[df["CVE_MUN"], df["Municipio"]],
                fill_color='white',
                align='left')),
    ])

    # Ajustar tamaño y agregar desplazamiento
    table.update_layout(
        title="Claves de municipios",
        height=400,  # Ajustar tamaño de la tabla
        width=350,
        margin=dict(t=30, b=10)  # Reducir el padding superior e inferior
    )
    table.update_layout(
        autosize=True,
        width=None,
        height=None
    )
    return(table)


import plotly.express as px
import pandas as pd

def afinidad(df_path, anio):
    print("Generamos afinidad")
    df = pd.read_csv("Datos/Complejidad Csv/Afinidad y complejidad por producto/afinidad_"+df_path+"_nombres.csv")

    d = df.copy()  # Para evitar modificar el DataFrame original

    afinidad_anio = f"afinidad_{anio}"
    #print(afinidad_anio)
    complejidad_producto_anio = f"complejidad_producto_{anio}"
    #print(complejidad_producto_anio)

    personal_ocupado_anio = f"personal_ocupado_{anio}"

  
    d = d.dropna(subset=[afinidad_anio, complejidad_producto_anio, personal_ocupado_anio])
    d[personal_ocupado_anio]=d[personal_ocupado_anio]
    #print(d[personal_ocupado_anio])
    # Colores
    d['Titulo_corto'] = d['Título_dos_digitos'].astype(str).apply(lambda x: x[:25] + '...' if len(x) > 25 else x)
    
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
    d['Título_dos_digitos'] = d['Título_dos_digitos'].apply(lambda x: espacios(str(x)) if pd.notna(x) else x)

    fig = px.scatter(
        d,
        x= afinidad_anio,
        y= complejidad_producto_anio,
        size= personal_ocupado_anio,
        color='Titulo_corto',
        custom_data=['Título', 'codigo_act', 'Título_dos_digitos'],
        color_continuous_scale=px.colors.sequential.Viridis,  # Paleta de colores,
    )

    fig.update_layout(
        title={
            "text": "Afinidad y complejidad por producto <br><span style='font-size:14px;'> (" + anio + ") </span>",
            "x": 0.5,  # Centrar el título
            "xanchor": "center"
        },
        xaxis_title="Afinidad",
        yaxis_title="Complejidad del Producto",
        coloraxis_showscale=False,       # Ocultar escala de colores
        #paper_bgcolor='rgba(0,0,0,0)',  # Fondo general transparente
        plot_bgcolor='rgba(0,0,0,0)',    # Fondo del área de trazado transparente
        xaxis=dict(
            showgrid=True,              # Mostrar líneas de la cuadrícula en X
            gridcolor='lightgray',      # Color de las líneas de la cuadrícula
            gridwidth=0.3,              # Grosor de las líneas de la cuadrícula
            zeroline=True,              # Mostrar línea del eje en X=0
            zerolinecolor='lightgray',  # Color de la línea del eje
            zerolinewidth=1             # Grosor de la línea del eje
        ),
        yaxis=dict(
            showgrid=True,              # Mostrar líneas de la cuadrícula en Y
            gridcolor='lightgray',
            gridwidth=0.3,
            zeroline=True,              # Mostrar línea del eje en Y=0
            zerolinecolor='lightgray',
            zerolinewidth=1
        )
    )
    

    # Actualizar los trazos (traces) para personalizar el hover y los marcadores
    fig.update_traces(
        hovertemplate=
        "<b>Actividad:</b> %{customdata[0]}<br>" +
        "<b>Código:</b> %{customdata[1]}<br>" +
        "<b>Afinidad:</b> %{x:.2f}<br>" +
        "<b>Complejidad:</b> %{y:.2f}<br>" +
        "<b>Personal:</b> %{marker.size:.0f}<br>" +
        "<extra>%{customdata[2]}</extra>",
        marker=dict(showscale=False)  # Desactiva la escala de colores
    )

    fig.update_layout(
        legend_title_text='Sector'
    )
    fig.update_layout(
        autosize=True,
        width=None,
        height=None,
        dragmode='pan'
        )

    return(fig)
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def diversidad_municipal(df_path, anio):
    df = pd.read_csv("Datos/Complejidad Csv/Diversidad y ubicuidad promedio de las clases de actividad economica/Hidalgo/dive_vs_ubi_"+df_path+'_mun.csv')
    diversidad_anio = f"diversidad_{anio}"
    especializado_anio = f"especializado_{anio}"
    df['CVE_MUN'] = df['CVE_MUN'].apply(lambda x: f"{x:03d}")

    # Crear la figura de dispersión e incluir 'estado' como texto en cada punto
    fig = px.scatter(
        df,
        x= diversidad_anio,
        y= especializado_anio,
        text='CVE_MUN',
        color="Región",
        symbol="Región",
        custom_data=['Municipio'],
        category_orders={
        "Región": [
            "Región Actopan",
            "Región Apan",
            "Región Huejutla",
            "Región Huichapan",
            "Región Ixmiquilpan",
            "Región Jacala",
            "Región Mineral de la Reforma",
            "Región Pachuca",
            "Región Tizayuca",
            "Región Tula",
            "Región Tulancingo",
            "Región Zacualtipán"
        ]
        },
        color_discrete_map={
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

    )

    # Agregar líneas de referencia en la mediana
    fig.add_vline(x=df[diversidad_anio].mean(), line_color='red', line_dash='dash')
    fig.add_hline(y=df[especializado_anio].mean(), line_color='red', line_dash='dash')

    # Actualizar la posición del texto para que se muestre debajo de cada punto
    fig.update_traces(textposition='bottom center')



    fig.update_layout(
        title={
            "text": "Diversidad y ubicuidad promedio de las clases de actividad economica <br><span style='font-size:14px;'> (" + anio + ") </span>",
            "x": 0.5,  # Centrar el título
            "xanchor": "center"
        },
        xaxis_title="Diversidad por municipio",
        yaxis_title="Ubicuidad promedio",
        coloraxis_showscale=False,       # Ocultar escala de colores
        #paper_bgcolor='rgba(0,0,0,0)',  # Fondo general transparente
        plot_bgcolor='rgba(0,0,0,0)',    # Fondo del área de trazado transparente
        xaxis=dict(
            showgrid=True,              # Mostrar líneas de la cuadrícula en X
            gridcolor='lightgray',      # Color de las líneas de la cuadrícula
            gridwidth=0.3,              # Grosor de las líneas de la cuadrícula
            zeroline=True,              # Mostrar línea del eje en X=0
            zerolinecolor='lightgray',  # Color de la línea del eje
            zerolinewidth=1             # Grosor de la línea del eje
        ),
        yaxis=dict(
            showgrid=True,              # Mostrar líneas de la cuadrícula en Y
            gridcolor='lightgray',
            gridwidth=0.3,
            zeroline=True,              # Mostrar línea del eje en Y=0
            zerolinecolor='lightgray',
            zerolinewidth=1
        )
    )

    # Personalizar el hover si es necesario
    fig.update_traces(
        hovertemplate=
        "<b>Municipio:</b> %{customdata[0]}<br>" +
        "<b>Ubicuidad Promedio:</b> %{y:.2f}<br>" +
        "<b>Diversidad:</b> %{x:.0f}<br>"
    )
    fig.update_layout(
        autosize=True,
        width=None,
        height=None,
        dragmode='pan'
        )

    # Figura
    return(fig)