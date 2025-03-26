from dash import html
import dash_leaflet.express as dlx
from dash_extensions.javascript import assign
import auxiliarBar
classes = list(range(1, 85))
colorscale = [f"rgb({int(255 * (i / 83))}, {int(255 * (1-i / 83))}, 0)" for i in range(84)]

style = dict(weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)
ctg = ["{}+".format(cls, classes[i + 1]) for i, cls in enumerate(classes[:-1])] + ["{}+".format(classes[-1])]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft")
#Funciones propias 

info = html.Div(children=auxiliarBar.createBarplot_industrias(df_industrial="F",año_sel="T",feature=None), id="info", className="info",
                style={"position": "absolute", "top": "10px", "right": "10px", "zIndex": "10", 'width': '350px', 'height': '300px'})

# Estilo dinámico en JavaScript
search_control = assign("""
    function(feature, context){
        var searchControl = new L.Control.Search({
            position: 'topleft',
            layer: context.layer,  
            propertyName: 'NOM_MUN',
            zoom: 12,
            marker: false
        });
        context.map.addControl(searchControl);
    }
""")
style_handle = assign("""function(feature, context){
    const {selected, classes, colorscale, colorProp} = context.hideout;
    const value = feature.properties[colorProp];
    var class_i=0
    for (let i = 0; i < classes.length; ++i) {
        if (value > classes[i]) {          
            class_i = i;
        }
    }
    if (selected.includes(parseInt(feature.properties.CVEGEO)-13000-1)) {
            return {color: 'black', fillColor: colorscale[class_i], fillOpacity: 0.7, weight: 5};
    }
    else {
            return {color: 'white', fillColor: colorscale[class_i], fillOpacity: 0.7, weight: 2};
    }
}""")
on_each_feature = assign("""function(feature, layer) {
    const defaultStyle = {
        weight: 2,
        dashArray: '3',
        fillOpacity: 0.7
    }
    if (feature.properties && feature.properties.tooltip) {
        layer.bindTooltip(feature.properties.tooltip, {permanent: false, direction: "auto"});
    }
    layer.on({
        mouseover: function highlightFeature(e) {
            var layer = e.target;

            layer.setStyle({
                weight: 5,
                fillOpacity: 1,
            });
            layer.bringToFront();
        },
    });
    layer.on('mouseout', () => {
              layer.setStyle(defaultStyle); 
            });
}""")

def defStyle(nombre):
    if(nombre=='none'):
        return {'display':'none'}
    if(nombre=='map'):
        return {"display": "block", 'height': '50vh',}
    if(nombre=='nav2'):
        return {"display": "block", 'height': '91.5vh','background-color':'blue'}
    if(nombre=='block'):
        return {"display": "block"}
    return {"display": "block", 'height': '91.5vh','background-color':'red'}