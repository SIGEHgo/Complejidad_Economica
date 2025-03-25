window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, context) {
                var searchControl = new L.Control.Search({
                    position: 'topleft',
                    layer: context.layer,
                    propertyName: 'NOM_MUN',
                    zoom: 12,
                    marker: false
                });
                context.map.addControl(searchControl);
            }

            ,
        function1: function(feature, context) {
            const {
                selected,
                classes,
                colorscale,
                colorProp
            } = context.hideout;
            const value = feature.properties[colorProp];
            var class_i = 0
            for (let i = 0; i < classes.length; ++i) {
                if (value > classes[i]) {
                    class_i = i;
                }
            }
            if (selected.includes(parseInt(feature.properties.CVEGEO) - 13000 - 1)) {
                return {
                    color: 'black',
                    fillColor: colorscale[class_i],
                    fillOpacity: 0.7,
                    weight: 5
                };
            } else {
                return {
                    color: 'white',
                    fillColor: colorscale[class_i],
                    fillOpacity: 0.7,
                    weight: 2
                };
            }
        },
        function2: function(feature, layer) {
            const defaultStyle = {
                weight: 2,
                dashArray: '3',
                fillOpacity: 0.7
            }
            if (feature.properties && feature.properties.tooltip) {
                layer.bindTooltip(feature.properties.tooltip, {
                    permanent: false,
                    direction: "auto"
                });
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
        }
    }
});