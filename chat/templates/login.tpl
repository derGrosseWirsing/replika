{config_load file="test.conf" section="setup"}
{include file="header.tpl" title="Replika Chat Login"}

<div id="loginform">
    <form action="index_new.php" method="post">
        <p>Please enter your name to continue:</p>
        <label for="name">Name:</label>
        <input type="text" name="name" id="name" />
        <button name="enter" id="enter" value="Enter" >Enter</button>
    </form>
</div>

{include file="footer.tpl"}