import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import assign

def generateMapFromElection(election, df_estatal, gdf_shapefile):
    # Asignar valores a la columna 'Area'
    gdf_shapefile["Valor-actual"] = df_estatal[election].round(2)
    gdf_shapefile['Area'] = gdf_shapefile['Valor-actual'].rank(ascending=False)
    # Crear la estructura GeoJSON con tooltips
    #print(gdf_shapefile.Area)
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": feature["geometry"],
                "properties": {
                    **feature["properties"],
                    "Area": gdf_shapefile.loc[idx, "Area"],
                    "tooltip": f"Entidad: {feature['properties'].get('NOM_MUN','N/A')} <br> Valor: {gdf_shapefile.loc[idx, 'Valor-actual']} <br> Ranking: {gdf_shapefile.loc[idx, 'Area']}"
                }
            }
            for idx, feature in enumerate(gdf_shapefile.__geo_interface__["features"])
        ]
    }

    # Crear GeoJSON con tooltip

    # Devolver el mapa con el GeoJSON actualizado
    return geojson_data