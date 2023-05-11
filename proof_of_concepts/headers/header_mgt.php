<?php
echo "<h2>Set cookie</h2>";

$cookie_name = "session";
$cookie_value = guidv4();

echo "<p>Cookie name: " . $cookie_name . "</p>";

echo "<p>Cookie value: " . $cookie_value . "</p>";

# httponly block browser to give cookie to JavaScripts
setcookie(
        $cookie_name,
        $cookie_value,
        $expires_or_options = 0,
        $path = "",
        $domain = "",
        $secure = false,
        $httponly = false
);

cors();

function guidv4($data = null) {
    // Generate 16 bytes (128 bits) of random data or use the data passed into the function.
    $data = $data ?? random_bytes(16);
    assert(strlen($data) == 16);

    // Set version to 0100
    $data[6] = chr(ord($data[6]) & 0x0f | 0x40);
    // Set bits 6-7 to 10
    $data[8] = chr(ord($data[8]) & 0x3f | 0x80);

    // Output the 36 character UUID.
    return vsprintf('%s%s-%s-%s-%s-%s%s%s', str_split(bin2hex($data), 4));
}

/**
 *  An example CORS-compliant method.  It will allow any GET, POST, or OPTIONS requests from any
 *  origin.
 *
 *  In a production environment, you probably want to be more restrictive, but this gives you
 *  the general idea of what is involved.  For the nitty-gritty low-down, read:
 *
 *  - https://developer.mozilla.org/en-US/search?q=HTTP%20access%20control
 *  - https://fetch.spec.whatwg.org/#http-cors-protocol
 *
 */
function cors() {

	header("Access-Control-Allow-Origin: *");
	header('Access-Control-Allow-Credentials: true');
	header('Access-Control-Max-Age: 86400');    // cache for 1 day
	header("Access-Control-Allow-Methods: GET");
		

    
    // Access-Control headers are received during OPTIONS requests
    if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
        
        if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_METHOD']))
            // may also be using PUT, PATCH, HEAD etc
            header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
        
        if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']))
            header("Access-Control-Allow-Headers: {$_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']}");
    
        exit(0);
    }
    
    echo "You have CORS!";
}


?>
<script>
	function listCookies() {
		var theCookies = document.cookie.split(';');
		var aString = '';
		for (var i = 1 ; i <= theCookies.length; i++) {
			aString += i + ' ' + theCookies[i-1] + "\n";
		}
		return aString;
	}
	alert(listCookies())

</script>

<html>
<head>
<!--
For the POC: Allow image from the same origin, allow use of inline source elements such as style attribute, onclick, or script tag bodies and javascript: URIs, allow scripts from ajax.googleapis.com
Header Set Content-Security-Policy "img-src 'self'; script-src 'unsafe-inline' ajax.googleapis.com;"

Allow everything but only from the same origin
Header Set Content-Security-Policy "default-src 'self'"

Only Allow Scripts from the same origin
Header Set Content-Security-Policy "script-src" 'self';"

Starter Policy: This policy allows images, scripts, AJAX, form actions, and CSS from the same origin, and does not allow any other resources to load (eg object, frame, media, etc). It is a good starting point for many sites.
Header Set Content-Security-Policy "default-src 'none'; script-src 'self'; connect-src 'self'; img-src 'self'; style-src 'self'; base-uri 'self'; form-action 'self'"

 -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
<script>
$(document).ready(function(){
  $("p").click(function(){
    $(this).hide();
  });
});
</script>
</head>
<body>

<p>If you click on me, I will disappear.</p>
<p>Click me away!</p>
<p>Click me too!</p>

</body>
</html>
