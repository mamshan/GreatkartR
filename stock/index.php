<?php


$result = file_get_contents('http://124.43.12.72/SW_APP/stock_balget.php?skuno=' . $_GET['skuno']);
  
echo $result;

?>