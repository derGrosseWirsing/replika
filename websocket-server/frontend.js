$(function () {
    "use strict";

    // for better performance - to avoid searching in DOM
    var content = $('.chats-text-cont .inner');
    var input = $('.input');
    var status = $('.intro');
    var usersOnline=$('#usersOnline');
    var adminPanel=$('#adminPanel');
    var emojis=$('.emojis');
    var chatTexts=$('.chat-body .chats-text-cont .inner');
    var chatInput=$('.chat-inp .input');
    var send=$('.chat-inp .opts .send');

    var admin = 0;
    $('#help').on('mousedown', function (e) {
        $('#help').fadeToggle(500);
    });
    // my color assigned by the server
    var myColor = false;
    // my name sent to the server
    var myName = false;

    // if user is running mozilla then use it's built-in WebSocket
    window.WebSocket = window.WebSocket || window.MozWebSocket;

    // if browser doesn't support WebSocket, just show some notification and exit
    if (!window.WebSocket) {
        content.html($('<p>', {
            text: 'Sorry, but your browser doesn\'t '
                + 'support WebSockets.'
        }));
        input.hide();
        $('span').hide();
        return;
    }

    // open connection
    var connection = new WebSocket('ws://localhost:8080');

    connection.onopen = function () {
        // first we want users to enter their names
        if (myName != false) {
            input.removeAttr('disabled');
        }
        status.html('Choose name: <input id="inputName" type="text" class="inputName" />');
        $('#inputName').keydown(function (e) {
            if (e.keyCode === 13) {

                var msg = $(this).val();
                if (!msg) {
                    return;
                }

                // send the message as an ordinary text
                connection.send(msg);
            }
        })
    };

    connection.onerror = function (error) {
        // just in there were some problems with connection...
        content.html($('<p>', {
            text: 'Sorry, but there\'s some problem with your '
                + 'connection or the server is down.'
        }));
    };

    // most important part - incoming messages
    connection.onmessage = function (message) {

        // try to parse JSON message. Because we know that the server always returns
        // JSON this should work without any problem but we should make sure that
        // the massage is not chunked or otherwise damaged.
        try {
            var json = JSON.parse(message.data);
        } catch (e) {
            console.log('This doesn\'t look like a valid JSON: ', message.data);
            return;
        }

        if (json.type === 'status') {
            if (json.data.status == 1 && json.data.author != false) {
                if (json.data.bot == 1) {
                    var botclass = "bot";
                }
                chatTexts.prepend('<div class="' + botclass + ' ' + json.data.author + 'preview chat" style="height:65px;display:none;"><p style="vertical-align:middle;" class="chat-text ' + botclass + ' ' + json.data.author + 'preview"><span><img style="margin:auto;display:block;height:30px;width:30px" src="loader.gif">' + json.data.author + ' is writing...</span></p><div>');
                $('div.' + botclass + '.' + json.data.author + 'preview').fadeIn(500);
            } else {
                if (json.data.bot == 1) {
                    var botclass = "bot";
                }

                $('div.' + botclass + '.' + json.data.author + 'preview').fadeOut(200, function () {
                    $('div.' + botclass + '.' + json.data.author + 'preview').remove();
                });

            }

        } else if (json.type === 'users') {
            if (admin == 1) {

                let adminUsers = "";
                $.each(json.data, function (index, value) {
                    
                    let chaosclass="";
                    let filterclass="";
                    let botadd="";
                    
                    if (value != false && value != null) {
                        if(value.chaos==1){chaosclass="chaoson";}
                        if(value.filter==1){filterclass="filteron";}
                        if(value.bot==1){botadd="<a data-id='" + index + "' class='chaos "+chaosclass+"' title='Chaos Mode'><i class='fas fa-comments'></i></a><a data-id='" + index + "' class='filter "+filterclass+"'><i class='fas fa-filter'></i></a>";}
                        adminUsers += "<span data-id='" + index + "'>" + value.name + "<a data-id='" + index + "' title='Kick User' class='kick'><i class='fas fa-minus-circle'></i></a>"+botadd+"</span>";
                    }
                });
                adminPanel.html(adminUsers);
                status.remove();
                adminPanel.find('span .filter').on('mousedown', function (e) {
                    connection.send(JSON.stringify({'type': 'filter', 'id': $(this).attr('data-id')}));
                });
                adminPanel.find('span .kick').on('mousedown', function (e) {
                    connection.send(JSON.stringify({'type': 'kick', 'id': $(this).attr('data-id')}));
                });
                adminPanel.find('span .chaos').on('mousedown', function (e) {
                    connection.send(JSON.stringify({'type': 'chaos', 'id': $(this).attr('data-id')}));
                });
            }

            usersOnline.html('');
            var users = '<span><a class="help"><i class="fas fa-question-circle"></i></a><strong>Users online: </strong></span>';
            usersOnline.html(users);
            console.log(json.data);
            $.each(json.data, function (index, value) {
                if (value != false && value != null) {

                    users += "<span data-id='" + value.name + "'>" + value.name + '</span>';
                }
            });

            usersOnline.html(users);
            usersOnline.find('span a.help').on('mousedown', function (e) {
                $('#help').fadeToggle(500);
            });
            usersOnline.find('span[data-id]').on('mousedown', function (e) {

                    $(this).toggleClass('active');
                    var str = input.val();

                    if (str.indexOf("@" + $(this).attr('data-id') + ":") == -1) {
                        input.val("@" + $(this).attr('data-id') + ":" + str);
                        input.focus();
                        e.preventDefault();
                    } else {
                        var str = input.val();
                        var res = str.replace("@" + $(this).attr('data-id') + ":", "");

                        input.val(res);
                        e.preventDefault();
                    }
                            });

        }

        // NOTE: if you're not sure about the JSON structure
        // check the server source code above
        if (json.type === 'color') { // first response from the server with user's color
            myColor = json.data;
            status.text("Welcome " + json.name);

            input.removeAttr('disabled');

            // from now user can start sending messages
        } else if (json.type === 'history') { // entire message history
            // insert every single message to the chat window
            for (var i = 0; i < json.data.length; i++) {
                addMessage(json.data[i].author, json.data[i].text,
                    json.data[i].color, new Date(json.data[i].time), json.data[i].bot, 1);
            }
        } else if (json.type === 'message') { // it's a single message

            input.removeAttr('disabled'); // let the user write another message
            addMessage(json.data.author, json.data.text,
                json.data.color, new Date(json.data.time), json.data.bot, 0);
        } else if (json.type === 'keep') {

        } else if (json.type === 'admin') {
            admin = 1;
        } else {
            console.log('Hmm..., I\'ve never seen JSON like this: ', json);

        }
    };


    var keycounter = 0;
    input.focusin(function () {

        keycounter = 0;
    });
    input.blur(function () {
        keycounter = 0;
        connection.send(JSON.stringify({'type': 'writing', 'writing': 0, 'bot': 0}));
    });


    emojis.keydown(function (e) {
        if (e.keyCode === 13) {
            var msg = input.val();
            if (!msg) {
                return;
            }
            keycounter = 0;
            input.blur();
            input.focus();
            connection.send(msg);
            input.val('');
        }
    });

    /**
     * Send message when user presses Enter key
     */
    input.keydown(function (e) {

        keycounter++;

        if (e.keyCode === 13) {

            var msg = $(this).val();
            if (!msg) {
                return;
            }
            keycounter = 0;
            input.blur();
            input.focus();
            // send the message as an ordinary text
            connection.send(msg);
            connection.send(JSON.stringify({'type': 'writing', 'writing': 0}));
            $(this).val('');

            // disable the input field to make the user wait until server
            // sends back response
            input.attr('disabled', 'disabled');

            // we know that the first message sent from a user their name
            if (myName === false) {
                myName = msg;
            }
        } else {
            if (keycounter == 3) {
                connection.send(JSON.stringify({'type': 'writing', 'writing': 1}));

            }
        }
    });

    send.click(function () {
        var msg = chatInput.val();

        if (!msg) {
            return;
        }

        // send the message as an ordinary text
        connection.send(msg);
        chatInput.val('');
        // disable the input field to make the user wait until server
        // sends back response
        input.attr('disabled', 'disabled');

        // we know that the first message sent from a user their name
        if (myName === false) {
            myName = msg;
        }




    });

    /**
     * This method is optional. If the server wasn't able to respond to the
     * in 3 seconds then show some error message to notify the user that
     * something is wrong.
     */
    setInterval(function () {
        if (connection.readyState !== 1) {
            status.text('Websocket offline');
            input.attr('disabled', 'disabled').text('Unable to comminucate '
                + 'with the WebSocket server.');
        }
    }, 3000);

    var audiobot = new Audio('pop.mp3');
    var audiohuman = new Audio('blupp.mp3');

    /**
     * Add message to the chat window
     */
    function addMessage(author, message, color, dt, bot, sound) {
        if (bot == 1) {
            var botclass = "bot";
            if (sound == 0) {

                audiobot.play();
            }
        } else {
            if (sound == 0) {

                audiohuman.play();
            }
        }

        if (message.indexOf("https://www.youtube.com/watch?v=") == 0) {
            let message_new;
            let message_array;
            message_new = message.replace("https://www.youtube.com/watch?v=", "");
            message_array = message_new.split('&');
            message = "<iframe width='400' height='300' src='https://www.youtube-nocookie.com/embed/" + message_array[0] + "' title='YouTube video player' frameborder='0' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture' allowfullscreen></iframe>";
        }

        var inhalt = '<p style="display:none;" class="chat-text ' + botclass + '"><span>' + author + ' @ ' +
            +(dt.getHours() < 10 ? '0' + dt.getHours() : dt.getHours()) + ':'
            + (dt.getMinutes() < 10 ? '0' + dt.getMinutes() : dt.getMinutes())
            + ':<br/> ' + message + '</span></p>';

        content.prepend(inhalt);
        $('.chat-text[style="display:none;"]').fadeIn(1000);

    }
});
