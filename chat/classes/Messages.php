<?php

require_once "ConnectDb.php";

class Messages
{
    private $db;
    private $number_of_bots;
    private $auth;

    /**
     * Messages constructor.
     * @param string $auth
     * @param int $number_of_bots
     */
    public function __construct(string $auth,int $number_of_bots=2)
    {
        $this->auth = $auth;
        $this->number_of_bots = $number_of_bots;
        $db = new connectDb("", "", "", "");
        $this->db = $db;
    }

    /**
     * @param string $name
     * @param string $auth
     * @param int $chaos
     * @return String
     */
    public function getLatestMessage(string $name, string $auth, int $chaos):String
    {
        if ($this->auth === $auth) {

            $dbConn = $this->db->connect();

            if (mysqli_connect_errno()) {
                return mysqli_connect_error();
            }

            $nameClean = $dbConn->real_escape_string($name);

            $query = "SELECT id,message,processed,author FROM messages WHERE 
                    author NOT LIKE '$nameClean' AND `processed` <= $this->number_of_bots";

            /**
             * $chaos:
             * 0=Bots only respond to human
             * 1=bots only respond to bots
             * 2=bots respond to everyone (danger -> mayhem!)
             */
            switch ($chaos) {
                case 2:
                    $addSql = "";
                    break;
                default:
                    $addSql = " AND `bot` = $chaos";
                    break;
            }

            $query .= $addSql . " ORDER BY created ASC LIMIT 1";

            $result = $dbConn->query($query);

            while ($row = $result->fetch_row()) {
                [$id, $message, $processed, $author] = $row;
                }

            $processed++;

            $this->updateMessages( $processed, $this->number_of_bots, $id);

            mysqli_close($dbConn);

            $responseArray['recipient'] = "@" . $author;
            $responseArray['message'] = $this->checkAddress($name, $message);

            if(is_null($this->checkAddress($name, $message))){
                return "";
            }

            return json_encode($responseArray);

        }
        return "";
    }

    /**
     * @param string $name
     * @param string $message
     * @return string
     */
    protected function checkAddress(string $name, string $message):string
    {
        $needle = '@' . $name . ':';
        $needle2 = '@' . strtolower($name) . ':';

        if (strpos($message, '@') === 0) {
            if (strpos($message, $needle) === 0 ||
                strpos($message, $needle2) === 0) {
                $message = str_replace(array($needle, $needle2), '', $message);
                return $message;
            }

            return "";

        } else {
            return $message;
        }

    }

    /**
     * @param int $processed_messages
     * @param int $number_of_bots
     * @param int $id
     */
    protected function updateMessages(int $processed_messages, int $number_of_bots, int $id)
    {
        $dbCon=$this->db->connect();
        if ($processed_messages >= $number_of_bots) {
            $dbCon->query("DELETE FROM messages WHERE id=$id");
        } else {
            $dbCon->query("UPDATE messages SET processed=$processed_messages WHERE id=$id");
        }
    }

    /**
     * @param $auth
     * @param $name
     * @param $message
     */
    public function saveMessage($auth = null, $name=NULL, $message=NULL)
    {
        $isBot = 1;

        if (is_null($auth)) {
            $isBot = 0;
        }elseif ($auth!==$this->auth){
            return "Auth error!";
        }

        if (!is_null($name) && $message) {

            $dbCon = $this->db->connect();
            $name = $dbCon->real_escape_string($name);
            $message=strip_tags($message);
            $messageClean = $dbCon->real_escape_string($message);

            $saveQuery = "INSERT INTO messages (author,message,bot)  VALUES ('$name','$messageClean',$isBot)";

            $dbCon->query($saveQuery);
            $this->saveFile($isBot, $name, $message);
        }
    }

    /**
     * @param int $bot
     * @param string $name
     * @param string $message
     */
    protected function saveFile(int $bot=0, string $name, string $message)
    {
        $fp = fopen(__dir__ . "/../log.txt", 'a');
        if($bot==1){
            $botClass="bot";
        }

        fwrite($fp,
            "<p class='chat-text " . $botClass . "'><span><strong>(" . date("g:i A") . ") " . $name . ":</strong><br>" . strip_tags($message) . "</span></p>");
        fclose($fp);
    }
}