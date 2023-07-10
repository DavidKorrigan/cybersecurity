<?php
	// Internal redirection
	$external_redirect_url = "http://172.17.0.2/read_cookie.php";
	$external_redirect_code = 301;

	header("Location: " . $external_redirect_url, true, $external_redirect_code);
?>