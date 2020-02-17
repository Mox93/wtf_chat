// console.log("Starting...")
var storageKey = "store";
var flags = localStorage.getItem(storageKey);
var app = Elm.Main.init({flags: flags});

app.ports.storeCache.subscribe(function(val) {
    if (val === null) {
        localStorage.removeItem(storageKey);
    } else {
        localStorage.setItem(storageKey, JSON.stringify(val));
    }
    // Report that the new session was stored successfully.
    setTimeout(function() { app.ports.onStoreChange.send(val); }, 0);
});

// Whenever localStorage changes in another tab, report it if necessary.
window.addEventListener("storage", function(event) {
    // console.log(">>> window.addEventListener")
    if (event.storageArea === localStorage && event.key === storageKey) {
        // console.log("onStoreChange", event.newValue)
        app.ports.onStoreChange.send(event.newValue);
    }
}, false);
