// Parse JSON.
JSONExample = {
    "frames": {
        "chaingun.png": {
            "frame": {
                "x": 1766,
                "y": 202,
                "w": 42,
                "h": 34
            },
            "rotated": false,
            "trimmed": true,
            "spriteSourceSize": {
                "x": 38,
                "y": 32,
                "w": 42,
                "h": 34
            },
            "sourceSize": {
                "w": 128,
                "h": 128
            }
        },
        "chaingun_impact.png": {
            "frame": {
                "x":1162,
                "y":322,
                "w":38,
                "h":34},
            "rotated": false,
            "trimmed": true,
            "spriteSourceSize": {
                "x":110,
                "y":111,
                "w":38,
                "h":34},
            "sourceSize": {
                "w":256,
                "h":256}
        },
        "chaingun_impact_0000.png": {
            "frame": {
                "x": 494,
                "y": 260,
                "w": 22,
                "h": 22
            },
            "rotated": false,
            "trimmed": true,
            "spriteSourceSize": {
                "x": 113,
                "y": 108,
                "w": 22,
                "h": 22
            },
            "sourceSize": {
                "w": 256,
                "h": 256
            }
        }
    }
};

parseJSON = function (weaponJSON) {
    var parsed = JSON.parse(weaponJSON);
    var x_field = parsed['frames']['chaingun_impact.png']['spriteSourceSize'].x;
    console.log(x_field);
    return x_field;
};

// XMLHttpRequest.
parseJSON = function (weaponJSON) {
    parsedJSON = JSON.parse(weaponJSON);
    return parsedJSON['frames']['chaingun_impact.png']['spriteSourceSize']['x'];
};

// Create a new XMLHttpRequest object
var weaponXHR = new XMLHttpRequest();

var setup = function() {
    // then use its open method to to define the request that
    // will be sent.
    weaponXHR.open('GET', "/media/js/standalone/libs/gamedev_assets/weapon.json", true);
    // After that, we want to define the onload method
    // of the request to be our parsing function from
    // before.
    weaponXHR.onload = function() {
        var x = parseJSON(this.responseText);
        return x;
    };
    // Finally, we want to call the send method of the
    // request object to actually send the request.
    weaponXHR.send();
};


// Manipulate the DOM.
var manipulateDOM = function() {
    var body = document.getElementById("body");
    var new_div = document.createElement("div");
    new_div.id = "gameContent";
    body.appendChild(new_div);
    var new_canvas = document.createElement("canvas");
    new_canvas.id = "gameCanvas";
    new_div.appendChild(new_canvas);
};
