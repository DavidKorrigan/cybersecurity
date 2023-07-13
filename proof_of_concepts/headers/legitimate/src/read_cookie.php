<?php
	// Header configuration
	$enable_cors = true;
	/**
	 * Possible value
	 * Access-Control-Allow-Origin: *
	 * Access-Control-Allow-Origin: http://172.17.0.2
	 * Access-Control-Allow-Origin: http://172.17.0.3
	 */
	$cors_configuration = "Access-Control-Allow-Origin: http://172.17.0.2";

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
		header('Access-Control-Allow-Credentials: true');
		//header('Access-Control-Max-Age: 86400');    // cache for 1 day
		//header("Access-Control-Allow-Methods: POST");
		//header("Access-Control-Allow-Headers: {$_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']}");
	}


	foreach ($_COOKIE as $key=>$val)
	{
    		echo $key.' is '.$val."<br>\n";
  	}
?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
		<title>Domain 1</title>
	</head>
	<body>
	<p>This is a resource from domain 1</p>
	</body>
</html>