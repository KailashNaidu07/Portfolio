<?php

require 'dependencies/vendor/autoload.php'; // Ensure PHPMailer is installed via Composer
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

if ($_SERVER['REQUEST_METHOD'] === "POST") {

    $mail = new PHPMailer(true);
    $email = $_POST['email'];
    $name = $_POST['name'];
    $subject = $_POST['subject'];
    $message = $_POST['message'];

    try {
        // Server settings
        $mail->isSMTP();
        $mail->Host = 'smtp.gmail.com'; // Replace with your SMTP server
        $mail->SMTPAuth = true;
        $mail->Username = 'wainainamartin29@gmail.com'; // Replace with your email
        $mail->Password = 'qhbb ajil bgwj suph'; // Replace with your password
        $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
        $mail->Port = 587;

        $mail->setFrom("myportfolio@codexoft.ke", "My Portfolio Website");

        $mail->addAddress('codexoftke@gmail.com'); // Add recipient email address
        // Create HTML table with submitted data
        $tableHTML = "<!DOCTYPE html>
<html lang='en'>

<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Contact Form Results</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;500&display=swap');
        body {
            font-family: 'Rubik', sans-serif;
        }
        .contact-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-family: Arial, sans-serif;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
        }

        .contact-table th,
        .contact-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #ddd;
        }

        .contact-table th {
            background-color: #4CAF50;
            color: white;
            text-align: left;
        }

        .contact-table tr:hover {
            background-color: #f5f5f5;
        }
    </style>
</head>

<body>
    <table class='contact-table'>
        <tr>
            <th>Field</th>
            <th>Value</th>
        </tr>
        <tr>
            <td>Name</td>
            <td>$name</td>
        </tr>
        <tr>
            <td>Email</td>
            <td>$email</td>
        </tr>
        <tr>
            <td>Subject</td>
            <td>$subject</td>
        </tr>
        <tr>
            <td>Message</td>
            <td>$message</td>
        </tr>
    </table>
</body>

</html>";

        $message = $tableHTML;
        $mail->isHTML(true);
        $mail->Subject = $subject;
        $mail->Body = $message;

        $mail->send();
        echo "Email was sent successfully";
    } catch (Exception $e) {
        echo $e;
        http_response_code(500);
    }
}