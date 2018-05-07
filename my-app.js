function initPage() {
    var center = new google.maps.LatLng(35.0479, -85.2960);
    var options =
        {
            zoom: 20,
            center: center
        };
    var map = new google.maps.Map(document.getElementById("map"), options);
    var request = new XMLHttpRequest();
    request.open("GET", "https://raw.githubusercontent.com/oitsjustjose/SCAL_USIgnite-911/gh-pages/pos.txt?token=ADtQ3Iw-5GZqC6zu0G6gpmiLc0OlFt6Mks5a-ZnKwA%3D%3D", true);
    request.send(null);
    request.onreadystatechange = function () {
        if (request.readyState === 4 && request.status === 200) {
            var type = request.getResponseHeader('Content-Type');
            if (type.indexOf("text") !== 1) {
                var spl = request.responseText.split("\n");
                for (var i in spl) {
                    var lat = spl[i].split(", ")[0];
                    var lon = spl[i].split(", ")[1];
                    console.log(lat, lon);
                    new google.maps.Marker(
                        {
                            position: new google.maps.LatLng(lat, lon),
                            map: map,
                            title: lat + ", " + lon
                        }
                    )
                }
            }
        }
    };
}
