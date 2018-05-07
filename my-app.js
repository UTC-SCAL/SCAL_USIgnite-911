function initPage() {
    var center = new google.maps.LatLng(35.0479, -85.2960);
    var options =
        {
            zoom: 10,
            center: center
        };
    var map = new google.maps.Map(document.getElementById("map"), options);
    var request = new XMLHttpRequest();
    var markers = [];
    var info_windows = [];
    request.open("GET", "https://raw.githubusercontent.com/oitsjustjose/SCAL_USIgnite-911/gh-pages/pos.txt", true);
    request.send(null);
    request.onreadystatechange = function () {
        if (request.readyState === 4 && request.status === 200) {
            var type = request.getResponseHeader('Content-Type');
            if (type.indexOf("text") !== 1) {
                var spl = request.responseText.split("\n");
                for (var i in spl) {
                    // Ignore lines that are empty:
                    if (spl[i].indexOf(",") === -1) {
                        continue;
                    }
                    var lat = spl[i].split(", ")[0];
                    var lon = spl[i].split(", ")[1];
                    markers[i] = new google.maps.Marker(
                        {
                            position: new google.maps.LatLng(lat, lon),
                            animation: google.maps.Animation.DROP,
                            map: map,
                            label: lat + ", " + lon
                        }
                    );
                    info_windows[i] = new google.maps.InfoWindow();
                    google.maps.event.addListener(markers[i], 'click', (function (marker, content, infowindow) {
                        return function () {
                            infowindow.setContent(content);
                            infowindow.open(map, marker);
                        };
                    })(markers[i], "<p>" + spl[i].split(", ")[2] + "</p>", info_windows[i]));

                    // markers[i].addListener('click', function () {
                    //     info_windows[i].open(map, markers[i]);
                    // });
                }
            }
        }
    };
}
