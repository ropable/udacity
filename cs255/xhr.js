function xhrGet(reqUri, callback, type) {
    var caller = xhrGet.caller;
    var xhr = new XMLHttpRequest();
    var setup = function() {
        xhr.open('GET', reqUri, true);
        if (type) {
            xhr.responseType = type;
        }
        xhr.onload = function () {
            if (callback) {
                try {
                    callback(xhr);
                } catch(e) {
                    throw 'xhrGet failed:\n' + reqUri + '\nException: ' + e + '\nresponseText: ' + xhr.responseText + '\ncaller: ' + caller;
                }
            }
        };
        xhr.send();
    };
    setup();
}

parseJSON = function (xhr) {
    var parsedJSON = JSON.parse(xhr.responseText);
    var x = parsedJSON.frames['chaingun_impact.png'].spriteSourceSize.x;
    return x;
};

playSound = function (xhr) {
    try {
        var context = new webkitAudioContext();
        var mainNode = context.createGainNode(0);
        mainNode.connect(context.destination);
        var clip = context.createBufferSource();
        context.decodeAudioData(xhr.response, function (buffer) {
            clip.buffer = buffer;
            clip.gain.value = 1.0;
            clip.connect(mainNode);
            clip.loop = true;
            clip.noteOn(0);
        }, function (data) {});
    }
    catch(e) {
        console.warn('Web Audio API is not supported in this browser');
    }
};

// Test code for you to run
var test = function() {
    // Note that these server locations seem to lack the assets at time of writing.
    // Code passes tests though.
    xhrGet('/media/js/standalone/libs/gamedev_assets/weapon.json', parseJSON, null);
    xhrGet('/media/js/standalone/libs/gamedev_assets/bg_menu.ogg', playSound, 'arraybuffer');
};
