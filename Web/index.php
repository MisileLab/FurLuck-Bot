<?php
    $properties = parse_ini_file('captcha.key');
    $site_key = $properties['site'];
?>
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>reCaptcha for Furluckbot</title>
    <script src="https://www.google.com/recaptcha/api.js?render=<?php echo ($site_key)?>"></script>
    <script type="text/javascript">
        document.addEventListener("DOMContentLoaded", function(){
            grecaptcha.ready(function(){
                grecaptcha.execute('<?php echo ($site_key)?>',{action:'homepage'}).then(function(token){
                    document.getElementById('g-recaptcha').value = token;
                })
            })
        })
    </script>
</head>
<body>
    <div>Furluckbot의 인증키를 만들 수 있습니다.</div>
    <form name="generate-key" method="POST" action="generate-key.php">
        <input type="hidden" id="g-recaptcha" name="g-recaptcha">
        <input type="hidden" id="userid" name="userid" value="<?php echo $_GET["id"] ?>">
        <input type="submit" value="인증키 만들기">
    </form>
</body>