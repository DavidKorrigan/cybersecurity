# Cookie setting, CSP & CORS
# Proof of Concept
## Usage
### Configuration
In headers/legitimate/src/index.php, update PHP variables:
```
// Cookie configuration
$cookie_path = '/';
$cookie_domain = $_SERVER['HTTP_HOST'];
$cookie_secure = false;
$cookie_httponly = false;
$cookie_samesite = 'lax';

// Header configuration
$enable_csp = false;
$csp_configuration = "Content-Security-Policy: script-src 'unsafe-inline' 172.17.0.3;";

// Webhook for HTTP Request
$http_url = "https://3ceaad7a-8dde-49e1-8b18-550cbe9fbc34.requestcatcher.com/test";

// Send a HTTP request from server to the webhook with cookie value
$enable_server_request = false;

```

Then update webhook in Javascript:
```
var webhook_url = "3ceaad7a-8dde-49e1-8b18-550cbe9fbc34.requestcatcher.com";
```

In headers/legitimate/src/read_cookie.php, update PHP variables:

```
// Header configuration
$enable_cors = true;
$cors_configuration = "Access-Control-Allow-Origin: http://172.17.0.2";
```

In headers/malicious/src/gotcha.js, update webhook in Javascript:
```
var webhook_url = "3ceaad7a-8dde-49e1-8b18-550cbe9fbc34.requestcatcher.com";
```

In headers/malicious/src/index.php, update PHP variables:
```
// Configuration to load external resource in PHP
$external_resource_url = "http://172.17.0.2/read_cookie.php";
$enable_load_external_resource = false;
```

### Start containers
- ./headers/legitimate/buildNstart.sh
- ./headers/malicious/buildNstart.sh

## Scenarii
### Scenario 1 - Local JavaScript - No protection

    - path=/
    - Secure=false
    - HttpOnly=false
    - SameSite=None

Cookie is sent to the Webhook in http & https.
### Scenario 2 - Local JavaScript - HttpOnly=true

    - path=/
    - Secure=false
    - HttpOnly=true
    - SameSite=None

Cookie is not sent to the Webhook in http & https.
### Scenario 3 - Local JavaScript - Secure=true

    - path=/
    - Secure=true
    - HttpOnly=false
    - SameSite=None

Browser raises the error: "Cookie 'PHPSESSID' has been rejected because a non-HTTPS cookie can’t be set as 'secure'.".

Cookie is not sent to the Webhook in http & https.
### Scenario 4 - Local JavaScript - Set CORS

    - path=/
    - Secure=false
    - HttpOnly=false
    - SameSite=None
    - Access-Control-Allow-Methods: POST

Cookie is sent to the Webhook in http & https even with GET HTTP method.
### Scenario 5 - External JavaScript - No protection

    - path=/
    - Secure=false
    - HttpOnly=false
    - SameSite=None

Cookie is sent by the external Javascript to the Webhook in http & https.
### Scenario 6 - External JavaScript - SameSite=Strict

    - path=/
    - Secure=false
    - HttpOnly=false
    - SameSite=Strict

Cookie is sent by the external Javascript to the Webhook even with strict samesite.
### Scenario 7 - JavaScript - CSP: Allow everything but only from the same origin

    - path=/
    - Secure=false
    - HttpOnly=false
    - SameSite=None
    - Content-Security-Policy: default-src 'self'

Cookie is not sent. Inline & external JavaScript load are blocked.
### Scenario 8 - JavaScript - CSP: Allow all inline >script< elements

    - path=/
    - Secure=false
    - HttpOnly=false
    - SameSite=None
    - Content-Security-Policy: script-src 'unsafe-inline'

Cookie is sent only by the local Javascript to the Webhook.
### Scenario 9 - JavaScript - CSP: Allow all inline >script< elements & specific origin

    - path=/
    - Secure=false
    - HttpOnly=false
    - SameSite=None
    - Content-Security-Policy: script-src 'unsafe-inline' 172.17.0.3

Cookie is sent by the local & external Javascript to the Webhook.
### Scenario 10 - HTTP Request - HttpOnly=true

    - path=/
    - Secure=false
    - HttpOnly=true
    - SameSite=None

Cookie is only sent to the Webhook via server side HTTP request.
### Scenario 11 - HTTP Request - External link - HttpOnly=true
Link to the Webhook

    - path=/
    - Secure=false
    - HttpOnly=true
    - SameSite=None

Cookie is not forwarded to external link.
### Scenario 12 - HTTP Request - Internal link - No Protection
Internal link to read_cookie.php

    - path=/
    - Secure=false
    - HttpOnly=false
    - SameSite=None

Cookie is accessible on read_cookie.php.

Cookie is sent by the local & external Javascript to the Webhook.
### Scenario 13 - HTTP Request - Internal link - HttpOnly=true - path=index.php
Internal link to read_cookie.php

    - path=/index.php
    - Secure=false
    - HttpOnly=true
    - SameSite=None

Cookie is not accessible on read_cookie.php.

Cookie is not sent by the local & external Javascript to the Webhook.
### Scenario 14 - HTTP Request - Form - HttpOnly=true - samesite=none

    - path=/
    - Secure=false
    - HttpOnly=true
    - SameSite=None

Cookie is accessible on read_cookie.php.
### Scenario 15 - HTTP Request - CSRF - HttpOnly=true - samesite=none
Go to http://172.17.0.3/csrf_01.html

    - path=/
    - Secure=false
    - HttpOnly=true
    - SameSite=None

Cookie is accessible on read_cookie.php.
### Scenario 16 - HTTP Request - CSRF - HttpOnly=true - samesite=Strict
Go to http://172.17.0.3/csrf_01.html

    - path=/
    - Secure=false
    - HttpOnly=true
    - SameSite=Strict

Cookie is not accessible on read_cookie.php.
### Scenario 17 - HTTP Request - External redirect - samesite=none
Go to http://172.17.0.3/external_redirect.php

    - path=/
    - Secure=false
    - HttpOnly=true
    - SameSite=none

Cookie is accessible on read_cookie.php.
### Scenario 18 - HTTP Request - External redirect - samesite=Strict
Go to http://172.17.0.3/external_redirect.php

    - path=/
    - Secure=false
    - HttpOnly=true
    - SameSite=Strict

Cookie is not accessible on read_cookie.php.
### Scenario 19 - HTTP Request - External redirect - samesite=Lax
Go to http://172.17.0.3/external_redirect.php

    - path=/
    - Secure=false
    - HttpOnly=true
    - SameSite=Lax

Cookie is accessible on read_cookie.php.
### SScenario 20 - CORS - Enable for Domain 1
Go to http://172.17.0.3/index.php

    - Access-Control-Allow-Origin: http://172.17.0.2

Message: "This is a resource from domain 1" is not displayed
### Scenario 21 - CORS - Wildcard
Go to http://172.17.0.3/index.php

    - Access-Control-Allow-Origin: *

Message: "This is a resource from domain 1" is displayed
### Scenario 22 - CORS - Enable for Domain 2
Go to http://172.17.0.3/index.php

    - Access-Control-Allow-Origin: http://172.17.0.3

Message: "This is a resource from domain 1" is displayed