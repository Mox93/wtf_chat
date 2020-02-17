console.log("Starting...");


function intiSocket(ns, token) {
    return io(ns, { transportOptions: { polling: {
        extraHeaders: { 'Authorization': 'Bearer ' + token }
    }}});
};


// Initialization
const storageKey = "store";
const configKey = "config";

var storage;
var socket;

var flags = localStorage.getItem(storageKey);
const app = Elm.Main.init({flags: flags});

app.ports.storeCache.subscribe(function(val) {
    if (val === null) {
        localStorage.removeItem(storageKey);
        console.log("Disconnecting...");
        socket.close();
    } else {
        localStorage.setItem(storageKey, JSON.stringify(val));
        storage = JSON.parse( localStorage.getItem(storageKey) );

        if (!socket || socket.disconnected) {
            socket = intiSocket(namespace, storage.viewer.access);
        };
    };
    // Report that the new session was stored successfully.
    setTimeout(function() { app.ports.onStoreChange.send(val); }, 0);
});


// Whenever localStorage changes in another tab, report it if necessary.
window.addEventListener("storage", function(event) {
    if (event.storageArea === localStorage && event.key === storageKey) {
        app.ports.onStoreChange.send(event.newValue);
    };
}, false);


// SocketIO
storage = JSON.parse( localStorage.getItem(storageKey) );

if (storage) {
    socket = intiSocket(namespace, storage.viewer.access);
}

socket.on('connect', function() {
    console.log("Connecting...")
    socket.emit('init');
});

//app.ports.sendMessage.subscribe(function(message) {
//    socket.emit('send message', message);
//});

socket.on('new message', function(message) {
    app.ports.receiveMessage.send(message);
});
