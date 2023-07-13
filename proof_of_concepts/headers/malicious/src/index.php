<?php
	// Configuration to load external resource in PHP
	$external_resource_url = "http://172.17.0.2/read_cookie.php";
	$enable_load_external_resource = false;


	if ($enable_load_external_resource === true) {
		php_loader($external_resource_url);
	}

	// Load an external resource
	function php_loader($external_resource_url) {
		// create a new cURL resource
		$ch = curl_init();

		// set URL and other appropriate options
		curl_setopt($ch, CURLOPT_URL, $external_resource_url);
		curl_setopt($ch, CURLOPT_HEADER, 0);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

		// grab URL and pass it to the browser
		$output = curl_exec($ch);
		
		print($output);
		
		// close cURL resource, and free up system resources
		curl_close($ch);
	}
?>
<!doctype html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
		<title>Domain 2</title>
		<script src="https://code.jquery.com/jquery-3.7.0.js" integrity="sha256-JlqSTELeR4TLqP0OG9dxM7yDPqX1ox/HfgiSLBj8+kM=" crossorigin="anonymous"></script>
	</head>
	<body>
		<h1>List of operations</h1>
		<ul>
			<li><a href="http://172.17.0.2/read_cookie.php">Direct link to read_cookie.php</a></li>
			<li><a href="http://172.17.0.3/csrf_01.html">Link to CSRF</a></li>
			<li><a href="http://172.17.0.3/external_redirect.php">Link to External redirect</a></li>
			<li id="response"></li>
		</ul>
	</body>
	
	<!-- Load external resource in Javascript -->
	<script>
		$(function(){
			$('#response').load('http://172.17.0.2/read_cookie.php');
		});
	</script>
</html>