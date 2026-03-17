<?php
$id = $_POST['id'];
$name = $_POST['name'];
$conn->query("UPDATE users SET name = '$name' WHERE id = $id");
?>
