<?php
$conn = new mysqli("localhost", "root", "", "test");

$name = $_GET['name'];

$result = $conn->query("SELECT id, name FROM users WHERE name = '$name'");

while($row = $result->fetch_assoc()) {
    echo $row['name'];
}
?>
