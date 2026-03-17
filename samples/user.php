<?php
$name = $_GET['name'];
$conn->query("SELECT id, name FROM users WHERE name = '$name'");
?>
