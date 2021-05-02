<?php


class ConnectDb
{
    protected $user;
    protected $db;
    protected $host;
    protected $password;

    /**
     * connectDb constructor.
     * @param $user
     * @param $db
     * @param $host
     * @param $password
     */
    public function __construct($host,$user,$password,$db)
    {
        $this->db=$db;
        $this->host=$host;
        $this->user=$user;
        $this->password=$password;
    }

    /**
     * @return mysqli|string
     */
    public function connect(){
        try{
            return mysqli_connect($this->host,$this->user,$this->password,$this->db);
        }catch(Exception $e){
            return $e->getCode().":".$e->getMessage();
        }
    }


}