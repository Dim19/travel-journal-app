document.addEventListener("DOMContentLoaded", function() {
    // Initialize the map centered at latitude 20, longitude 0 with zoom level 2
    var map = L.map('map').setView([20, 0], 2);

    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Define color mapping for travel statuses
    function getColor(status) {
        switch(status) {
            case 'Visited': return '#28a745';
            case 'Planned': return '#ffc107';
            case 'Wishlist': return '#6c757d';
            default: return '#007bff';
        }
    }

    // Load GeoJSON data for world countries
    fetch('/static/data/world_countries.json')
        .then(response => response.json())
        .then(geojsonData => {
            L.geoJson(geojsonData, {
                style: function(feature) {
                    var countryName = feature.properties.name;
                    var status = countryData[countryName] ? countryData[countryName].travel_status : "Wishlist";
                    return {
                        fillColor: getColor(status),
                        weight: 1,
                        opacity: 1,
                        color: 'white',
                        fillOpacity: 0.7
                    };
                },
                onEachFeature: function(feature, layer) {
                    var countryName = feature.properties.name;
                    if (countryData[countryName]) {
                        layer.bindPopup('<a href="/country/' + countryData[countryName].id + '">' + countryName + '</a>');
                    } else {
                        layer.bindPopup(countryName);
                    }
                }
            }).addTo(map);
        })
        .catch(err => console.error("Error loading GeoJSON data: ", err));
});