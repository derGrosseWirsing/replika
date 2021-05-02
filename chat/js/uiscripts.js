$(document).ready(function () {

    $('.chat-header .menu .menu-ico').click(function () {
        $('.chat-header .menu ul.list').slideToggle('fast');
    });
    $(document).click(function () {
        $(".chat-header .menu ul.list").slideUp('fast');
    });
    $(".chat-header .menu ul.list,.chat-header .menu .menu-ico").click(function (e) {
        e.stopPropagation();
    });
    $('.chat-inp .emoji').click(function () {
        $('.emoji-dashboard').slideToggle('fast');
    });
    $(document).click(function () {
        $(".emoji-dashboard").slideUp('fast');
    });
    $(".chat-header .menu ul.list,.chat-inp .emoji").click(function (e) {
        e.stopPropagation();
    });
    $('.emoji-dashboard li').click(function () {
        var emo = $(this).html();

        $('.chat-inp .input').find('div').remove();
        $('.chat-inp .input').val($('.chat-inp .input').val() + emo);
        $(".emoji-dashboard").slideUp('fast');

    });
    $('.chat-inp .opts .send').click(function () {
        var val = $('.chat-inp .input').val();


        if (val.length > 0) {
            $('.chat-body .chats-text-cont .inner').append('<p class="chat-text"><span><img style="display:block;height:25px;width:25px" src="loader.gif"></span></p>')
            $('.chats-text-cont').scrollTop($('.inner').height());
            $.post("post.php", {text: val}, function () {

            });

            // $('.chat-body .chats-text-cont').append('<p class="chat-text"><span>'+val+'</span></p>')

        }
        $('.chat-inp .input').val('');

    });
    $('input,.input').each(function () {
        tmpval = $(this).text().length;
        if (tmpval != '') {
            $(this).prev().addClass('trans');
            $(this).parent().addClass('lined');
        }
    });
    $('input,.input').focus(function () {
        $(this).prev().addClass('trans');
        $(this).parent().addClass('lined');
        $(document).keypress(function (e) {
            if (e.which == 13) {
                $('.chat-inp .opts .send').click();
            }
        });
    }).blur(function () {
        if ($(this).text().length == '') {
            $(this).prev().removeClass('trans');
            $(this).parent().removeClass('lined');
        }
    });

    //Load the file containing the chat log
    function loadLog() {

        $.ajax({
            url: "log.txt",
            cache: false,
            success: function (html) {
                $(".inner").html(html); //Insert chat log into the #chatbox div


                $('.chats-text-cont').scrollTop($('.inner').height());

            },
        });
    }

    setInterval(loadLog, 2500);	//Reload file every 2.5 seconds

    //If user wants to end session
    $("#exit").click(function () {
        var exit = confirm("Are you sure you want to end the session?");
        if (exit == true) {
            window.location = 'index.php?logout=true';
        }
    });

});
