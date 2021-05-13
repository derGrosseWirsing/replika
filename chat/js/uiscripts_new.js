$(document).ready(function () {



    $('.chat-inp .emoji').click(function () {
        $('.emoji-dashboard').slideToggle('fast');
    });
    $('.chat-body,#input').click(function () {
        $(".emoji-dashboard").slideUp('fast');
    });
    $(".chat-header .menu ul.list,.chat-inp .emoji").click(function (e) {
        e.stopPropagation();
    });
    $('.emoji-dashboard li').click(function () {
        var emo = $(this).text();


        $('.chat-inp .input').val($('.chat-inp .input').val() + emo);


    });









});
