<?php
$id = $_POST['id'];
$conn->query("DELETE FROM users WHERE id = $id");
?>
