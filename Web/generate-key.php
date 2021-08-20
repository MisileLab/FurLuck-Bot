<?php
    $properties = parse_ini_file('captcha.key');
    $userid = $_POST['userid'];
    $captcha = $_POST['g-recaptcha'];
    $secretKey = $properties['secret'];
    $ip = $_SERVER['REMOTE_ADDR']; // 옵션값으로 안 넣어도 됩니다.
    $is_authorized = false;
    $now_timestamp = time();
    $key = "";
    $mysqlhost = $properties['host'];
    $mysqluser = $properties['user'];
    $mysqlpassword = $properties['password'];
    $mysqldb = $properties['db'];
    $mysqlport = $properties['port'];
    
    $data = array(
      'secret' => $secretKey,
      'response' => $captcha,
      'remoteip' => $ip  // ip를 안 넣을거면 여기서도 빼줘야죠
    );
    
    $url = "https://www.google.com/recaptcha/api/siteverify";
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 10);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    $response = curl_exec($ch);
    curl_close($ch);
    
    $responseKeys = json_decode($response, true);

    if ($responseKeys["success"]) {
        $is_authorized = true;
        $key = md5($userid.strval($now_timestamp));

        $con=mysqli_connect($mysqlhost,$mysqluser,$mysqlpassword,$mysqldb,$mysqlport);
        if (mysqli_connect_errno()) {
            echo "Failed to connect to MySQL: " . mysqli_connect_error();
        }

        $sql = "INSERT INTO auth (id,`key`) VALUES ('".$userid."','".$key."') ON DUPLICATE KEY UPDATE `key`='".$key."'";
        if (!mysqli_query($con,$sql)) {
            die('Error: ' . mysqli_error($con));
        }

        mysqli_close($con);
    }
?>
<!DOCTYPE html>
<html lang="ko">
<head>
    <title>Generate Key for Furluckbot</title>
</head>
<body>
<?php
    if ($is_authorized) {
?>
    <table border="0.5px solid black">
        <tr>
            <td>ID</td>
            <td><?php echo ($userid)?></td>
        </tr>
        <tr>
            <td>KEY</td>
            <td><?php echo ($key)?></td>
        </tr>
    </table>
<?php
    } else {
        echo ("잘못된 접근입니다.");
    }
?>
</body>