// http://ejohn.org/blog/ecmascript-5-strict-mode-json-and-more/
"use strict";

// Optional. You will see this name in eg. 'ps' or 'top' command
process.title = 'node-chat';

// Port where we'll run the websocket server
var webSocketsServerPort = 8080;

// websocket and http servers
var webSocketServer = require('websocket').server;
var http = require('http');

/**
 * Global variables
 */


// list of currently connected clients (users)
var clients = {};
var userdata = {};

// check for json
function hasJsonStructure(str) {
    if (typeof str !== 'string') return false;
    try {
        const result = JSON.parse(str);
        const type = Object.prototype.toString.call(result);
        return type === '[object Object]'
            || type === '[object Array]';
    } catch (err) {
        return false;
    }
}

// For user and client index
function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

/**
 * Helper function for escaping input strings
 */
function htmlEntities(str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;')
        .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// Array with some colors
var colors = ['red', 'green', 'blue', 'magenta', 'purple', 'plum', 'orange'];
// ... in random order
colors.sort(function (a, b) {
    return Math.random() > 0.5;
});

/**
 * HTTP server
 */
var server = http.createServer(function (request, response) {
    // Not important for us. We're writing WebSocket server, not HTTP server
});
server.listen(webSocketsServerPort, function () {
    console.log((new Date()) + " Server is listening on port " + webSocketsServerPort);
});

/**
 * WebSocket server
 */
var wsServer = new webSocketServer({
    // WebSocket server is tied to a HTTP server. WebSocket request is just
    // an enhanced HTTP request. For more info http://tools.ietf.org/html/rfc6455#page-6
    httpServer: server
});

// for ping
function noop() {
}

// When client sends a pong
function heartbeat(ws) {
    this.isAlive = true;
    console.log("pong");

}

// Ping interval to delete dead connections
const interval = setInterval(function ping() {


    let key;
    for (key in clients) {
        // console.log(clients[key].remoteAddresses[0]);
        // isAlive is set in heartbeat function on pong
        if (clients[key].isAlive === false) {

            // give  client 4 retries
            if (clients[key].retry == 4) {
                delete userdata[key];
                return clients[key].close();

            } else {
                clients[key].retry++;
            }

        }
        // Send online users for frontend when client is alive
        clients[key].sendUTF(JSON.stringify({type: 'users', data: userdata}));

        clients[key].retry = 0;
        clients[key].isAlive = false;
        clients[key].ping(noop);
    }

}, 5000);

// This callback function is called every time someone
// tries to connect to the WebSocket server
wsServer.on('request', function (request) {

    console.log((new Date()) + ' Connection from origin ' + request.origin + '.');
    console.log("clientID: " + request.clientId);
    // accept connection - you should check 'request.origin' to make sure that
    // client is connecting from your website
    // (http://en.wikipedia.org/wiki/Same_origin_policy)
    if (request.origin == "http://localhost:8080" ||
        request.origin == "http://localhost") {
        var connection = request.accept(null, request.origin);
    } else {
        return;
    }

    // set user to admin
    if (request.origin == "http://localhost") {
        connection.admin = 1;
        connection.sendUTF(JSON.stringify({type: 'admin', data: "keep"}));
    }

    // we need to know client index to remove them on 'close' event
    // Index is an uuid
    var uuid = uuidv4();
    var index = uuid;
    clients[index] = connection;
    var userName = false;
    var userColor = false;
    var bot = 0;

    userdata[index] = {'name': "Guest", 'ip': connection.remoteAddresses[0], 'chaos': 0, 'filter': 0};
    connection.isAlive = true;
    connection.retry = 0;
    connection.on('pong', heartbeat(connection));
    connection.userId = index;


    console.log((new Date()) + ' Connection accepted.');

    const interval = setInterval(function checkmessages() {
        connection.sendUTF(JSON.stringify({type: 'keep', data: "keep"}));
    }, 5000);


    // user sent some message

    connection.on('message', function (message) {
        let key;
        for (key in clients) {
            clients[key].sendUTF(JSON.stringify({type: 'users', data: userdata}));
        }


        if (message.type === 'utf8') { // accept only text


            if (hasJsonStructure(message.utf8Data)) {
                var botObj = JSON.parse(message.utf8Data);

                // bot registered
                if (botObj.type == 'botconnection') {
                    bot = 1;
                    userdata[index]['bot'] = 1;
                    userdata[index]['name'] = botObj.name;
                    console.log("---_" + botObj.name);
                    var botname = htmlEntities(botObj.name);
                    delete userdata[botObj.id];
                    for (key in clients) {
                        clients[key].sendUTF(JSON.stringify({type: 'users', data: userdata}));
                    }

                }

                // kick from admin
                if (botObj.type == 'kick' && connection.admin == 1) {
                    clients[botObj.id].close();
                    delete userdata[botObj.id];
                    for (key in clients) {
                        clients[key].sendUTF(JSON.stringify({type: 'users', data: userdata}));
                    }
                    return;
                }

                // chaos mode from admin
                if (botObj.type == 'chaos' && connection.admin == 1) {
                    if (userdata[botObj.id]['chaos'] == 0) {
                        userdata[botObj.id]['chaos'] = 1;
                    } else {
                        userdata[botObj.id]['chaos'] = 0;
                    }

                    clients[botObj.id].sendUTF(JSON.stringify({type: 'chaos', data: "go"}));

                    for (key in clients) {
                        clients[key].sendUTF(JSON.stringify({type: 'users', data: userdata}));
                    }

                    return;
                }

                // filter switch from admin
                if (botObj.type == 'filter' && connection.admin == 1) {
                    if (userdata[botObj.id]['filter'] == 0) {
                        userdata[botObj.id]['filter'] = 1;
                    } else {
                        userdata[botObj.id]['filter'] = 0;
                    }

                    clients[botObj.id].sendUTF(JSON.stringify({type: 'filter', data: "go"}));
                    clients[botObj.id].sendUTF(JSON.stringify({type: 'userdata', data: userdata[index]}));
                    for (key in clients) {
                        clients[key].sendUTF(JSON.stringify({type: 'users', data: userdata}));
                    }
                    return;
                }

                // writing status
                if (botObj.type == "writing") {
                    var resObj = {
                        author: userName,
                        color: userColor,
                        status: botObj.writing,
                        bot: bot
                    };

                    var jsonWriting = JSON.stringify({type: 'status', data: resObj});
                    let key;
                    for (key in clients) {
                        clients[key].sendUTF(jsonWriting);
                    }
                    return;
                }


            }

            if (userName === false) { // first message sent by user is their name

                if (bot === 1) {
                    userName = botname;
                    clients[index].bot = 1;
                    userdata[index]['bot'] = 1;

                } else {
                    userdata[index]['bot'] = 0;

                    // remember user name
                    userName = htmlEntities(message.utf8Data);
                }

                // get random color and send it back to the user
                userColor = colors.shift();
                connection.sendUTF(JSON.stringify({type: 'color', data: userColor, name: userName}));

                userdata[index]['name'] = userName;
                console.log((new Date()) + ' User is known as: ' + userName
                    + ' with ' + userColor + ' color.');

                console.log(userdata);
                let key;
                for (key in clients) {
                    clients[key].sendUTF(JSON.stringify({type: 'users', data: userdata}));
                }

            } else { // log and broadcast the message
                console.log((new Date()) + ' Received Message from '
                    + userName + ': ' + message.utf8Data);


                var obj = {
                    time: (new Date()).getTime(),
                    text: htmlEntities(message.utf8Data),
                    author: userName,
                    color: userColor,
                    bot: bot
                };


                // broadcast message to all connected clients
                var json = JSON.stringify({type: 'message', data: obj});

                let key;
                for (key in clients) {
                    clients[key].sendUTF(json);
                }

            }
        }
    });

    // user disconnected
    connection.on('disconnect', function (connection) {
        console.log('onDisconnect');
        if (userName !== false && userColor !== false) {
            console.log((new Date()) + " Peer "
                + userdata[index]['ip'] + " disconnected.");
            // remove user from the list of connected clients
            delete clients[index];
            delete userdata[index];
            // push back user's color to be reused by another user
            colors.push(userColor);

            for (key in clients) {
                clients[key].sendUTF(JSON.stringify({type: 'users', data: userdata}));
            }
        }
    });


    // user disconnected
    connection.on('close', function (connection) {

        clearInterval(interval);

        console.log((new Date()) + " Peer "
            + userdata[index]['ip'] + " disconnected.");


        // remove user from the list of connected clients
        delete clients[index];

        delete userdata[index];
        colors.push(userColor);
        let key;
        for (key in clients) {
            clients[key].sendUTF(JSON.stringify({type: 'users', data: userdata}));
        }


    });

});
