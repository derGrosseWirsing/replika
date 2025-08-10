# Server uses NodeJS Websocket
- npm install websocket
- node chat-server.js

- Here is a description and markup conversion for both `chat-server.js` and `frontend.js` from the `websocket-server` directory:

---

## `chat-server.js`

**Description:**  
This file is a Node.js-based WebSocket server for chat applications. It manages client connections, assigns colors and names, handles message broadcasting, admin actions (kick, chaos mode, filter), and keeps track of user status. Features include:

- Accepts WebSocket connections and tracks clients.
- Assigns each user a unique color and name.
- Supports admin actions (kick users, toggle chaos/filter modes).
- Broadcasts chat messages and user status to all connected clients.
- Maintains heartbeat/ping mechanism to detect and remove dead connections.
- Escapes incoming text for HTML safety.

**Markup Conversion:**

```js
// chat-server.js
"use strict";

process.title = 'node-chat';
const webSocketsServerPort = 8080;
const webSocketServer = require('websocket').server;
const http = require('http');

// List of connected clients and user data
let clients = {};
let userdata = {};

// Helper functions for JSON validation, UUID, escaping HTML
function hasJsonStructure(str) { /* ... */ }
function uuidv4() { /* ... */ }
function htmlEntities(str) { /* ... */ }

// Colors for users
let colors = ['red', 'green', 'blue', 'magenta', 'purple', 'plum', 'orange'];
colors.sort(() => Math.random() > 0.5);

// Create HTTP server (required for WebSocket)
let server = http.createServer((request, response) => { });
server.listen(webSocketsServerPort, () => {
    console.log("Server is listening on port " + webSocketsServerPort);
});

// Create WebSocket server
let wsServer = new webSocketServer({ httpServer: server });

// Heartbeat interval to check alive clients
const interval = setInterval(function ping() { /* ... */ }, 5000);

// On new WebSocket connection request
wsServer.on('request', function (request) {
    // Accept or reject connection, assign admin if localhost
    // Assign UUID, color, name
    // Listen for messages, parse JSON, handle admin actions, broadcast messages
    // Listen for disconnect/close, clean up client and color
});
```

[View chat-server.js on GitHub](https://github.com/derGrosseWirsing/replika/blob/main/websocket-server/chat-server.js)

---

## `frontend.js`

**Description:**  
This file is a jQuery-based frontend for the chat application, connecting to the WebSocket server. It provides a chat UI, manages user input, updates online users, and interacts with admin features. Features include:

- Connects to the WebSocket server.
- Allows users to enter names and send chat messages.
- Displays messages, user status, and color assignment.
- Supports admin controls: kick, chaos mode, filter.
- Updates chat UI dynamically based on server events.
- Plays sound effects for bot and human messages.
- Embeds YouTube videos if posted as links.

**Markup Conversion:**

```js
// frontend.js
$(function () {
    "use strict";

    // Cache DOM elements
    var content = $('.chats-text-cont .inner');
    var input = $('.input');
    var status = $('.intro');
    var usersOnline = $('#usersOnline');
    var adminPanel = $('#adminPanel');
    // ... Other UI elements

    var admin = 0;
    var myColor = false;
    var myName = false;

    // Check WebSocket support, connect to server
    if (!window.WebSocket) { /* ... */ return; }
    var connection = new WebSocket('ws://localhost:8080');

    connection.onopen = function () { /* Enable name input */ };
    connection.onerror = function (error) { /* Show error message */ };
    connection.onmessage = function (message) {
        // Parse JSON, update UI for status, users, color, history, messages
        // Admin controls: kick, chaos, filter
        // Display messages, add to chat window
    };

    // Input event handlers for sending messages, admin controls, etc.
    // Sound effects for bot/human messages
    function addMessage(author, message, color, dt, bot, sound) {
        // Format and add message to chat window, play sound, embed YouTube if present
    }
});
```

[View frontend.js on GitHub](https://github.com/derGrosseWirsing/replika/blob/main/websocket-server/frontend.js)

---

If you need a deeper breakdown or want full code for either file, let me know!
