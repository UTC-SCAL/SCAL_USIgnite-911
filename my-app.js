var markers = [];
var map;
var icons = [
    "https://raw.githubusercontent.com/oitsjustjose/SCAL_USIgnite-911/gh-pages/icons/mon.png",
    "https://raw.githubusercontent.com/oitsjustjose/SCAL_USIgnite-911/gh-pages/icons/tues.png",
    "https://raw.githubusercontent.com/oitsjustjose/SCAL_USIgnite-911/gh-pages/icons/wed.png",
    "https://raw.githubusercontent.com/oitsjustjose/SCAL_USIgnite-911/gh-pages/icons/thurs.png",
    "https://raw.githubusercontent.com/oitsjustjose/SCAL_USIgnite-911/gh-pages/icons/fri.png",
    "https://raw.githubusercontent.com/oitsjustjose/SCAL_USIgnite-911/gh-pages/icons/sat.png",
    "https://raw.githubusercontent.com/oitsjustjose/SCAL_USIgnite-911/gh-pages/icons/sun.png"
];
var daysAllowed = {
    "Monday": false,
    "Tuesday": false,
    "Wednesday": false,
    "Thursday": false,
    "Friday": false,
    "Saturday": false,
    "Sunday": false
};

var typesAllowed = {
    "Unknown Injuries": false,
    "No Injuries": false,
    "Injuries": false,
    "Delayed": false,
    "Entrapment": false
};

var timesAllowed = {
    "00:00-1:59": false,
    "02:00-3:59": false,
    "04:00-5:59": false,
    "06:00-7:59": false,
    "08:00-9:59": false,
    "10:00-11:59": false,
    "12:00-13:59": false,
    "14:00-15:59": false,
    "16:00-17:59": false,
    "18:00-19:59": false,
    "20:00-21:59": false,
    "22:00-23:59": false
};

function toggle_type(element, criteria) {
    if (!typesAllowed[criteria]) {
        typesAllowed[criteria] = true;
        element.innerHTML += "<i class='ui right checkmark icon'></i>"
    }
    else {
        typesAllowed[criteria] = false;
        element.innerHTML = criteria;
    }
    updateMapMarkers();
}

function toggle_day(element, criteria) {
    // Indicates that there IS an icon:
    if (!daysAllowed[criteria]) {
        daysAllowed[criteria] = true;
        element.innerHTML += "<i class='ui right checkmark icon'></i>"
    }
    else {
        daysAllowed[criteria] = false;
        element.innerHTML = criteria;
    }
    updateMapMarkers();
}

function update_time() {
    var selectVals = $('#dropdown').val();
    timesAllowed = {
        "00:00-1:59": false,
        "02:00-3:59": false,
        "04:00-5:59": false,
        "06:00-7:59": false,
        "08:00-9:59": false,
        "10:00-11:59": false,
        "12:00-13:59": false,
        "14:00-15:59": false,
        "16:00-17:59": false,
        "18:00-19:59": false,
        "20:00-21:59": false,
        "22:00-23:59": false
    };
    for (var i in selectVals) {
        timesAllowed[selectVals[i]] = true;
    }
    updateMapMarkers();
}

function initPage() {
    var center = new google.maps.LatLng(35.0479, -85.2960);
    var options =
        {
            zoom: 15,
            center: center
        };
    map = new google.maps.Map(document.getElementById("map"), options);
}

function updateMapMarkers() {
    for (var i in markers) {
        markers[i].setMap(null);
    }
    markers = [];
    var request = new XMLHttpRequest();
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
                    var day = spl[i].split(",")[2].substring(1);
                    var time = spl[i].split(",")[5];
                    var reportType = spl[i].split(",")[6].substring(1);
                    if (!daysAllowed[day]) {
                        continue;
                    }
                    if (!typesAllowed[reportType]) {
                        continue;
                    }
                    if (!isWithinTimeRange(time)) {
                        continue;
                    }
                    var lat = spl[i].split(",")[0];
                    var lon = spl[i].split(",")[1];
                    var index = getIndex(day);
                    markers[i] = new google.maps.Marker(
                        {
                            position: new google.maps.LatLng(lat, lon),
                            icon: icons[index],
                            map: map
                        }
                    );
                }
            }
        }
    };
}

function isWithinTimeRange(time) {
    var hour = parseInt(time.split(":")[0]);
    var minute = parseInt(time.split(":")[1]);
    for (var i in timesAllowed) {
        var hourStart = parseInt(i.split("-")[0].split(":")[0]);
        var minuteStart = parseInt(i.split("-")[0].split(":")[1]);
        var hourEnd = parseInt(i.split("-")[1].split(":")[0]);
        var minuteEnd = parseInt(i.split("-")[1].split(":")[1]);

        if (hourStart <= hour && hour <= hourEnd) {
            if (minuteStart <= minute && minute <= minuteEnd) {
                return timesAllowed[i];
            }
        }
    }
    return false;
}


function getIndex(date) {
    if (date.indexOf("Monday") !== -1) {
        return 0;
    }
    if (date.indexOf("Tuesday") !== -1) {
        return 1;
    }
    if (date.indexOf("Wednesday") !== -1) {
        return 2;
    }
    if (date.indexOf("Thursday") !== -1) {
        return 3;
    }
    if (date.indexOf("Friday") !== -1) {
        return 4;
    }
    if (date.indexOf("Saturday") !== -1) {
        return 5;
    }
    if (date.indexOf("Sunday") !== -1) {
        return 6;
    }
}