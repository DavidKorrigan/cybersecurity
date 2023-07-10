# Cookie setting, CSP & CORS
# Proof of Concept

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

Cookie is only sent to the Webhook via HTTP request.
### Scenario 11 - HTTP Request - External link - HttpOnly=true
Link to the Webhook

    - path=/
    - Secure=false
    - HttpOnly=true
    - SameSite=None

Cookie is not forwarded to exteral link.
### Scenario 12 - HTTP Request - Internal link - No Protection
Internal link to read_cookie.php

    - path=/
    - Secure=false
    - HttpOnly=false
    - SameSite=None

Cookie is accessible on read_cookie.php.

Cookie is sent by the local & external Javascript to the Webhook.
### Scenario 13 - HTTP Request - Internal link - HttpOnly=true - path=header_mgt.php
Internal link to read_cookie.php

    - path=/read_cookie.php
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