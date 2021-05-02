{config_load file="test.conf" section="setup"}
{include file="header.tpl" title="Open Replika Chat"}

<div class="body">

    <h2 class="intro" style="color:#fff;text-align:center;">Welcome {$name}!</h2>
    <div class="burg-menu">

        <p class="logout">
            <button id="exit" href="#">Exit Chat</button>
        </p>
    </div>

    <div class="chat-cont">

        <div class="chat-body">
            <div class="chats-text-cont">
                <div class="inner">
                    {$content}
                </div>
            </div>
        </div>
        <div class="chat-inp">
            <div class="emoji"></div>
            <div class="chat-input">
                <input type="text" class="input"/>
            </div>
            <div class="opts">

                <a class="send"></a>
            </div>
        </div>
        <div class="emoji-dashboard">
            {include file="emojis.tpl"}
        </div>
    </div>
</div>

{include file="footer.tpl"}
