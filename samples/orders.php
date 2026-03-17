<?php
$user_id = $_GET['user_id'];
$conn->query("SELECT * FROM orders WHERE user_id = $user_id");
?>
