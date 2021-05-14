"""
**Direction of testing**

It is the intention that in a week, this project will have automated testing but for now.

**Postman testing for login**

The goal of these steps is to verify the login process works. This process uses Basic Auth for Authentication and JWT stored as a cookie called `token` for authorisation.

**Check that a user is unauthorised by default**

    1. Using postman, create a new GET request::

         http://127.0.0.1:5000/text/user/u1.txt

    2. Under the Send button there is a cookie button, ensure there are no cookies.
    3. Send the request. The test is successful if a 401 "not authorized" is received in response.

**Authenticate and aquire the authorisation token**

    1. Using postman, create a new POST request::

         http://127.0.0.1:5000/user/login

    2. Change the authorization type to `Basic Auth`.
    3. Change the username and password to (`u1`, `password`)
    4. Send the request. The test is successful if a 200 "ok" is received in response and a cookie named `token` is aquired.

**Access the restricted resource**

    1. Go back to the GET request::

         http://127.0.0.1:5000/text/user/u1.txt

    2. Make sure the `token` cookie is stored and will ne included in the request.
    3. Send the request. The test is successful if a 200 "TODO" is received in response.
"""