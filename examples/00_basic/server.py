# 
# Server
# 
# Example 0: Global and User Text Editor
# ======================================
#
# This server demonstrates the access control of two endpoints:
#  - /text/global.txt
#  - /text/user/<username>.txt
#
# All registered users can read and write to the /text/global.txt, however
# only a user can read and write to their own /text/user/<username>.txt file.
#
# The user management endpoints are implemented by the flask_restful_auth
# package. By default, they include:
# - /user/signup
# - /user/login
# - /user/logout