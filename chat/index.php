<?php
session_start();
require 'libs/Smarty.class.php';

$smarty = new Smarty;
$smarty->caching = true;
$smarty->cache_lifetime = 300;
$smarty->compile_check = false;

if (isset($_POST['enter']) && $_POST['name'] !== "") {
    $_SESSION['name'] = stripslashes(htmlspecialchars($_POST['name']));
} elseif (!isset($_SESSION['name'])) {
    $smarty->assign('login', '<span class="error">Please type in a name</span>');
    try {
        $smarty->display('login.tpl');
    } catch (SmartyException $e) {
        return $e->getMessage();
    }
} else {

    if (file_exists("log.txt") && filesize("log.txt") > 0) {
        $handle = fopen("log.txt", "r");
        $contents = fread($handle, filesize("log.txt"));
        fclose($handle);

        $smarty->assign('content', $contents);
    }

    $smarty->assign('loggedIn', 1);
    $smarty->assign("name", $_SESSION['name']);
    try {
        $smarty->display('index.tpl');
    } catch (SmartyException $e) {
        return $e->getMessage();
    }
}

