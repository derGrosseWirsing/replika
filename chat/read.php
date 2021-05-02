<?php

require "classes/Messages.php";

/**
 * @param $number_of_bots:
 * 1: Every Message is responded to only once
 * 2: Every Message is responded to twice
 * and so on...
 * @param $auth: Key which is stored in py File
 * @param $chaos:
 * 0: Bots only respond to humans
 * 1: Bots only respond to Bots
 * 2: Bots respond to everyone
 */
$auth="";
$number_of_bots=2;
$chaos=0;

$messages=new Messages($auth,$number_of_bots);
$message=$messages->getLatestMessage($_GET['name'],$_GET['auth'],$chaos);

echo $message;