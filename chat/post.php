<?php
session_start();
require "classes/Messages.php";
$auth='';

$messages=new Messages($auth);

if (isset($_SESSION['name'])) {
    $name = $_SESSION['name'];
    } else {
    $name = $_POST['name'];
}

$messages->saveMessage($_POST['auth'],$name,$_POST['text']);
