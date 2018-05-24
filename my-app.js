function initPage() {
    var center = new google.maps.LatLng(35.0479, -85.2960);
    var icons = [

    ];
    var options =
        {
            zoom: 15,
            center: center
        };
    var map = new google.maps.Map(document.getElementById("map"), options);
    var request = new XMLHttpRequest();
    var markers = [];
    request.open("GET", "https://gist.githubusercontent.com/oitsjustjose/278800f898380a8212bb6b78919c0833/raw/64be83d6a5d00d57ab8595e3e61c15242b124c51/data.csv", true);
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
                    var lat = spl[i].split(",")[0];
                    var lon = spl[i].split(",")[1];
                    markers[i] = new google.maps.Marker(
                        {
                            position: new google.maps.LatLng(lat, lon),
                            icon: icons[0],
                            map: map
                        }
                    );
                }
            }
        }
    };
}
