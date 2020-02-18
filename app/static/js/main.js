console.log("Starting...");


function intiSocket(token) {
    return io(namespace, { transportOptions: { polling: {
        extraHeaders: { 'Authorization': 'Bearer ' + token }
    }}});
};


function startListening() {
    socket.on('connect', function() {
        console.log("Connecting...");
        socket.emit('init');
    });

    socket.on('disconnect', function() {
            console.log("Disconnecting...");
        socket.emit('kill');
    });

    //app.ports.sendMessage.subscribe(function(message) {
    //    socket.emit('send message', message);
    //});

    socket.on('new message', function(message) {
        app.ports.receiveMessage.send(message);
    });
};


function manageSocket() {
    storage = JSON.parse( localStorage.getItem(storageKey) );

    if (socket && socket.disconnected) {
        socket.open();
    } else if (!socket && storage) {
        socket = intiSocket(storage.viewer.access);
        startListening()
    };
};


// Initialization
const storageKey = "store";
const configKey = "config";

var storage;
var socket;

var flags = localStorage.getItem(storageKey);
var app = Elm.Main.init({flags: flags});

app.ports.storeCache.subscribe(function(val) {
    if (val === null) {
        localStorage.removeItem(storageKey);
        if (socket && socket.connected) {
            socket.close();
        };
    } else {
        localStorage.setItem(storageKey, JSON.stringify(val));
        manageSocket();
    };
    // Report that the new session was stored successfully.
    setTimeout(function() { app.ports.onStoreChange.send(val); }, 0);
});


// Whenever localStorage changes in another tab, report it if necessary.
window.addEventListener("storage", function(event) {
    if (event.storageArea === localStorage && event.key === storageKey) {
        var newVal = JSON.parse(event.newValue);
        console.log("***", newVal);
        app.ports.onStoreChange.send(newVal);
    };
}, false);


// SocketIO
manageSocket();
