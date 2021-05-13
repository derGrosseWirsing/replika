<?php
session_start();
require 'libs/Smarty.class.php';

$smarty = new Smarty;
$smarty->caching = false;
$smarty->cache_lifetime = 300;
$smarty->compile_check = false;


try {
    $smarty->display('index_new.tpl');
} catch (SmartyException $e) {
    return $e->getMessage();
}
