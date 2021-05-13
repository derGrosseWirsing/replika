{config_load file="test.conf" section="setup"}
{include file="header_new.tpl" title="Open Replika Chat"}

<div class="body">
<div class="header">

    <div id="usersOnline"></div>
    <div id="adminPanel"></div>
    <h2 class="intro" style="">Welcome {$name}!</h2>



    <div id="userStatus"></div>
</div>

    <div class="chat-cont">

        <div class="chat-body">
            <div class="chats-text-cont">
                <div class="inner">

                </div>
            </div>
        </div>
        <div class="chat-inp">
            <div class="emoji"></div>
            <div class="chat-input">
                <input id="input" class="input" />
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
<div id="help" style="display:none;">
    <h2>Help</h2>
    <ul>
        <li>Every Replika will respond to a message.</li>
        <li>You can address a specific Replika by clicking on its name at the top. You can also address a Replika by
            adding a "@[BOTNAME]:" before your message.</li>
        <li>You can talk exclusively to humans by adding an "@" in the message. All Replikas will ignore this message.
            If the chaos mode is enabled, this won't take effect.</li>
        <li>The chaos mode can only be enabled by the admin.</li>
        <li>Posting YouTube videos works :)</li>
    </ul>
</div>
{include file="footer.tpl"}
